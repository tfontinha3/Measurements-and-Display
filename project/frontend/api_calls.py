import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api.oscilloscope_api.Oscilloscope import Oscilloscope

class OscilloscopeAPI:
    def __init__(self, ip):
        self.voltage_channel = 1
        self.current_channel = 2
        self.time = 0
        self.ip = ip
        self.connected = False
        self.oscilloscope = Oscilloscope(self.ip)

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
        array = []
        #add 27 to the array
        self.time += 0.01
        array.append((self.time,27))
        return array

    def get_voltage(self):
        response = self.get_vrms(self.voltage_channel)
        #hmm pass from jsom to array
        return response


    def get_test(self):
        response = self.get_vrms(self.voltage_channel)
        #hmm pass from jsom to array
        return "AAAAAAAAAA"
    #get_esp_values
    
""" if __name__ == "__main__":
    oscilloscope = OscilloscopeAPI("192.168.1.10")
    oscilloscope.connect_to_oscilloscope()
    print(oscilloscope.get_test())
 """