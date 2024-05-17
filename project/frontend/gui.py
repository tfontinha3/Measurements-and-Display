import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
# importing the requests library
import requests
 
# api-endpoint

class MeasurementWindow:
    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.top.title("Measurements")

        # List of measurements to choose from
        measurement_options = [
            "VMAX", "VMIN", "VTOP", "VBAS", "VAMP", "VAVG", "VRMS", "OVER", "PRES",
            "MAR", "MPAR", "PER", "FREQ", "RTIM", "FTIM", "PWID", "NWID", "PDUT",
            "NDUT", "RDEL", "FDEL", "RPH", "FPH"
        ]

        self.measurements_listbox = tk.Listbox(self.top, selectmode='multiple', exportselection=0)
        for item in measurement_options:
            self.measurements_listbox.insert(tk.END, item)
        self.measurements_listbox.pack(side="left", fill="y")

        # Button to confirm selection and show table
        self.show_table_button = tk.Button(self.top, text="Show Table", command=self.show_table)
        self.show_table_button.pack(side="left")

        self.tree = None  # Placeholder for the Treeview table

    def show_table(self):
        # Destroy previous treeview if it exists
        if self.tree is not None:
            self.tree.destroy()

        # Get selected measurements
        selected_indices = self.measurements_listbox.curselection()
        selected_measurements = [self.measurements_listbox.get(i) for i in selected_indices]

        # Create the Treeview table
        self.tree = ttk.Treeview(self.top, columns=("NAME", "MAX", "MIN", "CURR", "AVER", "DEV"), show="headings")
        
        # Define the column headings
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)

        # Insert data into the table (dummy data for demonstration)
        for measurement in selected_measurements:
            self.tree.insert("", "end", values=(measurement, 0, 0, 0, 0, 0))  # Replace 0's with real data
        
        self.tree.pack(side="right", fill="both", expand=True)

class OscilloscopeGUI:
    def __init__(self, master):
        self.master = master
        master.title("Simplified Oscilloscope")
        
        # Define the left and right frames
        self.left_frame = tk.Frame(master)
        self.right_frame = tk.Frame(master)
        self.left_frame.grid(row=0, column=0, sticky="nsew")
        self.right_frame.grid(row=0, column=1, sticky="ns")

        # Configure the grid layout to give certain weight to left and right frames
        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=0)
        master.grid_rowconfigure(0, weight=1)

        # Create a figure for plotting in the left frame
        self.fig = Figure(figsize=(5, 3), dpi=100)
        self.ax = self.fig.add_subplot(111)
        
        # Plot initial data
        #self.x = np.linspace(0, 2*np.pi, 100)
        #self.y = np.sin(self.x)  # Default channel 1 waveform
        #self.line, = self.ax.plot(self.x, self.y, 'r')

        # Embed the plot in the tkinter window
        self.canvas = FigureCanvasTkAgg(self.fig, self.left_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

        # Add buttons and entry widgets to the right frame
        
        self.start_button = ttk.Button(self.right_frame, text="Start / Stop", command=self.connect_to_oscilloscope)
        self.start_button.pack()

        # Label for channel selection
        self.channel_label = ttk.Label(self.right_frame, text="Channel Selection")
        self.channel_label.pack()
        # Scrolling selection for channels using ttk.Combobox
        self.channel_var = tk.StringVar()
        self.channel_combobox = ttk.Combobox(self.right_frame, textvariable=self.channel_var, state="readonly")
        self.channel_combobox['values'] = ("Channel 1", "Channel 2", "Channel 3")
        self.channel_combobox.current(0)  # set selection to Channel 1
        self.channel_combobox.pack()

        # Button to apply the selected channel and update the waveform
        self.apply_channel_button = ttk.Button(self.right_frame, text="Apply Channel", command=self.update_waveform)
        self.apply_channel_button.pack()

        self.measure_label = ttk.Label(self.right_frame, text="Display Measurements")
        self.measure_label.pack()

        self.measure_button = ttk.Button(self.right_frame, text="Measure", command=self.open_measurements)
        self.measure_button.pack()

        self.scale_label = ttk.Label(self.right_frame, text="Scale Selection")
        self.scale_label.pack()

        self.scale_var = tk.StringVar()
        self.scale_combobox = ttk.Combobox(self.right_frame, textvariable=self.scale_var, state="readonly", values=("0.01X", "0.02X", "0.05X", "0.1X", "0.2X", "0.5X", "1X", "2X", "5X", "10X","20X","50X","100X","200X","500X","1000X"))
        self.scale_combobox.current(6)  # Default scale (x1)
        self.scale_combobox.pack()

                # Button to apply scale
        self.apply_scale_button = ttk.Button(self.right_frame, text="Apply Scale", command=self.apply_scale)
        self.apply_scale_button.pack()

        self.scale_label = ttk.Label(self.right_frame, text="Horizontal Scale")
        self.scale_label.pack()

        self.horizontal_plus_button = ttk.Button(self.right_frame, text="Horizontal+", command=self.increase_horizontal_scale)
        self.horizontal_plus_button.pack()

        self.horizontal_minus_button = ttk.Button(self.right_frame, text="Horizontal-", command=self.decrease_horizontal_scale)
        self.horizontal_minus_button.pack()

        self.scale_label = ttk.Label(self.right_frame, text="Vertical Scale")
        self.scale_label.pack()

        self.vertical_plus_button = ttk.Button(self.right_frame, text="Vertical+", command=self.increase_vertical_scale)
        self.vertical_plus_button.pack()

        self.vertical_minus_button = ttk.Button(self.right_frame, text="Vertical-", command=self.decrease_vertical_scale)
        self.vertical_minus_button.pack()

        self.trigger_label = ttk.Label(self.right_frame, text="Trigger Value:")
        self.trigger_label.pack()

        self.trigger_value = tk.StringVar()
        self.trigger_entry = ttk.Entry(self.right_frame, textvariable=self.trigger_value)
        self.trigger_entry.pack()

        # Button to apply the trigger
        self.apply_trigger_button = ttk.Button(self.right_frame, text="Apply Trigger", command=self.apply_trigger)
        self.apply_trigger_button.pack()

        # Entry and button for setting the y-axis offset
        self.offset_var = tk.DoubleVar()
        self.offset_entry = ttk.Entry(self.right_frame, textvariable=self.offset_var)
        self.offset_entry.pack()
        self.set_offset_button = ttk.Button(self.right_frame, text="Set Offset", command=self.apply_offset)
        self.set_offset_button.pack()

        # Variable to store the current y-offset
        self.current_offset = 0


    def connect_to_oscilloscope(self):
        URL = "http://CTR208:29700/api/oscilloscope"
        r = requests.post(url = URL)
        return r.json()

    def get_waveform(self):
        URL = "http://CTR208:29700/api/oscilloscope/waveform"
        r = requests.get(url = URL)
        return r.json()

    def apply_trigger(self):
        # Apply the trigger logic
        trigger_value = float(self.trigger_value.get())  # Convert input to float, handle exceptions as needed
        # Implement the triggering logic here
        print("Trigger applied at:", trigger_value)  # Placeholder for actual triggering logic
        pass
    
    def apply_scale(self):
        # Apply the selected scale factor
        scale_factor_str = self.scale_var.get()
        scale_factor = float(scale_factor_str.strip('X'))  # Remove the 'X' and convert to float

        # Set new limits based on the scale factor
        x_center = np.mean(self.ax.get_xlim())
        x_range = 3.14 / scale_factor  # Adjust the x range around the center point
        self.ax.set_xlim(x_center - x_range / 2, x_center + x_range / 2)

        y_center = np.mean(self.ax.get_ylim())
        y_range = 1/scale_factor  # Adjust the y range around the center point
        self.ax.set_ylim(y_center - y_range / 2, y_center + y_range / 2)

        self.canvas.draw()  # Redraw the canvas with the new limits

    def apply_offset(self):
        # Adjust all y-values by the offset and redraw the graph
        offset = self.offset_var.get()
        adjusted_y = self.y + offset  # Add the offset to the original y-data
        self.ax.clear()  # Clear the existing plot
        self.ax.plot(self.x, adjusted_y, 'r')  # Plot the new data with the offset
        self.ax.figure.canvas.draw()  # Redraw the canvas

    def increase_horizontal_scale(self):
        xlim = self.ax.get_xlim()
        self.ax.set_xlim([xlim[0], xlim[1] * 1.2])  # Increase x-axis range
        self.canvas.draw()

    def decrease_horizontal_scale(self):
        xlim = self.ax.get_xlim()
        self.ax.set_xlim([xlim[0], xlim[1] * 0.8333])  # Decrease x-axis range
        self.canvas.draw()

    def increase_vertical_scale(self):
        ylim = self.ax.get_ylim()
        self.ax.set_ylim([ylim[0], ylim[1] * 1.2])  # Increase y-axis range
        self.canvas.draw()

    def decrease_vertical_scale(self):
        ylim = self.ax.get_ylim()
        self.ax.set_ylim([ylim[0], ylim[1] * 0.8333])  # Decrease y-axis range
        self.canvas.draw()

    def update_plot(self):
        # Redraw the plot with the current offset applied
        self.ax.clear()
        self.ax.plot(self.x, self.y + self.current_offset, 'r')
        self.canvas.draw()

    def update_waveform(self):
        # Update the waveform based on the selected channel
        channel = self.channel_var.get()
        if channel == "Channel 1":
            #self.y = np.sin(self.x)  # Sine wave for Channel 1
            data = dict(self.get_waveform())
            print("data:", data)
            self.y = data["y"]
            self.x = data["x"]
            #print(len(self.x), len(self.y))

        elif channel == "Channel 2":
            self.y = np.cos(self.x)  # Cosine wave for Channel 2
        elif channel == "Channel 3":
            self.y = np.abs(np.sin(self.x))  # Absolute sine wave for Channel 3

        self.line, = self.ax.plot(self.x, self.y, 'r')
        self.line.set_ydata(self.y)  # Set new y-data for the plot
        self.ax.relim()  # Recalculate limits
        self.ax.autoscale_view()  # Autoscale view
        self.canvas.draw()  # Redraw the canvas
    
    def open_measurements(self):
        # Open a new window with measurement details
        self.measurement_window = MeasurementWindow(self.master)

    def toggle_start(self):
        # Start/stop the data update
        pass

    def trigger_apply(self):
        # Set horizontal trigger
        pass

    def update_plot(self):
        # Update the plot with new data
        pass

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('800x600')  # You can specify the initial window size
    gui = OscilloscopeGUI(root)
    root.mainloop()

