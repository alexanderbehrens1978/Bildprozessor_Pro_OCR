# modules/ocr_tesseract_cpu.py
try:
	import pytesseract
except ModuleNotFoundError:
	import subprocess, sys

	subprocess.check_call([sys.executable, "-m", "pip", "install", "pytesseract"])
	import pytesseract

from PIL import Image, ImageDraw, ImageFont


def perform_ocr(image, lang='deu'):
	"""
	Führt OCR mit Tesseract (CPU) aus. Zeichnet grüne Umrandungen um erkannte Texte,
	nummeriert diese und liefert Positionsdaten.

	:param image: PIL.Image-Objekt
	:param lang: Sprache (Standard 'deu')
	:return: (processed_image, results)
			 processed_image: Das Bild mit eingezeichneten Umrandungen
			 results: Liste von Dicts mit 'number', 'text', 'left', 'top', 'width', 'height'
	"""
	data = pytesseract.image_to_data(image, lang=lang, output_type=pytesseract.Output.DICT)
	draw = ImageDraw.Draw(image)
	results = []
	try:
		font = ImageFont.truetype("arial.ttf", 16)
	except:
		font = None

	num = 1
	n_boxes = len(data['level'])
	for i in range(n_boxes):
		text = data['text'][i].strip()
		if text != "":
			x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
			draw.rectangle([(x, y), (x + w, y + h)], outline="green", width=2)
			draw.text((x, y - 20), str(num), fill="green", font=font)
			results.append({
				'number': num,
				'text': text,
				'left': x,
				'top': y,
				'width': w,
				'height': h
			})
			num += 1
	return image, results
