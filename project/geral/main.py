import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from measurement_window import MeasurementWindow
import time
import math
from api_calls import OscilloscopeAPI
#from Measurement import Measurement

class OscilloscopeGUI:
    def __init__(self, master):
        self.master = master
        master.title("Oscilloscope GUI")
        OscilloscopeIP = "0.0.0.0"
        self.api = OscilloscopeAPI(OscilloscopeIP)
        if self.api.get_test() == 0.0:
            print("Connected to API")


        self.velocity_data = []
        self.start_time = time.time()
        

        self.create_widgets()
        self.setup_plot()
        self.update_plot()


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

        """
        style = ttk.Style()
        style.configure('TFrame', background='gray')
        style.configure('TLabel', background='gray', foreground='#FFD700', font=('Helvetica', 10, 'bold'))  # Less bright yellow
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

        # Add IP address and port entry and connect button
        self.ip_label = ttk.Label(self.top_frame, text="Oscilloscope IP and Port:")
        self.ip_label.pack(side="left", padx=5)

        self.ip_entry = ttk.Entry(self.top_frame, width=30, foreground='gray')
        self.ip_entry.insert(0, "123.123.123.123:12345")
        self.ip_entry.bind("<FocusIn>", self.on_entry_click)
        self.ip_entry.bind("<FocusOut>", self.on_focus_out)
        self.ip_entry.pack(side="left", padx=5)

        self.connect_button = ttk.Button(self.top_frame, text="Connect", command=self.connect_to_oscilloscope)
        self.connect_button.pack(side="left", padx=5)

        self.request_waveform_button = ttk.Button(self.top_frame, text="Request Waveform", command=self.request_waveform)
        self.request_waveform_button.pack(side="left", padx=5)

        self.apply_channel_button = ttk.Button(self.right_frame, text="Apply Channel", command=self.update_waveform)
        self.apply_channel_button.pack(pady=5)

        self.channel_label = ttk.Label(self.right_frame, text="Channel Selection")
        self.channel_label.pack(pady=5)

        self.channel_var = tk.StringVar()
        self.channel_combobox = ttk.Combobox(self.right_frame, textvariable=self.channel_var, state="readonly")
        self.channel_combobox['values'] = ("Channel 1", "Channel 2", "Channel 3")
        self.channel_combobox.current(0)
        self.channel_combobox.pack(pady=5)

        self.start_label = ttk.Label(self.right_frame, text="Start Measuring")
        self.start_label.pack(pady=5)

        self.start_button = ttk.Button(self.right_frame, text="Start / Stop", command=self.connect_to_oscilloscope)
        self.start_button.pack(pady=5)

        self.measure_label = ttk.Label(self.right_frame, text="Display Measurements")
        self.measure_label.pack(pady=5)

        self.measure_button = ttk.Button(self.right_frame, text="Measure", command=self.open_measurements)
        self.measure_button.pack(pady=5)

        self.scale_label = ttk.Label(self.right_frame, text="Scale Selection")
        self.scale_label.pack(pady=5)

        self.scale_var = tk.StringVar()
        self.scale_combobox = ttk.Combobox(self.right_frame, textvariable=self.scale_var, state="readonly",
                                           values=("0.01X", "0.02X", "0.05X", "0.1X", "0.2X", "0.5X", "1X", "2X", "5X", "10X", "20X", "50X", "100X", "200X", "500X", "1000X"))
        self.scale_combobox.current(6)
        self.scale_combobox.pack(pady=5)

        self.apply_scale_button = ttk.Button(self.right_frame, text="Apply Scale", command=self.apply_scale)
        self.apply_scale_button.pack(pady=5)

        self.horizontal_scale_label = ttk.Label(self.right_frame, text="Horizontal Scale")
        self.horizontal_scale_label.pack(pady=5)

        self.horizontal_plus_button = ttk.Button(self.right_frame, text="Horizontal+", command=self.increase_horizontal_scale)
        self.horizontal_plus_button.pack(pady=5)

        self.horizontal_minus_button = ttk.Button(self.right_frame, text="Horizontal-", command=self.decrease_horizontal_scale)
        self.horizontal_minus_button.pack(pady=5)

        self.vertical_scale_label = ttk.Label(self.right_frame, text="Vertical Scale")
        self.vertical_scale_label.pack(pady=5)

        self.vertical_plus_button = ttk.Button(self.right_frame, text="Vertical+", command=self.increase_vertical_scale)
        self.vertical_plus_button.pack(pady=5)

        self.vertical_minus_button = ttk.Button(self.right_frame, text="Vertical-", command=self.decrease_vertical_scale)
        self.vertical_minus_button.pack(pady=5)

        self.auto_scale_label = ttk.Label(self.right_frame, text="Automatic Scale")
        self.auto_scale_label.pack(pady=5)

        self.set_offset_button = ttk.Button(self.right_frame, text="Auto Scale", command=self.apply_offset)
        self.set_offset_button.pack(pady=5)

        self.current_offset = 0
        """

    def setup_plot(self):
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title("Real-Time Data")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Velocity")

        self.canvas = FigureCanvasTkAgg(self.figure, self.left_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.line, = self.ax.plot([], [], 'r-')

    def update_plot(self):

        elapsed_time, velocity = self.api.get_test()

        self.velocity_data.append((elapsed_time, velocity))

        # Keep the last 100 points
        self.velocity_data = self.velocity_data[-100:]

        times, values = zip(*self.velocity_data) if self.velocity_data else ([], [])

        self.line.set_data(times, values)

        self.ax.set_xlim(max(0, elapsed_time - 10), elapsed_time)
        self.ax.set_ylim(-1.5, 1.5)

        self.canvas.draw()

        self.master.after(100, self.update_plot)

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