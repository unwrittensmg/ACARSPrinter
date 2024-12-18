from flask import Flask, render_template, jsonify, request
import os
import json
import requests  # For fetching METAR and ATIS data
import threading

app = Flask(__name__)

# Paths and Constants
DATA_FOLDER = os.path.join(os.getcwd(), "data")
SETTINGS_FILE = os.path.join(DATA_FOLDER, "settings.json")

# Ensure the data folder exists
os.makedirs(DATA_FOLDER, exist_ok=True)


# Load settings
def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as file:
            return json.load(file)
    return {"callsign": "", "logon_code": "", "simbrief_username": ""}


@app.route("/")
def index():
    """Render the main page."""
    return render_template("index.html")


# API Endpoint: Fetch METAR
@app.route("/api/metar", methods=["GET"])
def get_metar():
    icao = request.args.get("icao", "").upper()
    if not icao:
        return jsonify({"error": "No ICAO code provided"}), 400

    try:
        # Fetch METAR data from aviationweather.gov
        url = f"https://aviationweather.gov/api/data/metar?ids={icao}&format=raw"
        response = requests.get(url)
        response.raise_for_status()

        data = response.text.strip()
        if not data:
            return jsonify({"error": f"No METAR data found for {icao}."}), 404

        return jsonify({"metar": data})
    except Exception as e:
        return jsonify({"error": f"Failed to fetch METAR: {str(e)}"}), 500


# API Endpoint: Fetch ATIS (VATSIM)
@app.route("/api/atis", methods=["GET"])
def get_atis():
    icao = request.args.get("icao", "").upper()
    if not icao:
        return jsonify({"error": "No ICAO code provided"}), 400

    vatsim_url = "https://data.vatsim.net/v3/vatsim-data.json"
    try:
        response = requests.get(vatsim_url)
        response.raise_for_status()
        data = response.json()

        # Filter ATIS data based on ICAO
        atis_messages = [
            f"{entry['callsign']}: {' '.join(entry['text_atis'])}"
            for entry in data.get("atis", [])
            if icao in entry['callsign']
        ]

        if atis_messages:
            return jsonify({"messages": atis_messages})
        else:
            return jsonify({"error": f"No ATIS data found for {icao}."}), 404
    except Exception as e:
        return jsonify({"error": f"Failed to fetch ATIS data: {str(e)}"}), 500


# API Endpoint: Print Simulation
@app.route("/api/print", methods=["POST"])
def print_data():
    data = request.json
    script = data.get("script", "")
    content = data.get("content", "")

    if not script or not content:
        return jsonify({"error": "Invalid print request"}), 400

    try:
        # Simulated print functionality
        print(f"Printing using {script}: {content}")
        return jsonify({"message": "Data sent to printer successfully!"})
    except Exception as e:
        return jsonify({"error": f"Failed to print: {str(e)}"}), 500


if __name__ == "__main__":
    print("Starting Flask App...")
    app.run(host="0.0.0.0", port=5000, debug=True)
