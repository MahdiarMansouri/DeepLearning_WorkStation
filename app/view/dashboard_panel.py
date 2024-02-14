import tkinter as tk


class Dashboard(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.width, self.height = 300, 200

        tk.Label(self, text="Main Menu").pack(pady=10, padx=10)
        tk.Button(self, text="Go to Make Model", command=lambda: controller.show_frame("MakeModel")).pack()
        tk.Button(self, text="Go to Make Pipeline", command=lambda: controller.show_frame("MakePipeline")).pack()
        tk.Button(self, text="Go to Show Results", command=lambda: controller.show_frame("ShowResults")).pack()
