from flask import Flask, render_template, jsonify, request
import os
import json
import requests
from subprocess import run

app = Flask(__name__)

# Paths and Constants
DATA_FOLDER = os.path.join(os.getcwd(), "data")
SETTINGS_FILE = os.path.join(DATA_FOLDER, "settings.json")
API_KEYS_FILE = os.path.join(DATA_FOLDER, "api_keys.json")
AVWX_API_URL = "https://avwx.rest/api/metar/"
AVWX_TAF_URL = "https://avwx.rest/api/taf/"

# Ensure the data folder exists
os.makedirs(DATA_FOLDER, exist_ok=True)

if not os.path.exists(SETTINGS_FILE):
    with open(SETTINGS_FILE, "w") as file:
        json.dump({}, file)

if not os.path.exists(API_KEYS_FILE):
    with open(API_KEYS_FILE, "w") as file:
        json.dump({"avwx_api_key": "your_avwx_api_key"}, file)  # Default placeholder

@app.route("/")
def index():
    """Render the main page."""
    return render_template("index.html")

# API Endpoint: Fetch METAR and TAF from AVWX
@app.route("/api/metar", methods=["GET"])
def get_metar():
    icao = request.args.get("icao", "").upper()
    if not icao:
        return jsonify({"error": "No ICAO code provided"}), 400

    try:
        # Load API key from separate JSON file
        with open(API_KEYS_FILE, "r") as file:
            api_keys = json.load(file)
        avwx_api_key = api_keys.get("avwx_api_key", "")

        if not avwx_api_key:
            return jsonify({"error": "AVWX API key is missing. Please configure it."}), 500

        headers = {"Authorization": f"Bearer {avwx_api_key}"}

        # Fetch METAR
        metar_response = requests.get(f"{AVWX_API_URL}{icao}", headers=headers)
        metar_response.raise_for_status()
        metar_data = metar_response.json().get("raw", "METAR not available")

        # Fetch TAF
        taf_response = requests.get(f"{AVWX_TAF_URL}{icao}", headers=headers)
        taf_response.raise_for_status()
        taf_data = taf_response.json().get("raw", "TAF not available")

        return jsonify({"metar": metar_data, "taf": taf_data})
    except requests.RequestException as e:
        return jsonify({"error": f"Failed to fetch data: {str(e)}"}), 500

# API Endpoint: Fetch SimBrief Callsign
@app.route("/api/simbrief_callsign", methods=["GET"])
def fetch_simbrief_callsign():
    """Fetch the latest callsign from SimBrief for the given username."""
    simbrief_username = request.args.get("username", "").strip()
    if not simbrief_username:
        return jsonify({"error": "SimBrief username is required."}), 400

    try:
        # SimBrief API endpoint
        simbrief_url = f"https://www.simbrief.com/api/xml.fetcher.php?username={simbrief_username}"

        # Fetch data from SimBrief
        response = requests.get(simbrief_url)
        response.raise_for_status()

        # Parse XML response
        import xml.etree.ElementTree as ET
        root = ET.fromstring(response.text)
        callsign = root.find(".//general/icao_airline").text + root.find(".//general/flight_number").text

        return jsonify({"callsign": callsign})
    except requests.RequestException as e:
        return jsonify({"error": f"Failed to fetch SimBrief callsign: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Error processing SimBrief response: {str(e)}"}), 500

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

        return jsonify({"message": "CPDLC message sent to printer successfully!"})
    except Exception as e:
        return jsonify({"error": f"Failed to print CPDLC: {str(e)}"}), 500

# API Endpoint: Print METAR
@app.route("/api/print_metar", methods=["POST"])
def print_metar():
    try:
        data = request.json
        metar = data.get("metar", "")
        taf = data.get("taf", "")

        if not metar or not taf:
            return jsonify({"error": "METAR or TAF data is missing"}), 400

        # Call the print_metar.py script and pass METAR and TAF as arguments
        script_path = os.path.join("modules", "print_metar.py")
        run(["python", script_path, metar, taf], check=True)

        return jsonify({"message": "METAR and TAF sent to printer successfully!"})
    except Exception as e:
        return jsonify({"error": f"Failed to print METAR and TAF: {str(e)}"}), 500

# API Endpoint: Print ATIS
@app.route("/api/print_atis", methods=["POST"])
def print_atis():
    try:
        data = request.json
        message = data.get("message", "")

        if not message:
            return jsonify({"error": "No ATIS message provided"}), 400

        # Call the print_atis.py script and pass the ATIS message as an argument
        script_path = os.path.join("modules", "print_atis.py")
        run(["python", script_path, message], check=True)

        return jsonify({"message": "ATIS message sent to printer successfully!"})
    except Exception as e:
        return jsonify({"error": f"Failed to print ATIS: {str(e)}"}), 500

@app.route("/api/atis", methods=["GET"])
def get_atis():
    icao = request.args.get("icao", "").upper()
    if not icao:
        return jsonify({"error": "No ICAO code provided"}), 400

    try:
        # Example ATIS data source: Replace with your actual ATIS source
        vatsim_url = "https://data.vatsim.net/v3/vatsim-data.json"
        response = requests.get(vatsim_url)
        response.raise_for_status()

        data = response.json()

        # Filter ATIS data for the specified ICAO
        atis_messages = [
            f"{entry['callsign']}: {' '.join(entry['text_atis'])}"
            for entry in data.get("atis", [])
            if icao in entry["callsign"]
        ]

        if atis_messages:
            return jsonify({"messages": atis_messages})
        else:
            return jsonify({"error": f"No ATIS data found for {icao}."}), 404
    except requests.RequestException as e:
        return jsonify({"error": f"Failed to fetch ATIS: {str(e)}"}), 500


# API Endpoint: Get Settings
@app.route("/api/settings", methods=["GET"])
def get_settings():
    """Fetch current settings."""
    try:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r") as file:
                settings = json.load(file)
            return jsonify(settings)
        else:
            return jsonify({"error": "Settings file not found."}), 404
    except Exception as e:
        return jsonify({"error": f"Failed to fetch settings: {str(e)}"}), 500

# API Endpoint: Save Settings
@app.route("/api/settings", methods=["POST"])
def save_settings():
    """Save updated settings."""
    try:
        data = request.json
        print("Incoming settings data:", data)  # Debugging

        with open(SETTINGS_FILE, "w") as file:
            json.dump(data, file, indent=4)

        return jsonify({"message": "Settings saved successfully!"})
    except Exception as e:
        print("Error saving settings:", str(e))  # Debugging
        return jsonify({"error": f"Failed to save settings: {str(e)}"}), 500

if __name__ == "__main__":
    print("Starting Flask App...")
    app.run(host="0.0.0.0", port=5000, debug=True)
