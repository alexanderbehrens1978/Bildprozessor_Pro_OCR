# image_canvas.py
import tkinter as tk

class ImageCanvas(tk.Frame):
    def __init__(self, parent, bg="white", height=480):
        super().__init__(parent)
        self.canvas = tk.Canvas(self, bg=bg, height=height)
        self.canvas.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.scrollbar_y = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar_y.grid(row=0, column=1, sticky="ns")
        self.scrollbar_x = tk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.scrollbar_x.grid(row=1, column=0, sticky="ew")
        self.canvas.config(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
