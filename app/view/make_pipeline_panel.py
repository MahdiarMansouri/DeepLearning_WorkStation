import tkinter as tk

from dashboard_panel import Dashboard


class MakePipeline(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.width, self.height = 400, 300
        tk.Label(self, text="This is the Make Pipeline").pack(pady=10, padx=10)
        tk.Button(self, text="Return to Dashboard", command=lambda: controller.show_frame("Dashboard")).pack()
