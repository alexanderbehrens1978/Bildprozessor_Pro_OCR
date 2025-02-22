# ocr_app.py
import tkinter as tk
from tkinter import filedialog, messagebox
from ocr_display import process_file, display_text


def run_ocr_app(lang='deu'):
	"""
	Startet die OCR-Anwendung:
	  - Öffnet einen Dateidialog, um eine vorhandene Bild- oder PDF-Datei auszuwählen.
	  - Führt OCR auf der ausgewählten Datei durch.
	  - Zeigt den erkannten Text in einem eigenen Fenster an.

	:param lang: Sprachcode für OCR (Standard: 'deu' für Deutsch)
	"""
	# Initialisiere Tkinter und verstecke das Hauptfenster
	root = tk.Tk()
	root.withdraw()

	# Öffne einen Dialog zur Dateiauswahl (Bilder und PDFs)
	file_path = filedialog.askopenfilename(
		title="Wähle ein Bild oder PDF für OCR",
		filetypes=[("Bilddateien und PDFs", "*.png;*.jpg;*.jpeg;*.pdf"), ("Alle Dateien", "*.*")]
	)

	if not file_path:
		messagebox.showwarning("Keine Datei ausgewählt", "Es wurde keine Datei ausgewählt.")
		return

	# Führe OCR auf der ausgewählten Datei aus
	ocr_text = process_file(file_path, lang=lang)

	# Zeige den erkannten Text in einem eigenen Fenster an
	display_text(ocr_text, title="OCR Ergebnis")


if __name__ == "__main__":
	run_ocr_app()
