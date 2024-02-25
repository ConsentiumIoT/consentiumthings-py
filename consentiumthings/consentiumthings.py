import requests
from urllib.parse import urljoin


class consentiumthings:
    BASE_URL = "https://consentiuminc.online/api/board/"

    def __init__(self, board_key):
        self.board_key = board_key
        self.send_url = urljoin(self.BASE_URL, "updatedata")
        self.receive_url = urljoin(self.BASE_URL, "getdata")
        self.receive_recent_url = urljoin(self.BASE_URL, "getdata/recent")
        self.session = requests.Session()

    def begin_send(self, send_key):
        self.send_key = send_key
        self.send_url = f"{self.send_url}?key={send_key}&boardkey={self.board_key}"

    def begin_receive(self, receive_key, recent=True):
        self.receive_key = receive_key
        base_url = self.receive_recent_url if recent else self.receive_url
        self.receive_url = f"{base_url}?receivekey={receive_key}&boardkey={self.board_key}"

    def send_data(self, data_buff, info_buff):
        if len(data_buff) > 4 or len(info_buff) > 4:
            raise ValueError("Only four sensor data points are allowed.")

        sensor_data = [{"info": info, "data": str(data)} for data, info in zip(data_buff, info_buff)]
        payload = {
            "sensors": {"sensorData": sensor_data},
            "boardInfo": {"firmwareVersion": "0.0", "architecture": "GenericPython"}
        }

        try:
            response = self.session.post(self.send_url, json=payload)
            response.raise_for_status()
            print(response.text)
        except requests.exceptions.RequestException as e:
            print(f"An error occurred during sending data: {e}")

    def receive_data(self):
        try:
            response = self.session.get(self.receive_url)
            response.raise_for_status()
            data = response.json().get('sensors', [])
        except (requests.exceptions.RequestException, ValueError) as e:
            print(f"An error occurred during receiving data: {e}")
            return {}

        sensor_data = {}
        for item in data:
            for sensor in item.get('sensorData', []):
                sensor_type = sensor.get('info')
                if sensor_type:
                    sensor_data.setdefault(sensor_type, []).append({'data': sensor.get('data'),
                                                                    'updatedAt': sensor.get('updatedAt')})
        return sensor_data
