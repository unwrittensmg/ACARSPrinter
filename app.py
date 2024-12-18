from flask import Flask, render_template, jsonify, request
import os
import json
import requests
from subprocess import run
from bs4 import BeautifulSoup

app = Flask(__name__)

# Paths and Constants
DATA_FOLDER = os.path.join(os.getcwd(), "data")
SETTINGS_FILE = os.path.join(DATA_FOLDER, "settings.json")

# Ensure the data folder exists
os.makedirs(DATA_FOLDER, exist_ok=True)


@app.route("/")
def index():
    """Render the main page."""
    return render_template("index.html")


# API Endpoint: Get Real CPDLC Messages from VATSIM
@app.route("/api/messages", methods=["GET"])
def get_messages():
    """Fetch real CPDLC messages from VATSIM."""
    try:
        # Fetch data from VATSIM's live data feed
        vatsim_url = "https://data.vatsim.net/v3/vatsim-data.json"
        response = requests.get(vatsim_url)
        response.raise_for_status()

        data = response.json()

        # Extract CPDLC messages from the VATSIM feed
        messages = []
        for flight in data.get('flight', []):
            # Assuming CPDLC messages are included in the 'messages' field of each flight
            if 'messages' in flight:
                for message in flight['messages']:
                    messages.append(message)

        if messages:
            return jsonify(messages)
        else:
            return jsonify({"error": "No CPDLC messages found."}), 404

    except Exception as e:
        return jsonify({"error": f"Failed to fetch CPDLC messages: {str(e)}"}), 500


# API Endpoint: Print CPDLC Message
@app.route("/api/print_cpdlc", methods=["POST"])
def print_cpdlc():
    try:
        data = request.json
        message = data.get("message", "")

        if not message:
            return jsonify({"error": "No message provided"}), 400

        # Call the print_cpdlc.py script and pass the message as an argument
        script_path = os.path.join("modules", "print_cpdlc.py")
        run(["python", script_path, message], check=True)

        return jsonify({"message": "Message sent to printer successfully!"})
    except Exception as e:
        return jsonify({"error": f"Failed to print: {str(e)}"}), 500


# API Endpoint: Get Settings
@app.route("/api/settings", methods=["GET"])
def get_settings():
    """Fetch current settings."""
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as file:
            settings = json.load(file)
        return jsonify(settings)
    return jsonify({"simbrief_username": "", "callsign": "", "logon_code": "", "printer_name": ""})


# API Endpoint: Save Settings
@app.route("/api/settings", methods=["POST"])
def save_settings():
    """Save updated settings."""
    try:
        data = request.json
        with open(SETTINGS_FILE, "w") as file:
            json.dump(data, file, indent=4)
        return jsonify({"message": "Settings saved successfully!"})
    except Exception as e:
        return jsonify({"error": f"Failed to save settings: {str(e)}"}), 500


# API Endpoint: Fetch METAR from VATSIM
@app.route("/api/metar", methods=["GET"])
def get_metar():
    icao = request.args.get("icao", "").upper()
    if not icao:
        return jsonify({"error": "No ICAO code provided"}), 400

    try:
        # Directly fetch METAR data from VATSIM's live data feed
        vatsim_url = "https://data.vatsim.net/v3/vatsim-data.json"
        response = requests.get(vatsim_url)
        response.raise_for_status()

        data = response.json()

        # Search for METAR data in the flight information
        for flight in data.get('flight', []):
            if 'metar' in flight and flight.get('callsign') == icao:
                metar_data = flight['metar']
                if metar_data:
                    return jsonify({"metar": metar_data})

        # If no METAR found for the ICAO code in the VATSIM feed
        return jsonify({"error": f"No METAR data found for {icao}."}), 404

    except requests.exceptions.RequestException as e:
        # This will catch any request-related exceptions (e.g., network errors)
        return jsonify({"error": f"Failed to fetch METAR data: {str(e)}"}), 500
    except Exception as e:
        # This will catch any other exceptions (e.g., parsing errors)
        return jsonify({"error": f"An error occurred while fetching METAR data: {str(e)}"}), 500


# API Endpoint: Fetch ATIS from VATSIM
@app.route("/api/atis", methods=["GET"])
def get_atis():
    icao = request.args.get("icao", "").upper()
    if not icao:
        return jsonify({"error": "No ICAO code provided"}), 400

    try:
        # Fetch ATIS data from VATSIM API
        vatsim_url = "https://data.vatsim.net/v3/vatsim-data.json"
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


# API Endpoint: Print ATIS (Triggered when printing ATIS message)
@app.route("/api/print_atis", methods=["POST"])
def print_atis():
    try:
        data = request.json
        message = data.get("message", "")

        if not message:
            return jsonify({"error": "No ATIS message provided"}), 400

        # Call the print_cpdlc.py script and pass the ATIS message as an argument
        script_path = os.path.join("modules", "print_cpdlc.py")
        run(["python", script_path, message], check=True)

        return jsonify({"message": "ATIS message sent to printer successfully!"})
    except Exception as e:
        return jsonify({"error": f"Failed to print ATIS: {str(e)}"}), 500


if __name__ == "__main__":
    print("Starting Flask App...")
    app.run(host="0.0.0.0", port=5000, debug=True)
