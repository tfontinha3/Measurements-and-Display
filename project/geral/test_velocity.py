import time
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.widgets as widgets
from velocity import Velocity 

class Measurement:
    def __init__(self, get_method):
        
        self.x_data = []
        self.y_data = []
        self.max_x = 0
        #self.fig, self.ax = plt.subplots()
        #self.line, = self.ax.plot([], [], lw=2)
        self.max_length = 300  # Keep last 300 data points

        #self.button = widgets.Button(plt.axes([0.81, 0.05, 0.1, 0.075]), 'Reset Experiment')
        #self.button.on_clicked(self.reset_experiment)

    def reset_experiment(self, event):
        self.x_data.clear()
        self.y_data.clear()
        self.ax.set_xlim(0, 30)  # Reset x-axis limit
        self.ax.set_ylim(-100, 100) #aqui o limite de altura

    def animate(self):

        velocity_data = self.get_method
        #passar json para data
        
        if velocity_data:
            for pair in velocity_data:
                x, y = map(float, pair)
                seconds = x / 1000  
                if seconds > self.max_x:

                    self.x_data.append(seconds)
                    self.y_data.append(y)
                    self.max_x = seconds

            # Limit data to keep memory usage low
            if len(self.x_data) > self.max_length:
                self.x_data = self.x_data[-self.max_length:]
                self.y_data = self.y_data[-self.max_length:]

            self.line.set_data(self.x_data, self.y_data)
            self.ax.set_xlim(min(self.x_data), max(self.x_data) + 10)
            self.ax.relim()
            self.ax.autoscale_view()

    def run(self):
        anim = FuncAnimation(self.fig, self.animate, frames=None, interval=100, repeat=False)
        plt.show()

def main():
    local_ip = "192.168.124.59"
    local_port = 4210 
    velocity = Velocity(local_ip, local_port)
    print("Created Velocity object")
    while True:
        velocity_data = velocity.get_data()
        print(velocity_data)
        time.sleep(1)
    
    

if __name__ == "__main__":
    main()
