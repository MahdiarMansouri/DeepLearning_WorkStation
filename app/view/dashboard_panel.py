import tkinter as tk
from make_pipeline_panel import MakePipeline
from make_model_panel import MakeModel
from show_results_panel import ShowResults


class Dashboard(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.width, self.height = 300, 200  # Preferred size for the MenuPage
        tk.Label(self, text="Main Menu").pack(pady=10, padx=10)
        tk.Button(self, text="Go to Make Model", command=lambda: parent.show_frame(MakeModel)).pack()
        tk.Button(self, text="Go to Make Pipeline", command=lambda: parent.show_frame(MakePipeline)).pack()
        tk.Button(self, text="Go to Show Results", command=lambda: parent.show_frame(ShowResults)).pack()
