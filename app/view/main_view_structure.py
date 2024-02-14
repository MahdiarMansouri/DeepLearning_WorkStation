import tkinter as tk
from dashboard_panel import Dashboard
from make_model_panel import MakeModel
from make_pipeline_panel import MakePipeline
from show_results_panel import ShowResults


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.frames = {}

        # Initialize all frames and store them
        for F in (Dashboard, MakePipeline, MakeModel, ShowResults):
            frame = F(self)
            self.frames[F] = frame
            # The frames are stacked on top of each other
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Dashboard)

    def show_frame(self, context):
        frame = self.frames[context]
        frame.tkraise()
        # Resize the window to fit the frame
        self.geometry(f"{frame.width}x{frame.height}")
