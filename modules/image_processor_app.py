import tkinter as tk
from tkinter import messagebox, filedialog
import json, os, subprocess, sys

from modules.utils import get_program_path
from modules.poppler_manager import get_poppler_path, install_poppler
from modules.settings_manager import load_settings as settings_load, save_settings as settings_save
from modules.gui_components import create_menu, create_image_canvas, create_layers_ui, \
	create_widgets as create_widgets_func
from modules.file_handlers import load_image_file, save_image_file
from modules.image_ops import update_image_op, show_image_op, apply_filter_op
from modules.ocr_runner import run_ocr_op
from modules.ocr_factory import get_ocr_module


class ImageProcessorApp:
	def __init__(self, root):
		self.root = root
		self.root.title("Bildprozessor Pro Version 1.0")
		self.poppler_path = ""
		self.settings_file_name = "Keine Einstellungen geladen"
		self.default_layer_settings = []
		self.show_left_preview = True
		self.layer_vars = []
		self.filter_options = [
			"Negativ", "Multiplikation", "Helligkeit", "Kontrast", "Schärfen",
			"Weichzeichnen", "Graustufen", "Sepia", "Posterize", "Solarize",
			"Kantenerkennung", "Emboss", "Edge Enhance", "Detail", "Smooth",
			"Binarize", "Gamma Correction", "Adaptive Threshold", "Color Boost", "Custom"
		]
		self.original_image = None
		self.processed_image = None
		self.filename = None

		self.load_default_settings()
		self.create_menu()
		self.create_widgets()

	def load_default_settings(self):
		prog_path = get_program_path()
		settings_file = os.path.join(prog_path, "settings.json")
		if os.path.exists(settings_file):
			try:
				with open(settings_file, "r") as f:
					settings = json.load(f)
				self.poppler_path = settings.get("poppler_path", "")
				self.default_layer_settings = settings.get("layers", [])
				self.settings_file_name = os.path.basename(settings_file)
				self.show_left_preview = settings.get("show_left_preview", True)
			except Exception as e:
				messagebox.showerror("Fehler", f"Einstellungen konnten nicht geladen werden: {str(e)}")
		else:
			self.default_layer_settings = []
			self.show_left_preview = True
			messagebox.showwarning("Einstellungen nicht gefunden", "Die Datei settings.json wurde nicht gefunden.")

	def create_menu(self):
		create_menu(self.root, self)

	def create_widgets(self):
		# Verwende die umbenannte Funktion aus gui_components
		widgets = create_widgets_func(self.root, self.show_left_preview)
		(self.main_frame, self.top_frame, self.preview_frame, self.slider_frame,
		 self.left_canvas, self.right_canvas, self.filename_label, self.settings_label) = widgets
		create_layers_ui(self.slider_frame, self.layer_vars, self.filter_options, self.update_image)

		if self.default_layer_settings:
			for setting in self.default_layer_settings:
				layer_idx = setting["layer"] - 1
				if layer_idx < len(self.layer_vars):
					enabled_var, filter_var, strength_var = self.layer_vars[layer_idx]
					enabled_var.set(setting.get("enabled", False))
					filter_var.set(setting.get("filter", self.filter_options[0]))
					strength_var.set(setting.get("strength", 1.0))
			self.update_image()

	def load_image(self):
		load_image_file(self)

	def save_image(self):
		save_image_file(self)

	def load_settings(self):
		file_path = filedialog.askopenfilename(
			title="Einstellungen laden",
			filetypes=[("JSON-Dateien", "*.json"), ("Alle Dateien", "*.*")]
		)
		if file_path:
			try:
				with open(file_path, 'r') as f:
					settings = json.load(f)
				self.poppler_path = settings.get("poppler_path", "")
				self.show_left_preview = settings.get("show_left_preview", True)
				for setting in settings.get("layers", []):
					layer_idx = setting["layer"] - 1
					if layer_idx < len(self.layer_vars):
						enabled_var, filter_var, strength_var = self.layer_vars[layer_idx]
						enabled_var.set(setting.get("enabled", False))
						filter_var.set(setting.get("filter", self.filter_options[0]))
						strength_var.set(setting.get("strength", 1.0))
				self.settings_file_name = file_path.split(os.sep)[-1]
				self.settings_label.config(text="Einstellungen: " + self.settings_file_name)
				messagebox.showinfo("Erfolg", "Einstellungen erfolgreich geladen.")
				self.update_image()
			except Exception as e:
				messagebox.showerror("Fehler", f"Laden fehlgeschlagen: {str(e)}")

	def save_settings(self):
		settings = {
			"poppler_path": self.poppler_path,
			"layers": [],
			"show_left_preview": self.show_left_preview
		}
		for idx, (enabled_var, filter_var, strength_var) in enumerate(self.layer_vars):
			settings["layers"].append({
				"layer": idx + 1,
				"enabled": enabled_var.get(),
				"filter": filter_var.get(),
				"strength": strength_var.get()
			})
		file_path = settings_save(settings)
		if file_path:
			self.settings_file_name = file_path.split(os.sep)[-1]
			self.settings_label.config(text="Einstellungen: " + self.settings_file_name)
			messagebox.showinfo("Erfolg", "Einstellungen erfolgreich gespeichert.")

	def update_image(self, *args):
		update_image_op(self)

	def apply_filter(self, img, filter_name, strength=1.0):
		return apply_filter_op(img, filter_name, strength)

	def show_image(self, image, canvas):
		show_image_op(image, canvas)

	def set_poppler_path(self):
		prog_path = get_program_path()
		path = filedialog.askdirectory(title="Wähle den Poppler-Library-Bin-Ordner", initialdir=prog_path)
		if path:
			self.poppler_path = path
			messagebox.showinfo("Poppler Pfad", f"Poppler Pfad gesetzt auf:\n{self.poppler_path}")

	def install_poppler(self):
		install_poppler()

	def run_ocr(self):
		run_ocr_op(self)


if __name__ == "__main__":
	root = tk.Tk()
	app = ImageProcessorApp(root)
	root.mainloop()
