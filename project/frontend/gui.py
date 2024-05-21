import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import requests

class MeasurementWindow:
    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.top.title("Measurements")

        measurement_options = [
            "VMAX", "VMIN", "VTOP", "VBAS", "VAMP", "VAVG", "VRMS", "OVER", "PRES",
            "MAR", "MPAR", "PER", "FREQ", "RTIM", "FTIM", "PWID", "NWID", "PDUT",
            "NDUT", "RDEL", "FDEL", "RPH", "FPH"
        ]

        self.measurements_listbox = tk.Listbox(self.top, selectmode='multiple', exportselection=0)
        for item in measurement_options:
            self.measurements_listbox.insert(tk.END, item)
        self.measurements_listbox.pack(side="left", fill="y")

        self.show_table_button = tk.Button(self.top, text="Show Table", command=self.show_table)
        self.show_table_button.pack(side="left")

        self.tree = None

    def show_table(self):
        if self.tree is not None:
            self.tree.destroy()

        selected_indices = self.measurements_listbox.curselection()
        selected_measurements = [self.measurements_listbox.get(i) for i in selected_indices]

        self.tree = ttk.Treeview(self.top, columns=("NAME", "MAX", "MIN", "CURR", "AVER", "DEV"), show="headings")

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)

        for measurement in selected_measurements:
            self.tree.insert("", "end", values=(measurement, 0, 0, 0, 0, 0))

        self.tree.pack(side="right", fill="both", expand=True)

class OscilloscopeGUI:
    def __init__(self, master):
        self.master = master
        master.title("Simplified Oscilloscope")
        
        self.create_widgets()

    def create_widgets(self):
        self.left_frame = tk.Frame(self.master, bg="white")
        self.right_frame = tk.Frame(self.master, bg="lightgrey")
        self.left_frame.grid(row=0, column=0, sticky="nsew")
        self.right_frame.grid(row=0, column=1, sticky="ns")

        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=0)
        self.master.grid_rowconfigure(0, weight=1)

        self.fig = Figure(figsize=(5, 3), dpi=100)
        self.ax = self.fig.add_subplot(111)
        
        self.x = np.linspace(0, 2*np.pi, 100)
        self.y = np.sin(self.x)
        self.line, = self.ax.plot(self.x, self.y, 'r')

        self.canvas = FigureCanvasTkAgg(self.fig, self.left_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

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

        self.trigger_label = ttk.Label(self.right_frame, text="Trigger Value:")
        self.trigger_label.pack(pady=5)

        self.trigger_value = tk.StringVar()
        self.trigger_entry = ttk.Entry(self.right_frame, textvariable=self.trigger_value)
        self.trigger_entry.pack(pady=5)

        self.apply_trigger_button = ttk.Button(self.right_frame, text="Apply Trigger", command=self.apply_trigger)
        self.apply_trigger_button.pack(pady=5)

        self.set_offset_button = ttk.Button(self.right_frame, text="Auto Scale", command=self.apply_offset)
        self.set_offset_button.pack(pady=5)

        self.current_offset = 0

    def connect_to_oscilloscope(self):
        URL = "http://CTR208:29700/api/oscilloscope"
        r = requests.post(url = URL)
        data = r.json()
        print(data)

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
        self.ax.set_ylim(y_center - y_range / 2, y_center + y_range / 2)

        self.canvas.draw()

    def apply_offset(self):
        offset = self.current_offset
        adjusted_y = self.y + offset
        self.ax.clear()
        self.ax.plot(self.x, adjusted_y, 'r')
        self.ax.figure.canvas.draw()

    def increase_horizontal_scale(self):
        xlim = self.ax.get_xlim()
        self.ax.set_xlim([xlim[0], xlim[1] * 1.2])
        self.canvas.draw()

    def decrease_horizontal_scale(self):
        xlim = self.ax.get_xlim()
        self.ax.set_xlim([xlim[0], xlim[1] * 0.8333])
        self.canvas.draw()

    def increase_vertical_scale(self):
        ylim = self.ax.get_ylim()
        new_range = max(abs(ylim[0]), abs(ylim[1])) * 1.2
        self.ax.set_ylim(-new_range, new_range)
        self.canvas.draw()

    def decrease_vertical_scale(self):  
        ylim = self.ax.get_ylim()
        new_range = max(abs(ylim[0]), abs(ylim[1])) * 0.8333
        self.ax.set_ylim(-new_range, new_range)
        self.canvas.draw()

    def update_waveform(self):
        channel = self.channel_var.get()
        if channel == "Channel 1":
            self.y = np.sin(self.x)
        elif channel == "Channel 2":
            self.y = np.cos(self.x)
        elif channel == "Channel 3":
            self.y = np.abs(np.sin(self.x))

        self.line.set_ydata(self.y)
        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas.draw()

    def open_measurements(self):
        self.measurement_window = MeasurementWindow(self.master)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('800x600')
    gui = OscilloscopeGUI(root)
    root.mainloop()
