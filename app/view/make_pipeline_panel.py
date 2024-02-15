import tkinter as tk
from tkinter import ttk, filedialog
from app.models.db_models.database_model import ModelDA
from app.models.dl_models.pipeline import PipelineRunner


class MakePipeline(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.width, self.height = 2500, 400
        self.controller = controller

        self.pipelines = []

        model_da = ModelDA()
        model_names = model_da.get_model_names()
        feature_methods = [None, 'sobel', 'morph', 'gabor', 'hog']

        # Left side - Parameter selection
        tk.Label(self, text="Choose your data file").grid(row=1, column=0, sticky='e')
        self.data_path_entry = tk.Entry(self)
        self.data_path_entry.grid(row=1, column=1, sticky='we')
        tk.Button(self, text="Browse", command=self.browse_data_file).grid(row=1, column=2)

        tk.Label(self, text="Batch Size").grid(row=2, column=0, sticky='e')
        self.batch_size_entry = tk.Entry(self)
        self.batch_size_entry.grid(row=2, column=1, sticky='we')

        tk.Label(self, text="Feature Extraction Method").grid(row=3, column=0, sticky='e')
        self.feature_method_entry = tk.StringVar()
        ttk.Combobox(self, values=feature_methods, textvariable=self.feature_method_entry).grid(row=3, column=1,
                                                                                                sticky='we')

        tk.Label(self, text="Model Name").grid(row=4, column=0, sticky='e')
        self.model_name_entry = tk.StringVar()
        ttk.Combobox(self, values=model_names, textvariable=self.model_name_entry).grid(row=4, column=1, sticky='we')

        tk.Label(self, text="Pretrained").grid(row=5, column=0, sticky='e')
        self.pretrained_var = tk.BooleanVar()
        tk.Checkbutton(self, variable=self.pretrained_var).grid(row=5, column=1, sticky='w')

        tk.Label(self, text="Epoch Numbers").grid(row=6, column=0, sticky='e')
        self.epoch_nums_entry = tk.Entry(self)
        self.epoch_nums_entry.grid(row=6, column=1, sticky='we')

        tk.Label(self, text="Optimizer").grid(row=7, column=0, sticky='e')
        self.optimizer_entry = tk.StringVar()
        ttk.Combobox(self, values=['adam'], textvariable=self.optimizer_entry).grid(row=7, column=1, sticky='we')

        tk.Label(self, text="Loss Function").grid(row=8, column=0, sticky='e')
        self.loss_func_entry = tk.StringVar()
        ttk.Combobox(self, values=['CrossEntropy'], textvariable=self.loss_func_entry).grid(row=8, column=1,
                                                                                            sticky='we')

        tk.Label(self, text="Learning Rate").grid(row=9, column=0, sticky='e')
        self.lr_entry = tk.StringVar()
        ttk.Combobox(self, textvariable=self.lr_entry, values=['0.001', '0.003', '0.01', '0.03']).grid(row=9, column=1,
                                                                                                       sticky='we')

        # Right side - Pipeline table
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
        self.pipeline_treeview.grid(row=0, column=3, rowspan=10, columnspan=7, sticky='nsew', padx=10, pady=5)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.pipeline_treeview.yview)
        scrollbar.grid(row=0, column=10, rowspan=10, sticky='ns')
        self.pipeline_treeview.configure(yscrollcommand=scrollbar.set)

        # Bottom buttons
        tk.Button(self, text="Menu", command=lambda: controller.show_frame("Dashboard")).grid(row=10, column=0, pady=10)
        tk.Button(self, text="Make Pipeline", command=self.make_pipeline).grid(row=10, column=1, pady=10)
        tk.Button(self, text="Run Pipelines", command=self.run_pipelines).grid(row=10, column=3, pady=10)

    def browse_data_file(self):
        folder_selected = filedialog.askdirectory()
        self.data_path_entry.delete(0, tk.END)
        self.data_path_entry.insert(0, folder_selected)

    def make_pipeline(self):
        data_path = self.data_path_entry.get()
        batch_size = self.batch_size_entry.get()
        feature_method = self.feature_method_entry.get()
        model_name = self.model_name_entry.get()
        pretrained = self.pretrained_var.get()
        pretrained = 1 if pretrained else 0
        epoch_nums = self.epoch_nums_entry.get()
        optimizer = self.optimizer_entry.get()
        loss_func = self.loss_func_entry.get()
        lr = self.lr_entry.get()

        values = [data_path, batch_size, feature_method, model_name, pretrained, epoch_nums, optimizer, loss_func, lr]
        self.pipeline_treeview.insert('', tk.END, values=values)

        match lr:
            case '0.001':
                lr = 1e-3
            case '0.01':
                lr = 1e-2
            case '0.003':
                lr = 3e-3
            case '0.03':
                lr = 3e-2

        if feature_method == 'None':
            feature_method = None

        self.controller.pipelines_values.append(values)
        self.controller.pipelines.append(
            PipelineRunner(data_path, int(batch_size), feature_method, model_name, int(pretrained),
                           int(epoch_nums), optimizer, float(lr), loss_func)
        )

        print(len(self.controller.pipelines))

    def run_pipelines(self):
        print(len(self.controller.pipelines))
        print(len(self.controller.pipelines_values))
        self.controller.show_frame("TrainingModel")
