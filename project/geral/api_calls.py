import requests
import Oscilloscope
import math
import time
from velocity import Velocity

class API:
    def __init__(self, ip):
        self.voltage_channel = 1
        self.current_channel = 2

        self.speedSensor = Velocity()

        self.time = 0
        self.oscilloscope = Oscilloscope.Oscilloscope(ip)
        self.start_time = time.time()
        self.connected = False

    def connect(self):
        try:
            self.oscilloscope.connect()
            self.connected = True
            return self.oscilloscope.idn
        except Exception as ex:
            print("Error connecting to Oscilloscope")

    def get_waveform(self):
        try:
            data = self.oscilloscope.get_waveform_samples()
            return data.body
        except Exception as ex:
            print("Error communicating to Oscilloscope")
    
    def get_vrms(self, channel):
        try:
            data = self.oscilloscope.get_measurement(channel, "CURR", "VRMS")
            return data.body
        except Exception as ex:
            print("Error communicating to Oscilloscope")

    def get_full_measurements(self, channel, item = "FREQ"):
        try:
            data = self.oscilloscope.get_full_measurement(channel, item)
            return data.body
        except Exception as ex:
            print("Error communicating to Oscilloscope")


    def get_velocity(self):
        data = self.speedSensor.get_data()
        
        return data

    def get_voltage(self):
        response = self.get_vrms(self.voltage_channel)
        #hmm pass from jsom to array
        elapsed_time = time.time() - self.start_time
        measurements = []
        measurements.append((elapsed_time, response))
        return measurements
    
    def get_current(self):
        response = self.get_vrms(self.current_channel)
        #hmm pass from jsom to array
        measurements = []
        if response:
            elapsed_time = time.time() - self.start_time
            measurements.append((elapsed_time, response))
        return measurements

    def get_test(self):
        # Get the elapsed time since the start
        elapsed_time = time.time() - self.start_time
        # Calculate the sine value
        sine_value = math.sin(elapsed_time)
        array = []
        array.append((elapsed_time, sine_value))
        return array
    
    #get_esp_values
    
if __name__ == "__main__":
    oscilloscope = API("0.0.0.0")
    while True:
        print(oscilloscope.get_velocity())
        time.sleep(0.5)
