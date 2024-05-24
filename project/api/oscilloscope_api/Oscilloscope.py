#from lib.Response import Response
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lib.Response import Response

from .instruments import DS1000Z

class Oscilloscope:
    def __init__(self, hostname):
        self.hostname = hostname

    def connect(self):
        self.instrument = DS1000Z(self.hostname)
        self.idn = self.instrument.get_identification()
        return Response(True, 0, self.idn)
    
    def select_probe(self, channel, probe: int):
        self.instrument.set_probe_ratio(probe, channel)
        return Response(True, 0, None)

    def get_probe(self, channel):
        probe = self.instrument.get_probe_ratio(channel)
        return Response(True, 0, probe)

    def show_only_selected_channel(self, channel: int):
        for i in range(1, 4):
            if i == channel:
                self.instrument.show_channel(i)
            else:
                self.instrument.hide_channel(i)
        return Response(True, 0, None)

    def get_sample_rate(self):
        self.current_sample_rate = self.instrument.get_sample_rate()
        return Response(True, 0, self.current_sample_rate)
    
    def autoscale(self):
        self.instrument.autoscale()
        self.is_autoscale = True
        return Response(True, 0, None)

    def clear_screen(self):
        self.instrument.clear()
        return Response(True, 0, None)

    def run(self, run: bool = True):
        self.instrument.run() if run else self.instrument.stop()
        return Response(True, 0, None)

    def get_channel_coupling(self, channel: int = 1):
        channel_coupling = self.instrument.get_channel_coupling(channel)
        return Response(True, 0, channel_coupling)
    
    def set_channel_coupling(self, channel: int = 1, coupling: str = "DC"):
        if coupling not in ["AC", "DC", "GND"]:
            return "Invalid coupling mode. Availables: DC, AC, DND"
        self.instrument.set_channel_coupling(channel)
        return Response(True, 0, None)

    def get_channel_offset(self, channel: int = 1):
        self.offset = self.instrument.get_channel_offset(channel)
        return Response(True, 0, self.offset)
    
    def set_channel_offset(self, channel: int = 1, offset: float = 0):
        self.offset = self.instrument.set_channel_offset(offset, channel)
        return Response(True, 0, None)

    def get_channel_vrange(self, channel: int = 1):
        self.range = self.instrument.get_channel_range(channel)
        return Response(True, 0, self.range)
    
    def set_channel_vrange(self, channel: int = 1, range: float = 8):
        self.offset = self.instrument.set_channel_range(range, channel)
        return Response(True, 0, None)

    def reset(self):
        self.instrument.reset()
        return Response(True, 0, None)

    def enable_source(self, source: int = 1, state: bool = True):
        self.instrument.enable_source(source) if state else self.instrument.disable_source(source)
        return Response(True, 0, None)

    def get_measurement(self, channel: int = 1, type: str = "CURR", item: str = "FREQ"):
        measurement = self.instrument.get_measurement(item, type, channel)
        return Response(True, 0, measurement)

    def get_full_measurement(self, channel: int = 1, item: str = "FREQ"):
        max = self.instrument.get_measurement(item, "MAX", channel)
        min = self.instrument.get_measurement(item, "MIN", channel)
        curr = self.instrument.get_measurement(item, "CURR", channel)
        aver = self.instrument.get_measurement(item, "AVER", channel)
        dev = self.instrument.get_measurement(item, "DEV", channel)
        return Response(True, 0, {
            "max": max,
            "min": min,
            "curr": curr,
            "aver": aver,
            "dev": dev
        })

    def set_waveform_format(self, format: str = "ASC"):
        self.instrument.set_waveform_format("ASC")
        return Response(True, 0, None)

    def get_waveform_samples(self):
        x, y = self.instrument.get_waveform_samples(channel=2)
        return Response(True, 0, {
            "x": x,
            "y": y
        })
    
