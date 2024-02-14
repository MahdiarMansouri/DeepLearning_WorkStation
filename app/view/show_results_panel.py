import tkinter as tk


class ShowResults(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.width, self.height = 500, 400
        tk.Label(self, text="This is the Show results").pack(pady=10, padx=10)
        tk.Button(self, text="Return to Menu", command=lambda: controller.show_frame("Dashboard")).pack()