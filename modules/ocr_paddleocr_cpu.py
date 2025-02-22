# modules/ocr_paddleocr_cpu.py
import subprocess, sys

# Versuche, PaddleOCR zu importieren. Falls das fehlgeschlagene Import-Statement auf das fehlende 'paddle'-Modul hindeutet,
# wird versucht, das CPU-Paket von PaddlePaddle zu installieren.
try:
	from paddleocr import PaddleOCR, draw_ocr
except ModuleNotFoundError as e:
	if "paddle" in str(e).lower():
		print("Paddle-Modul nicht gefunden, installiere paddlepaddle-cpu...")
		subprocess.check_call([sys.executable, "-m", "pip", "install", "paddlepaddle-cpu"])
	else:
		print("PaddleOCR-Modul nicht gefunden, installiere paddleocr...")
		subprocess.check_call([sys.executable, "-m", "pip", "install", "paddleocr"])
	from paddleocr import PaddleOCR, draw_ocr

from PIL import Image, ImageDraw, ImageFont
import numpy as np

# Erstelle eine PaddleOCR-Instanz für CPU (use_gpu=False)
ocr_model = PaddleOCR(use_angle_cls=True, lang="de", use_gpu=False)


def perform_ocr(image, lang='deu'):
	"""
	Führt OCR mit PaddleOCR (CPU) aus, zeichnet grüne Umrandungen, nummeriert die Ergebnisse
	und liefert Positionsdaten.

	:param image: PIL.Image-Objekt
	:param lang: Wird ignoriert, da das Modell bereits für 'de' eingestellt ist.
	:return: (processed_image, results)
			 results: Liste von Dicts mit 'number', 'text' und 'points' (die Bounding Box)
	"""
	image_np = np.array(image.convert("RGB"))
	result = ocr_model.ocr(image_np, cls=True)
	draw = ImageDraw.Draw(image)
	results = []
	try:
		font = ImageFont.truetype("arial.ttf", 16)
	except:
		font = None
	num = 1
	for line in result:
		box = line[0]  # Liste von 4 Punkten: [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
		text = line[1][0]
		# Zeichne die Bounding Box (geschlossen durch erneutes Verbinden des ersten Punktes)
		draw.line(box + [box[0]], fill="green", width=2)
		x, y = box[0]
		draw.text((x, y - 20), str(num), fill="green", font=font)
		results.append({
			'number': num,
			'text': text,
			'points': box
		})
		num += 1
	return image, results
