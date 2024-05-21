import time
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.widgets as widgets
from api_calls import OscilloscopeAPI

class Measurement:
    def __init__(self, get_method):
        self.get_method = get_method
        self.data = []

    def update(self):
        new_data = self.get_method()
        self.data.extend(new_data)
        return self.data

if __name__ == "__main__":
    oscilloscope = OscilloscopeAPI("0.0.0.0")
    velocity = Measurement(oscilloscope.get_velocity)
    while True : 
        velocity.update()
        print(velocity.data)

