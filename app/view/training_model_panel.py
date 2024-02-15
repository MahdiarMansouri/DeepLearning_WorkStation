import tkinter as tk
from tkinter import ttk

from app.models.db_models.database_model import ModelDA
from app.models.dl_models.dl_models import Result


class TrainingModel(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.width, self.height = 2500, 500
        tk.Label(self, text="This is the training pipelines").grid(row=0, column=0, padx=10, pady=10)

        self.pipeline_treeview = ttk.Treeview(self, columns=(
            'Data Path', 'Batch Size', 'Feature Method', 'Model Name', 'Pretrained', 'Epoch Numbers', 'Optimizer',
            'Loss Function', 'Learning Rate'), show='headings')
        self.pipeline_treeview.heading('Data Path', text='Data Path')
        self.pipeline_treeview.heading('Batch Size', text='Batch Size')
        self.pipeline_treeview.heading('Feature Method', text='Feature Method')
        self.pipeline_treeview.heading('Model Name', text='Model Name')
        self.pipeline_treeview.heading('Pretrained', text='Pretrained')
        self.pipeline_treeview.heading('Epoch Numbers', text='Epoch Numbers')
        self.pipeline_treeview.heading('Optimizer', text='Optimizer')
        self.pipeline_treeview.heading('Loss Function', text='Loss Function')
        self.pipeline_treeview.heading('Learning Rate', text='Learning Rate')
        self.pipeline_treeview.grid(row=0, column=0, rowspan=10, columnspan=7, sticky='nsew', padx=10, pady=5)

        tk.Button(self, text="Menu", command=lambda: controller.show_frame("Dashboard")).grid(row=10, column=0, pady=10)
        tk.Button(self, text="Show Results", command=lambda: controller.show_frame("ShowResults")).grid(row=10, column=1,
                                                                                                        pady=10)

    def update_pipelines(self, pipelines_values, pipelines):
        # self.pipeline_treeview.delete(0, tk.END)
        for pipeline_value in pipelines_values:
            print('pipeline value is: ', pipeline_value)
            self.pipeline_treeview.insert('', tk.END, pipeline_value)

        for idx, pipeline in enumerate(pipelines):
            print(f'running pipeline {idx + 1}')
            print('pipeline is: ', pipeline)
            print('running process start ...')
            pipeline.run()
            result = pipeline.get_results()
            model_da = ModelDA()
            model_da.add_model_result(result)
            print('results saved to database...')
