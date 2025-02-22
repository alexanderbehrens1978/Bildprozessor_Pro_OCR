# main.py
import tkinter as tk
from modules.image_processor_app import ImageProcessorApp

def main():
    root = tk.Tk()
    root.geometry("1024x768")
    app = ImageProcessorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
