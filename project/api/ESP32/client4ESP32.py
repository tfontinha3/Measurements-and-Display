import requests
import time

def fetch_data():
    url = "http://192.168.122.59/velocity"
    while True:
        try:
            print("Fetching velocity data from ESP32")
            response = requests.get(url)
            if response.status_code == 200:
                print("Received value:", response.text)
            else:
                print("Failed to retrieve data. Status code:", response.status_code)
        except Exception as e:
            print("Error occurred:", str(e),"\n")
        time.sleep(1)  # Delay for 1 second

if __name__ == "__main__":
    fetch_data()