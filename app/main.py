import tkinter as tk

from app.view.training_model_panel import TrainingModel
from view.dashboard_panel import Dashboard
from view.make_model_panel import MakeModel
from view.make_pipeline_panel import MakePipeline
from view.show_results_panel import ShowResults


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.frames = {}
        self.pipelines = []
        self.pipelines_values = []
        self.title("DeepLearning WorkStation")
        self.init_frames()

    def init_frames(self):
        for F in (Dashboard, MakePipeline, MakeModel, ShowResults, TrainingModel):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("Dashboard")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        self.geometry(f"{frame.width}x{frame.height}")
        if page_name == "TrainingModel":
            frame.update_pipelines(self.pipelines_values, self.pipelines)


if __name__ == "__main__":
    app = App()
    app.mainloop()
