from app.view.dashboard_panel import Dashboard
import tkinter as tk


class MakeModel(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.width, self.height = 500, 400
        tk.Label(self, text="This is the Make Model").pack(pady=10, padx=10)
        tk.Button(self, text="Return to Menu", command=lambda: controller.show_frame("Dashboard")).pack()