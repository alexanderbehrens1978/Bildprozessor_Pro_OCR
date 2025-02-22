# modules/ocr_runner.py
import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk
from modules.ocr_factory import get_ocr_module

def run_ocr_op(app_instance):
    if app_instance.processed_image is None:
        messagebox.showwarning("Kein Bild", "Bitte laden Sie ein Bild und wenden Sie Filter an, bevor OCR ausgeführt wird.")
        return
    ocr_func = get_ocr_module("tesseract_cpu")
    try:
        processed, results = ocr_func(app_instance.processed_image.copy(), lang='deu')
    except Exception as e:
        messagebox.showerror("OCR Fehler", f"Bei der OCR ist ein Fehler aufgetreten: {str(e)}")
        return
    ocr_window = tk.Toplevel(app_instance.root)
    ocr_window.title("OCR Ergebnis")
    tk_img = ImageTk.PhotoImage(processed)
    img_label = tk.Label(ocr_window, image=tk_img)
    img_label.image = tk_img
    img_label.pack()
    text_lines = []
    for res in results:
        if 'left' in res:
            text_lines.append(f"{res['number']}: {res['text']} (Position: {res['left']}, {res['top']})")
        else:
            text_lines.append(f"{res['number']}: {res['text']} (Box: {res['points']})")
    text_label = tk.Label(ocr_window, text="\n".join(text_lines), justify="left")
    text_label.pack()
