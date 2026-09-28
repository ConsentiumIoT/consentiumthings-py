import requests
from urllib.parse import urljoin
import uuid
from datetime import datetime, timezone

class ConsentiumThings:
    __BASE_URL = "https://api.consentiumiot.com/"

    def __init__(self, board_key):
        self.__receive_recent = None
        self.__board_key = board_key
        self.__send_url = urljoin(self.__BASE_URL, "v2/updateData")
        self.__receive_url = urljoin(self.__BASE_URL, "getData")
        self.__session = requests.Session()
        self.__send_key = None
        self.__receive_key = None

    def begin_send(self, send_key):
        self.__send_key = send_key

    def begin_receive(self, receive_key, recents=False):
        self.__receive_key = receive_key
        self.__receive_recent = recents

    def send_data(self, data_buff, info_buff, firmware="0.0", arch="GenericPython",
                  status_ota=False, signal_strength=-100):
        """
        Send sensor data to Consentium IoT Cloud.
        """
        if not self.__send_key:
            raise ValueError("Send key not initialized. Call begin_send first.")

        sensor_data = [{"info": info, "data": str(data)}
                       for data, info in zip(data_buff, info_buff)]

        mac = ":".join(f"{b:02x}" for b in uuid.getnode().to_bytes(6, "big"))

        payload = {
            "sensors": {"sensorData": sensor_data},
            "boardInfo": {
                "firmwareVersion": firmware,
                "architecture": arch,
                "statusOTA": status_ota,
                "deviceMAC": mac,
                "signalStrength": signal_strength
            }
        }

        params = {"sendKey": self.__send_key, "boardKey": self.__board_key}

        try:
            response = self.__session.post(self.__send_url, params=params, json=payload)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as http_err:
            # If the server sent a JSON error message, capture it
            try:
                error_payload = response.json()
            except ValueError:
                error_payload = {"message": response.text}

            print(f"HTTP error {response.status_code}: {error_payload.get('message')}")
            return error_payload  # Return JSON error payload for caller to handle

        except requests.exceptions.RequestException as e:
            # Covers network errors, timeouts, etc.
            print(f"An error occurred during sending data: {e}")
            return {"message": str(e)}

    def receive_data(self, start_date_time=None, end_date_time=None):
        """
        Fetch sensor data from Consentium IoT Cloud.
        Returns a dictionary mapping sensor labels (info1, info2...) to values.
        """
        if not self.__receive_key:
            raise ValueError("Receive key not initialized. Call begin_receive first.")

        params = {
            "receiveKey": self.__receive_key,
            "boardKey": self.__board_key
        }

        if self.__receive_recent and (start_date_time or end_date_time):
            raise ValueError(
                "Time slicing parameters (start_time/end_time) cannot be used "
                "because 'recents=True' was set in begin_receive()."
            )

        if self.__receive_recent:
            params["recents"] = "true"
        else:
            params["recents"] = "false"
            # Assuming your backend API accepts these exact parameter names.
            # Update keys if the API expects "start" / "end" instead.
            if start_date_time:
                params["from"] = start_date_time
            if end_date_time:
                params["to"] = end_date_time

        try:
            response = self.__session.get(self.__receive_url, params=params)
            response.raise_for_status()
            payload = response.json()
        except (requests.exceptions.RequestException, ValueError) as e:
            print(f"An error occurred during receiving data: {e}")
            return {}

        board = payload.get("board", {})
        feeds = payload.get("feeds", [])

        sensor_map = {f"info{i}": f"value{i}" for i in range(1, len(board) + 1) if f"info{i}" in board}

        parsed_data = []
        for feed in feeds:
            time_str = feed.get("updated_at")
            dt_naive = datetime.fromisoformat(time_str)
            dt_utc = dt_naive.replace(tzinfo=timezone.utc)
            dt_local = dt_utc.astimezone()
            local_updated_at = dt_local.isoformat(timespec='milliseconds')

            entry = {"updated_at": local_updated_at}
            for info_key, value_key in sensor_map.items():
                label = board.get(info_key)
                if label and value_key in feed:
                    entry[label] = feed[value_key]
            parsed_data.append(entry)

        return parsed_data
