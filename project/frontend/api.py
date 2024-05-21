import requests

class OscilloscopeAPI:
    def __init__(self):
        self.base_url = "http://CTR208:29700/api/oscilloscope"

    def connect_to_oscilloscope(self):
        response = requests.post(url=self.base_url)
        return response.json()

    def get_waveform(self):
        response = requests.get(url=f"{self.base_url}/waveform")
        return response.json()
