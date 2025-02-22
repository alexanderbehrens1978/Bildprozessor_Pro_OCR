import subprocess, sys

try:
    from paddleocr import PaddleOCR, draw_ocr
except ModuleNotFoundError as e:
    if "paddle" in str(e).lower():
        subprocess.check_call([sys.executable, "-m", "pip", "install", "paddlepaddle-cpu"])
    else:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "paddleocr"])
    from paddleocr import PaddleOCR, draw_ocr

from PIL import Image, ImageDraw, ImageFont
import numpy as np

ocr_model = PaddleOCR(use_angle_cls=True, lang="de", use_gpu=False)

def perform_ocr(image, lang='deu'):
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
        box = line[0]
        text = line[1][0]
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
