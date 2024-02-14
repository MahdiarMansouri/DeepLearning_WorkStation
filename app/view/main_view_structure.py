import tkinter as tk
from dashboard_panel import Dashboard
from make_model_panel import MakeModel
from make_pipeline_panel import MakePipeline
from show_results_panel import ShowResults


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.frames = {}
        self.init_frames()

    def init_frames(self):
        for F in (Dashboard, MakePipeline, MakeModel, ShowResults):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("Dashboard")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        self.geometry(f"{frame.width}x{frame.height}")

if __name__ == "__main__":
    app = App()
    app.mainloop()
