# modules/ocr_app.py
import tkinter as tk
from tkinter import filedialog, messagebox
from modules.ocr_display import process_file, display_text

def run_ocr_app():
    """
    Öffnet einen Dateidialog, führt OCR auf der ausgewählten Datei aus und zeigt das Ergebnis an.
    """
    file_path = filedialog.askopenfilename(
        title="Wähle ein Bild oder PDF für OCR",
        filetypes=[("Bilddateien und PDFs", "*.png;*.jpg;*.jpeg;*.pdf"), ("Alle Dateien", "*.*")]
    )
    if not file_path:
        messagebox.showwarning("Keine Datei ausgewählt", "Es wurde keine Datei ausgewählt.")
        return

    ocr_text = process_file(file_path, lang='deu')
    display_text(ocr_text, title="OCR Ergebnis")

def get_frame(parent):
    """
    Liefert einen Frame mit einem Button, der die OCR-Funktion startet.
    """
    frame = tk.Frame(parent)
    button = tk.Button(frame, text="OCR ausführen", command=run_ocr_app)
    button.pack(padx=10, pady=10)
    return frame
