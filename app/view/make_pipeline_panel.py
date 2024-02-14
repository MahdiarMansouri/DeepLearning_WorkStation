# import tkinter as tk
#
# from dashboard_panel import Dashboard
#
#
# class MakePipeline(tk.Frame):
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         self.width, self.height = 400, 300
#         tk.Label(self, text="This is the Make Pipeline").pack(pady=10, padx=10)
#         tk.Button(self, text="Return to Dashboard", command=lambda: controller.show_frame("Dashboard")).pack()

import tkinter as tk
from tkinter import ttk

class MakePipeline(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.width, self.height = 400, 300
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        # Model Configuration Form
        tk.Label(self, text="Model name").grid(row=0, column=0, sticky='e')
        tk.Entry(self).grid(row=0, column=1, sticky='we')

        tk.Label(self, text="Pretrained").grid(row=1, column=0, sticky='e')
        pretrained_var = tk.BooleanVar()
        tk.Checkbutton(self, variable=pretrained_var).grid(row=1, column=1, sticky='w')

        tk.Label(self, text="Input size").grid(row=2, column=0, sticky='e')
        tk.Entry(self).grid(row=2, column=1, sticky='we')

        tk.Label(self, text="Output classes").grid(row=3, column=0, sticky='e')
        tk.Entry(self).grid(row=3, column=1, sticky='we')

        tk.Label(self, text="Feature extraction method").grid(row=4, column=0, sticky='e')
        ttk.Combobox(self, values=["Method A", "Method B", "Method C"]).grid(row=4, column=1, sticky='we')

        tk.Label(self, text="Epoch numbers").grid(row=5, column=0, sticky='e')
        tk.Entry(self).grid(row=5, column=1, sticky='we')

        tk.Label(self, text="Batch size").grid(row=6, column=0, sticky='e')
        tk.Entry(self).grid(row=6, column=1, sticky='we')

        tk.Label(self, text="Optimizer").grid(row=7, column=0, sticky='e')
        ttk.Combobox(self, values=["Optimizer A", "Optimizer B", "Optimizer C"]).grid(row=7, column=1, sticky='we')

        tk.Label(self, text="Learning rate").grid(row=8, column=0, sticky='e')
        tk.Entry(self).grid(row=8, column=1, sticky='we')

        tk.Label(self, text="Loss functions").grid(row=9, column=0, sticky='e')
        ttk.Combobox(self, values=["Function A", "Function B", "Function C"]).grid(row=9, column=1, sticky='we')

        tk.Label(self, text="Metrics").grid(row=10, column=0, sticky='e')
        ttk.Combobox(self, values=["Metric A", "Metric B", "Metric C"]).grid(row=10, column=1, sticky='we')

        # Navigation Buttons
        tk.Button(self, text="Menu", command=self.goto_menu).grid(row=11, column=0, pady=10)
        tk.Button(self, text="Pipeline", command=self.goto_pipeline).grid(row=11, column=1, pady=10)

        self.grid_columnconfigure(1, weight=1)  # Make the second column expandable

    def goto_menu(self):
        self.controller.show_frame("Dashboard")

    def goto_pipeline(self):
        # This method should switch to the "Pipeline" page
        # pass  # Replace with actual navigation logic to the "Pipeline" page
        print('pipeline ...')

# The below part would be in your main application file (`app.py`)
# from model_config_page import ModelConfigPage
# You would then include ModelConfigPage in the list of pages to load in the App class.
