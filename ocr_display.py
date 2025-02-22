# ocr_display.py
import os
import tkinter as tk
from tkinter import scrolledtext, messagebox
from PIL import Image
from pdf2image import convert_from_path

# Falls pytesseract noch nicht installiert ist, kann dieser Trick hilfreich sein:
try:
    import pytesseract
except ModuleNotFoundError:
    import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pytesseract"])
    import pytesseract

def perform_ocr_on_image(image, lang='deu'):
    """
    Führt OCR auf einem PIL-Image durch und gibt den erkannten Text zurück.
    """
    try:
        text = pytesseract.image_to_string(image, lang=lang)
        return text
    except Exception as e:
        return f"OCR-Fehler: {str(e)}"

def process_image_file(file_path, lang='deu'):
    """
    Öffnet ein Bild, führt OCR darauf aus und gibt den erkannten Text zurück.
    """
    try:
        image = Image.open(file_path)
        return perform_ocr_on_image(image, lang)
    except Exception as e:
        return f"Fehler beim Öffnen des Bildes: {str(e)}"

def process_pdf_file(file_path, lang='deu', dpi=200):
    """
    Konvertiert alle Seiten einer PDF in Bilder, führt auf jeder Seite OCR aus und gibt den
    gesamten erkannten Text zurück.
    """
    try:
        pages = convert_from_path(file_path, dpi=dpi)
        result_text = ""
        for i, page in enumerate(pages):
            page_text = perform_ocr_on_image(page, lang)
            result_text += f"--- Seite {i+1} ---\n{page_text}\n\n"
        return result_text
    except Exception as e:
        return f"Fehler beim Öffnen der PDF: {str(e)}"

def process_file(file_path, lang='deu'):
    """
    Entscheidet anhand der Dateiendung, ob es sich um eine Bild- oder PDF-Datei handelt,
    und führt den entsprechenden OCR-Prozess durch.
    """
    _, ext = os.path.splitext(file_path.lower())
    if ext == '.pdf':
        return process_pdf_file(file_path, lang)
    else:
        return process_image_file(file_path, lang)

def display_text(text, title="OCR Ergebnis"):
    """
    Öffnet ein Tkinter-Fenster mit einem ScrolledText-Widget, um den erkannten Text anzuzeigen.
    """
    root = tk.Tk()
    root.title(title)
    st = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=30)
    st.pack(expand=True, fill='both')
    st.insert(tk.END, text)
    st.configure(state='disabled')
    root.mainloop()

# Beispiel für den direkten Aufruf des Moduls über die Kommandozeile
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        if os.path.exists(file_path):
            ocr_result = process_file(file_path, lang='deu')
            display_text(ocr_result, title=f"OCR Ergebnis für {os.path.basename(file_path)}")
        else:
            messagebox.showerror("Fehler", f"Datei nicht gefunden: {file_path}")
    else:
        print("Usage: python ocr_display.py <Pfad zur Datei>")
