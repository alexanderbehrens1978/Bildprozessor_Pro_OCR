# modules/ocr_factory.py
def get_ocr_module(name="tesseract_cpu"):
	"""
	Liefert die perform_ocr-Funktion des gewählten OCR-Moduls.

	Mögliche Optionen:
	  - "tesseract_cpu"
	  - "tesseract_gpu"
	  - "paddleocr_cpu"
	  - "paddleocr_gpu"
	"""
	if name == "tesseract_cpu":
		from modules.ocr_tesseract_cpu import perform_ocr
		return perform_ocr
	elif name == "tesseract_gpu":
		from modules.ocr_tesseract_gpu import perform_ocr
		return perform_ocr
	elif name == "paddleocr_cpu":
		from modules.ocr_paddleocr_cpu import perform_ocr
		return perform_ocr
	elif name == "paddleocr_gpu":
		from modules.ocr_paddleocr_gpu import perform_ocr
		return perform_ocr
	else:
		raise ValueError(f"Unbekanntes OCR-Modul: {name}")
