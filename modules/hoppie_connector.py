import os
import time
from hoppie_connector import HoppieConnector, HoppieError
import json

DATA_FOLDER = os.path.join(os.getcwd(), "data")
SETTINGS_FILE = os.path.join(DATA_FOLDER, "settings.json")
MESSAGES_FILE = os.path.join(DATA_FOLDER, "messages.txt")

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as file:
            return json.load(file)
    return {"callsign": "", "logon_code": ""}

def main():
    settings = load_settings()
    callsign = settings.get("callsign", "")
    logon_code = settings.get("logon_code", "")

    if not callsign or not logon_code:
        print("Callsign and logon code are required in settings.json!")
        return

    try:
        print(f"Starting Hoppie Connector for callsign: {callsign}")
        cnx = HoppieConnector(callsign, logon_code)

        while True:
            messages, delay = cnx.peek()
            with open(MESSAGES_FILE, "a") as file:
                for m_id, msg in messages:
                    formatted_message = f"Message {m_id}: {msg}"
                    print(formatted_message)
                    file.write(formatted_message + "\n")
            time.sleep(delay)

    except HoppieError as e:
        print(f"Hoppie Error: {e}")

if __name__ == "__main__":
    main()
