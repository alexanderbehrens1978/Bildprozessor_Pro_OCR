import tkinter as tk
from image_processor_app import ImageProcessorApp
from filters import apply_filter
from image_canvas import ImageCanvas
from settings_manager import load_settings, save_settings
from poppler_manager import install_poppler, get_poppler_path
from ocr_manager import set_tesseract_cmd, perform_ocr
from PIL import Image
from ocr_display import process_file, display_text
from ocr_app import run_ocr_app

# Optional: Setze den Pfad zur Tesseract-Executable, falls notwendig (z. B. unter Windows)
set_tesseract_cmd(r"C:\Programme\Tesseract-OCR\tesseract.exe")


def main():
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
