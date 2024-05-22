import vxi11
from PIL import Image
import pyvisa
import time

class DS1104Z:
    def __init__(self, visa_resource_name: str):
        rm = pyvisa.ResourceManager()
        self.instr = rm.open_resource(visa_resource_name)
        if self.get_equipment_idn() is None:
            print("Invalid Instrument.")

    def get_equipment_idn(self):
        try:
            self.idn = self.instr.query("*IDN?")
            return self.idn
        except Exception as ex:
            print("Error: Cannot obtain equipment IDN.")
            return None

    def read_digital_waveform(self, timeout: int = 10000):
        self.instr.write(":RUN")
        time.sleep(2)
        self.instr.write(":WAV:DATA? DIG")

    def acquire_waveform(self, continuous: bool = True, timebase: float = 5e-6, timeout: int = 10000):
        if continuous:
            self.set_timebase(timebase, 0)
            self.read_digital_waveform(timeout)
