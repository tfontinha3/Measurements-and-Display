import tkinter as tk
from tkinter import ttk

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
