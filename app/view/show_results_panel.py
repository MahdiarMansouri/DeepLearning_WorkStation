from app.view.dashboard_panel import Dashboard
import tkinter as tk



class ShowResults(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.width, self.height = 500, 400  # Preferred size for the SecondPage
        tk.Label(self, text="This is the Show results").pack(pady=10, padx=10)
        tk.Button(self, text="Return to Menu", command=lambda: parent.show_frame(Dashboard)).pack()