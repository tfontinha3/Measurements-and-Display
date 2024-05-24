import requests
import pycurl
import json
from io import BytesIO
from time import time

from .models import Oscilloscope

BASE_URL = "http://localhost:29700/api/oscilloscope/"

def connect():
    res = requests.post(BASE_URL)
    response = json.loads(res.text)
    return response


def get_measurements(channel):
    url = f"http://localhost:29700/api/oscilloscope/measurement/single/{channel}/VRMS/CURR"

    # Create a BytesIO object to store the response
    response_buffer = BytesIO()
    
    # Initialize pycurl
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEDATA, response_buffer)
    
    # Perform the request
    c.perform()
    c.close()
    
    # Get the response and decode it
    response_body = response_buffer.getvalue().decode('utf-8')
    
    # Parse the response as JSON
    response = json.loads(response_body)
    
    return response

#idn = connect()
#print(idn)

server = Oscilloscope("192.168.1.10")

for i in range(100):
    start = time()
    #print(get_measurements(1), time()-start)
    print(server.get_measurement(1, "CURR", "VRMS"), time()-start)