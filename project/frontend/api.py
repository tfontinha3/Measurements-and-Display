import requests

class OscilloscopeAPI:
    def __init__(self):
        self.base_url = ""

    def set_base_url(self, ip_address):
        self.base_url = f"http://{ip_address}/api/oscilloscope"

    def connect_to_oscilloscope(self):
        response = requests.post(url=self.base_url)
        return response.json()

    def get_waveform(self):
        response = requests.get(url=f"{self.base_url}/waveform")
        return response.json()
