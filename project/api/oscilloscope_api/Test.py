import sys
#from Oscilloscope import Oscilloscope
from instruments import DS1000Z

import matplotlib.pyplot as plt

class Oscilloscope:
    def __init__(self, hostname):
        self.hostname = hostname

    def connect(self):
        self.instrument = DS1000Z(self.hostname)
        self.idn = self.instrument.get_identification()

    def select_probe(self, channel, probe: int):
        self.instrument.set_probe_ratio(probe, channel)

    def get_probe(self, channel):
        self.instrument.get_probe_ratio(channel)

    def show_only_selected_channel(self, channel: int):
        for i in range(1, 4):
            if i == channel:
                self.instrument.show_channel(i)
            else:
                self.instrument.hide_channel(i)

    def get_sample_rate(self):
        self.current_sample_rate = self.instrument.get_sample_rate()
        return self.current_sample_rate
    
    def autoscale(self):
        self.instrument.autoscale()
        self.is_autoscale = True

    def clear_screen(self):
        self.instrument.clear()

    def run(self, run: bool = True):
        self.instrument.run() if run else self.instrument.stop()

    def get_channel_coupling(self, channel: int = 1):
        return self.instrument.get_channel_coupling(channel)
    
    def set_channel_coupling(self, channel: int = 1, coupling: str = "DC"):
        if coupling not in ["AC", "DC", "GND"]:
            return "Invalid coupling mode. Availables: DC, AC, DND"
        return self.instrument.set_channel_coupling(channel)

    def get_channel_offset(self, channel: int = 1):
        self.offset = self.instrument.get_channel_offset(channel)
        return self.offset
    
    def set_channel_offset(self, channel: int = 1, offset: float = 0):
        self.offset = self.instrument.set_channel_offset(offset, channel)

    def get_channel_vrange(self, channel: int = 1):
        self.range = self.instrument.get_channel_range(channel)
        return self.range
    
    def set_channel_vrange(self, channel: int = 1, range: float = 8):
        self.offset = self.instrument.set_channel_range(range, channel)

    def reset(self):
        self.instrument.reset()

    def enable_source(self, source: int = 1, state: bool = True):
        self.instrument.enable_source(source) if state else self.instrument.disable_source(source)

    def get_measurement(self, channel: int = 1, type: str = "CURR", item: str = "FREQ"):
        return self.instrument.get_measurement(item, type, channel)

    def get_full_measurement(self, channel: int = 1, item: str = "FREQ"):
        max = self.instrument.get_measurement(item, "MAX", channel)
        min = self.instrument.get_measurement(item, "MIN", channel)
        curr = self.instrument.get_measurement(item, "CURR", channel)
        aver = self.instrument.get_measurement(item, "AVER", channel)
        dev = self.instrument.get_measurement(item, "DEV", channel)
        return {
            "max": max,
            "min": min,
            "curr": curr,
            "aver": aver,
            "dev": dev
        }

    def set_waveform_format(self, format: str = "ASC"):
        self.instrument.set_waveform_format("ASC")

    def get_waveform_samples(self):
        return self.instrument.get_waveform_samples()

    def set_trigger_level(self, channel: int = 1, level: float = 1):
        self.instrument.set_trigger_level(level, channel)

    def set_trigger_mode(self, mode: str = "EDGE"):
        self.instrument.set_trigger_mode(mode)

    def set_trigger_coupling(self, coupling: str = "DC"):
        self.instrument.set_trigger_coupling(coupling)

    def set_trigger_sweep(self, mode: str = "AUTO"):
        self.instrument.set_trigger_sweep(mode)

    def set_trigger_holdoff(self, time: float = 16e-9):
        self.instrument.set_trigger_holdoff(time)

    def set_trigger_source(self, channel: int = 1):
        self.instrument.set_trigger_source(channel)

    def set_trigger_direction(self, direction: str = "POS"):
        self.instrument.set_trigger_direction(direction)

    def set_trigger_condition(self, condition: str):
        self.instrument.set_trigger_comdition(condition)

    def configure_trigger(self):

        pass


HOSTNAME = "192.168.1.10"

if __name__ == "__main__":

    instrument = Oscilloscope(HOSTNAME)
    idn = instrument.connect()
    print(idn)

    instrument.select_probe(1, 1)
    instrument.show_only_selected_channel(1)
    sample_rate = instrument.get_sample_rate()
    #instrument.set_trigger_level(0.1)
    #instrument.set_trigger_level(1, 2)
    print(sample_rate)
    print(instrument.get_measurement(1, "MAX", "VMAX"))
    print(instrument.get_full_measurement(1, "VMAX"))
    offset = instrument.set_channel_offset(1, 0.01)
    instrument.set_waveform_format("ASC")

    x,y = instrument.get_waveform_samples()

    plt.plot(x,y)
    plt.show()

    """
    instrument.autoscale()
    instrument.clear_screen()
    instrument.run(True)
    coupling_mode = instrument.get_channel_coupling()
    print(coupling_mode)

    offset = instrument.get_channel_offset(1)
    print(offset)
    offset = instrument.set_channel_offset(1, 0)
    offset = instrument.get_channel_offset(1)
    print(offset)

    range = instrument.get_channel_vrange(1)
    print(range)
    range = instrument.set_channel_vrange(1, 0.16)
    range = instrument.get_channel_vrange(1)
    print(range)

    meas = instrument.get_full_measurement(1, "VAVG")
    print(meas)
    """
    sys.exit(0)