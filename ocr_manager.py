# ocr_manager.py

try:
	import pytesseract
except ModuleNotFoundError:
	import subprocess
	import sys

	# Versucht, pytesseract automatisch zu installieren
	subprocess.check_call([sys.executable, "-m", "pip", "install", "pytesseract"])
	import pytesseract

from PIL import Image


def set_tesseract_cmd(cmd_path):
	"""
	Setzt den Pfad zur Tesseract-Executable.

	:param cmd_path: Vollständiger Pfad zur tesseract.exe (z. B. unter Windows)
	"""
	pytesseract.pytesseract.tesseract_cmd = cmd_path


def perform_ocr(image, lang='deu'):
	"""
	Führt OCR (Optical Character Recognition) auf einem Bild durch.

	:param image: Ein PIL.Image-Objekt, auf dem OCR durchgeführt werden soll.
	:param lang: Sprachcode für OCR (Standard 'deu' für Deutsch)
	:return: Erkannten Text als String.
	:raises Exception: Bei Fehlern während der OCR-Verarbeitung.
	"""
	try:
		text = pytesseract.image_to_string(image, lang=lang)
		return text
	except Exception as e:
		raise Exception(f"OCR-Fehler: {str(e)}")
