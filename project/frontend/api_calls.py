import requests
from ..api.oscilloscope_api import Oscilloscope


class OscilloscopeAPI:
    def __init__(self, ip):
        self.voltage_channel = 1
        self.current_channel = 2
        self.time = 0
        self.oscilloscope = Oscilloscope.Oscilloscope(ip)

    def connect_to_oscilloscope(self):
        try:
            self.oscilloscope.connect()
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


    def get_test():
        response = self.get_vrms(self.voltage_channel)
        #hmm pass from jsom to array
        return response
    #get_esp_values

