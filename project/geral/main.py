import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from measurement_window import MeasurementWindow
import time
import math
from api_calls import OscilloscopeAPI

class OscilloscopeGUI:
    def __init__(self, master):
        self.master = master
        master.title("Oscilloscope GUI")
        OscilloscopeIP = "0.0.0.0"
        self.api = OscilloscopeAPI(OscilloscopeIP)
        if self.api.get_test() == 0.0:
            print("Connected to API")

        self.velocity_data = []
        self.voltage_data = []
        self.current_data = []
        self.start_time = time.time()
        
        self.create_widgets()
        self.setup_plots()
        self.update_velocity_plot()
        self.update_voltage_plot()
        self.update_current_plot()

    def create_widgets(self):
        style = ttk.Style()
        style.configure('TFrame', background='gray')
        style.configure('TLabel', background='gray', foreground='#FFD700', font=('Helvetica', 10, 'bold'))
        style.configure('TButton', background='#FFD700', foreground='black', font=('Helvetica', 10, 'bold'))
        style.configure('TEntry', fieldbackground='gray', foreground='white')

        self.master.configure(background='gray')

        self.top_frame = ttk.Frame(self.master, style='TFrame')
        self.top_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

        self.left_frame = ttk.Frame(self.master, style='TFrame')
        self.right_frame = ttk.Frame(self.master, style='TFrame')
        self.left_frame.grid(row=1, column=0, sticky="nsew")
        self.right_frame.grid(row=1, column=1, sticky="ns")

        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=0)
        self.master.grid_rowconfigure(1, weight=1)

        self.ip_label = ttk.Label(self.top_frame, text="Oscilloscope IP and Port:")
        self.ip_label.pack(side="left", padx=5)

        self.ip_entry = ttk.Entry(self.top_frame, width=30, foreground='gray')
        self.ip_entry.insert(0, "123.123.123.123:12345")
        self.ip_entry.bind("<FocusIn>", self.on_entry_click)
        self.ip_entry.bind("<FocusOut>", self.on_focus_out)
        self.ip_entry.pack(side="left", padx=5)

        self.connect_button = ttk.Button(self.top_frame, text="Connect", command=self.connect_to_oscilloscope)
        self.connect_button.pack(side="left", padx=5)

    def setup_plots(self):
        self.figure_velocity = Figure(figsize=(5, 2), dpi=100)
        self.ax_velocity = self.figure_velocity.add_subplot(111)
        self.ax_velocity.set_title("Real-Time Velocity Data")
        self.ax_velocity.set_xlabel("Time (s)")
        self.ax_velocity.set_ylabel("Velocity")

        self.canvas_velocity = FigureCanvasTkAgg(self.figure_velocity, self.left_frame)
        self.canvas_velocity.draw()
        self.canvas_velocity.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.line_velocity, = self.ax_velocity.plot([], [], 'r-')

        self.figure_voltage = Figure(figsize=(5, 2), dpi=100)
        self.ax_voltage = self.figure_voltage.add_subplot(111)
        self.ax_voltage.set_title("Real-Time Voltage Data")
        self.ax_voltage.set_xlabel("Time (s)")
        self.ax_voltage.set_ylabel("Voltage")

        self.canvas_voltage = FigureCanvasTkAgg(self.figure_voltage, self.left_frame)
        self.canvas_voltage.draw()
        self.canvas_voltage.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.line_voltage, = self.ax_voltage.plot([], [], 'b-')

        self.figure_current = Figure(figsize=(5, 2), dpi=100)
        self.ax_current = self.figure_current.add_subplot(111)
        self.ax_current.set_title("Real-Time Current Data")
        self.ax_current.set_xlabel("Time (s)")
        self.ax_current.set_ylabel("Current")

        self.canvas_current = FigureCanvasTkAgg(self.figure_current, self.left_frame)
        self.canvas_current.draw()
        self.canvas_current.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.line_current, = self.ax_current.plot([], [], 'g-')

    def update_velocity_plot(self):
        get_values = self.api.get_velocity()
        print(get_values)
        
        # Append new values to the velocity_data list
        self.velocity_data.extend(get_values)

        # Remove duplicate points based on the same timestamp
        unique_data = {time: value for time, value in self.velocity_data}

        # Convert back to a list of tuples
        self.velocity_data = list(unique_data.items())

        # Sort by time to maintain the correct order
        self.velocity_data.sort()

        # Keep the last 100 points
        self.velocity_data = self.velocity_data[-100:]

        if self.velocity_data:
            times = [point[0] for point in self.velocity_data]
            values = [point[1] for point in self.velocity_data]

            self.line_velocity.set_data(times, values)

            self.ax_velocity.set_xlim(min(times), max(times) if max(times) - min(times) > 30 else (min(times) + 30))
            self.ax_velocity.set_ylim(min(values) - 1, max(values) + 1)

            self.canvas_velocity.draw()

        self.master.after(100, self.update_velocity_plot)

    def update_voltage_plot(self):
        get_values = self.api.get_test()
        print(get_values)
        
        # Append new values to the voltage_data list
        self.voltage_data.extend(get_values)

        # Remove duplicate points based on the same timestamp
        unique_data = {time: value for time, value in self.voltage_data}

        # Convert back to a list of tuples
        self.voltage_data = list(unique_data.items())

        # Sort by time to maintain the correct order
        self.voltage_data.sort()

        # Keep the last 100 points
        self.voltage_data = self.voltage_data[-100:]

        if self.voltage_data:
            times = [point[0] for point in self.voltage_data]
            values = [point[1] for point in self.voltage_data]

            self.line_voltage.set_data(times, values)

            self.ax_voltage.set_xlim(min(times), max(times) if max(times) - min(times) > 30 else (min(times) + 30))
            self.ax_voltage.set_ylim(min(values) - 1, max(values) + 1)

            self.canvas_voltage.draw()

        self.master.after(100, self.update_voltage_plot)

    def update_current_plot(self):
        get_values = self.api.get_test()
        print(get_values)
        
        # Append new values to the current_data list
        self.current_data.extend(get_values)

        # Remove duplicate points based on the same timestamp
        unique_data = {time: value for time, value in self.current_data}

        # Convert back to a list of tuples
        self.current_data = list(unique_data.items())

        # Sort by time to maintain the correct order
        self.current_data.sort()

        # Keep the last 100 points
        self.current_data = self.current_data[-100:]

        if self.current_data:
            times = [point[0] for point in self.current_data]
            values = [point[1] for point in self.current_data]

            self.line_current.set_data(times, values)

            self.ax_current.set_xlim(min(times), max(times) if max(times) - min(times) > 30 else (min(times) + 30))
            self.ax_current.set_ylim(min(values) - 1, max(values) + 1)

            self.canvas_current.draw()

        self.master.after(100, self.update_current_plot)



    def on_entry_click(self, event):
        if self.ip_entry.get() == "123.123.123.123:12345":
            self.ip_entry.delete(0, "end")  
            self.ip_entry.insert(0, "")
            self.ip_entry.config(foreground='white')

    def on_focus_out(self, event):
        if self.ip_entry.get() == "":
            self.ip_entry.insert(0, "123.123.123.123:12345")
            self.ip_entry.config(foreground='gray')

    def connect_to_oscilloscope(self):
        ip_address = self.ip_entry.get()
        self.api.set_base_url(ip_address)
        data = self.api.connect_to_oscilloscope()
        print(data)

    def request_waveform(self):
        data = self.api.get_waveform()
        if data:
            self.x = data["x"]
            self.y = data["y"]
            self.update_plot()

    def apply_trigger(self):
        trigger_value = float(self.trigger_value.get())
        print("Trigger applied at:", trigger_value)

    def apply_scale(self):
        scale_factor_str = self.scale_var.get()
        scale_factor = float(scale_factor_str.strip('X'))

        x_center = np.mean(self.ax.get_xlim())
        x_range = 3.14 / scale_factor
        self.ax.set_xlim(x_center - x_range / 2, x_center + x_range / 2)

        y_center = np.mean(self.ax.get_ylim())
        y_range = 1 / scale_factor
        self.ax.set_ylim(y_center - y_range / 2, y_range / 2)

        self.measurement_canvas.draw()

    def apply_offset(self):
        offset = self.current_offset
        adjusted_y = self.y + offset
        self.ax.clear()
        self.ax.plot(self.x, adjusted_y, '#FFD700')
        self.ax.figure.canvas.draw()

    def increase_horizontal_scale(self):
        xlim = self.ax.get_xlim()
        self.ax.set_xlim([xlim[0], xlim[1] * 1.2])
        self.measurement_canvas.draw()

    def decrease_horizontal_scale(self):
        xlim = self.ax.get_xlim()
        self.ax.set_xlim([xlim[0], xlim[1] * 0.8333])
        self.measurement_canvas.draw()

    def increase_vertical_scale(self):
        ylim = self.ax.get_ylim()
        new_range = max(abs(ylim[0]), abs(ylim[1])) * 1.2
        self.ax.set_ylim(-new_range, new_range)
        self.measurement_canvas.draw()

    def decrease_vertical_scale(self):
        ylim = self.ax.get_ylim()
        new_range = max(abs(ylim[0]), abs(ylim[1])) * 0.8333
        self.ax.set_ylim(-new_range, new_range)
        self.measurement_canvas.draw()


    def update_waveform(self):
        channel = self.channel_var.get()
        if channel == "Channel 1":
            data = self.api.get_waveform()
            print("data:", data)
            self.y = data["y"]
            self.x = data["x"]
        elif channel == "Channel 2":
            self.y = np.cos(self.x)
        elif channel == "Channel 3":
            self.y = np.abs(np.sin(self.x))

        self.line.set_ydata(self.y)
        self.ax.relim()
        self.ax.autoscale_view()
        self.measurement_canvas.draw()

    def open_measurements(self):
        self.measurement_window = MeasurementWindow(self.master)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('1000x700')
    gui = OscilloscopeGUI(root)
    root.mainloop()

"""
    
"""