# modules/image_processor_app.py
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk, ImageFilter, ImageOps, ImageChops, ImageEnhance
from pdf2image import convert_from_path
import json, os, subprocess, sys

from modules.utils import get_program_path
from modules.poppler_manager import get_poppler_path, install_poppler
from modules.settings_manager import load_settings, save_settings
from modules.gui_components import create_menu, create_image_canvas, create_layers_ui

# Importiere die OCR-Factory, um später das OCR-Modul zu wählen (Standard: tesseract_cpu)
from modules.ocr_factory import get_ocr_module


class ImageProcessorApp:
	def __init__(self, root):
		self.root = root
		self.root.title(
			"Bildprozessor Pro            Version 1.0        21.02.2025 von Alexander Behrens info@alexanderbehrens.com")
		self.poppler_path = ""  # Benutzerdefinierter Poppler-Pfad (wird ggf. manuell gesetzt)
		self.settings_file_name = "Keine Einstellungen geladen"
		self.default_layer_settings = []
		self.load_default_settings()
		self.create_menu()  # Menü wird erstellt (inklusive OCR-Menüpunkt)

		self.original_image = None
		self.processed_image = None
		self.filename = None
		self.layer_vars = []
		self.filter_options = [
			"Negativ", "Multiplikation", "Helligkeit", "Kontrast", "Schärfen",
			"Weichzeichnen", "Graustufen", "Sepia", "Posterize", "Solarize",
			"Kantenerkennung", "Emboss", "Edge Enhance", "Detail", "Smooth",
			"Binarize", "Gamma Correction", "Adaptive Threshold", "Color Boost", "Custom"
		]
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
				# Neuer Parameter: linke Vorschau anzeigen oder nicht
				self.show_left_preview = settings.get("show_left_preview", True)
			except Exception as e:
				messagebox.showerror("Fehler", f"Einstellungen konnten nicht geladen werden: {str(e)}")
		else:
			self.default_layer_settings = []
			self.show_left_preview = True
			messagebox.showwarning("Einstellungen nicht gefunden", "Die Datei settings.json wurde nicht gefunden.")

	def create_menu(self):
		# Nutzt die Funktion aus gui_components, ergänzt um einen OCR-Menüpunkt
		menu_bar = tk.Menu(self.root)

		# Datei-Menü
		file_menu = tk.Menu(menu_bar, tearoff=0)
		file_menu.add_command(label="Bild laden", command=self.load_image)
		file_menu.add_command(label="Bild speichern", command=self.save_image)
		file_menu.add_separator()
		file_menu.add_command(label="Einstellungen laden", command=self.load_settings)
		file_menu.add_command(label="Einstellungen speichern", command=self.save_settings)
		file_menu.add_separator()
		file_menu.add_command(label="Beenden", command=self.root.quit)
		menu_bar.add_cascade(label="Datei", menu=file_menu)

		# Einstellungen-Menü (Poppler etc.)
		settings_menu = tk.Menu(menu_bar, tearoff=0)
		settings_menu.add_command(label="Poppler Pfad setzen", command=self.set_poppler_path)
		settings_menu.add_command(label="Poppler installieren", command=self.install_poppler)
		menu_bar.add_cascade(label="Einstellungen", menu=settings_menu)

		# Extras-Menü: Hier integrieren wir OCR als Zusatzfunktion
		extras_menu = tk.Menu(menu_bar, tearoff=0)
		extras_menu.add_command(label="OCR ausführen", command=self.run_ocr)
		menu_bar.add_cascade(label="Extras", menu=extras_menu)

		self.root.config(menu=menu_bar)

	def create_widgets(self):
		main_frame = tk.Frame(self.root)
		main_frame.pack(fill=tk.BOTH, expand=True)

		# Obere Leiste: Dateiname und Einstellungen
		top_frame = tk.Frame(main_frame)
		top_frame.pack(fill=tk.X, padx=10, pady=5)
		self.filename_label = tk.Label(top_frame, text="Kein Bild geladen", anchor="w")
		self.filename_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
		self.settings_label = tk.Label(top_frame, text="Einstellungen: " + self.settings_file_name, anchor="e")
		self.settings_label.pack(side=tk.RIGHT)

		# Vorschau-Frame für Original- und bearbeitetes Bild
		preview_frame = tk.Frame(main_frame)
		preview_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

		if self.show_left_preview:
			left_frame = tk.Frame(preview_frame, bg="lightgray")
			left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
			self.left_canvas = create_image_canvas(left_frame)
		else:
			self.left_canvas = None  # Wird nicht verwendet

		right_frame = tk.Frame(preview_frame, bg="lightyellow")
		# Falls linke Vorschau deaktiviert ist, soll der rechte Bereich den gesamten Platz einnehmen.
		if self.show_left_preview:
			right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
		else:
			right_frame.pack(fill=tk.BOTH, expand=True)
		self.right_canvas = create_image_canvas(right_frame)

		# Slider-/Layer-Panel (bleibt unverändert)
		self.slider_frame = tk.Frame(main_frame)
		self.slider_frame.pack(fill=tk.X, padx=10, pady=10)
		create_layers_ui(self.slider_frame, self.layer_vars, self.filter_options, self.update_image)

		# Anwenden von Default-Einstellungen (falls vorhanden)
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
		file_path = filedialog.askopenfilename(
			filetypes=[("Bilder/PDFs", "*.png;*.jpg;*.jpeg;*.pdf"), ("Alle Dateien", "*.*")]
		)
		if file_path:
			try:
				if file_path.lower().endswith(".pdf"):
					current_poppler_path = get_poppler_path(self.poppler_path)
					if not current_poppler_path:
						messagebox.showerror("Fehler",
											 "Poppler Pfad ist nicht gesetzt. Bitte setze den Poppler Pfad unter 'Einstellungen'.")
						return
					pages = convert_from_path(file_path, dpi=200, poppler_path=current_poppler_path)
					self.original_image = pages[0]
				else:
					self.original_image = Image.open(file_path).convert("RGB")
				self.filename = os.path.basename(file_path)
				self.filename_label.config(text=self.filename)
				self.show_image(self.original_image, self.left_canvas)
				self.update_image()
				self.left_canvas.update_idletasks()
				h = self.left_canvas.winfo_height()
				self.right_canvas.config(height=h)
			except Exception as e:
				messagebox.showerror("Fehler", f"Konnte Bild laden: {str(e)}")

	def save_image(self):
		if self.processed_image:
			filter_info = []
			for i, (enabled_var, filter_var, strength_var) in enumerate(self.layer_vars):
				if enabled_var.get():
					filter_info.append(f"{i + 1}_{filter_var.get()}_{strength_var.get():.2f}")
			default_name = ""
			if self.filename:
				base = os.path.splitext(self.filename)[0]
				default_name = f"{base}_" + "_".join(filter_info) if filter_info else base
			file_path = filedialog.asksaveasfilename(
				defaultextension=".png",
				filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("Alle Dateien", "*.*")],
				title="Bild speichern",
				initialfile=default_name
			)
			if file_path:
				try:
					self.processed_image.save(file_path)
					messagebox.showinfo("Erfolg", "Bild erfolgreich gespeichert.")
				except Exception as e:
					messagebox.showerror("Fehler", f"Speichern fehlgeschlagen: {str(e)}")

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
				for setting in settings.get("layers", []):
					layer_idx = setting["layer"] - 1
					if layer_idx < len(self.layer_vars):
						enabled_var, filter_var, strength_var = self.layer_vars[layer_idx]
						enabled_var.set(setting.get("enabled", False))
						filter_var.set(setting.get("filter", self.filter_options[0]))
						strength_var.set(setting.get("strength", 1.0))
				self.settings_file_name = os.path.basename(file_path)
				self.settings_label.config(text="Einstellungen: " + self.settings_file_name)
				messagebox.showinfo("Erfolg", "Einstellungen erfolgreich geladen.")
				self.update_image()
			except Exception as e:
				messagebox.showerror("Fehler", f"Laden fehlgeschlagen: {str(e)}")

	def save_settings(self):
		settings = {
			"poppler_path": self.poppler_path,
			"layers": [],
			"show_left_preview": self.show_left_preview  # Speichere den neuen Parameter
		}
		for idx, (enabled_var, filter_var, strength_var) in enumerate(self.layer_vars):
			settings["layers"].append({
				"layer": idx + 1,
				"enabled": enabled_var.get(),
				"filter": filter_var.get(),
				"strength": strength_var.get()
			})
		file_path = save_settings(settings)
		if file_path:
			self.settings_file_name = os.path.basename(file_path)
			self.settings_label.config(text="Einstellungen: " + self.settings_file_name)
			messagebox.showinfo("Erfolg", "Einstellungen erfolgreich gespeichert.")

	def update_image(self, *args):
		if self.original_image:
			img = self.original_image.copy()
			# Filteranwendung für alle aktiven Layer
			for enabled_var, filter_var, strength_var in self.layer_vars:
				if enabled_var.get():
					img = self.apply_filter(img, filter_var.get(), strength_var.get())
			self.processed_image = img
			self.show_image(img, self.right_canvas)

	def apply_filter(self, img, filter_name, strength=1.0):
		# Beispielhafter Filtercode – hier können weitere Filter implementiert werden.
		try:
			if filter_name == "Negativ":
				blend_factor = min(max(strength, 0), 1)
				inverted = ImageOps.invert(img)
				return Image.blend(img, inverted, blend_factor)
			elif filter_name == "Multiplikation":
				blend_factor = min(max(strength, 0), 1)
				overlay_value = int(255 * blend_factor)
				overlay = Image.new("RGB", img.size, (overlay_value, overlay_value, overlay_value))
				return ImageChops.multiply(img, overlay)
			elif filter_name == "Custom":
				return img.copy()
			else:
				return img.copy()
		except Exception as e:
			messagebox.showerror("Fehler", f"Fehler beim Anwenden des Filters: {str(e)}")
			return img.copy()

	def show_image(self, image, canvas):
		canvas.delete("all")
		photo = ImageTk.PhotoImage(image)
		canvas.create_image(10, 10, image=photo, anchor="nw")
		canvas.image = photo
		width, height = image.size
		canvas.config(scrollregion=(0, 0, width + 20, height + 20))

	def set_poppler_path(self):
		prog_path = get_program_path()
		path = filedialog.askdirectory(title="Wähle den Poppler-Library-Bin-Ordner", initialdir=prog_path)
		if path:
			self.poppler_path = path
			messagebox.showinfo("Poppler Pfad", f"Poppler Pfad gesetzt auf:\n{self.poppler_path}")

	def install_poppler(self):
		install_poppler()

	def run_ocr(self):
		"""
		Führt OCR auf dem aktuell geladenen Bild aus.
		Wird über den Menüpunkt "OCR ausführen" im Extras-Menü aufgerufen.
		Standardmäßig wird das OCR-Modul "tesseract_cpu" verwendet.
		"""
		if self.original_image is None:
			messagebox.showwarning("Kein Bild", "Bitte laden Sie zunächst ein Bild.")
			return

		# Hole das OCR-Modul (Standard: tesseract_cpu)
		ocr_func = get_ocr_module()  # Default-Parameter in der Factory ist "tesseract_cpu"
		try:
			# Wende OCR auf einer Kopie des geladenen Bildes an, um das Original nicht zu verändern.
			processed, results = ocr_func(self.original_image.copy(), lang='deu')
		except Exception as e:
			messagebox.showerror("OCR Fehler", f"Bei der OCR ist ein Fehler aufgetreten: {str(e)}")
			return

		# Erstelle ein neues Fenster zur Anzeige des OCR-Ergebnisses
		ocr_window = tk.Toplevel(self.root)
		ocr_window.title("OCR Ergebnis")
		tk_img = ImageTk.PhotoImage(processed)
		img_label = tk.Label(ocr_window, image=tk_img)
		img_label.image = tk_img  # Referenz speichern
		img_label.pack()

		# Erstelle einen Textbereich zur Anzeige der erkannten Texte und Positionen
		text_lines = []
		for res in results:
			# Unterscheidung zwischen Tesseract- (left/top) und PaddleOCR-Ergebnissen (points)
			if 'left' in res:
				text_lines.append(f"{res['number']}: {res['text']} (Position: {res['left']}, {res['top']})")
			else:
				text_lines.append(f"{res['number']}: {res['text']} (Box: {res['points']})")
		text_label = tk.Label(ocr_window, text="\n".join(text_lines), justify="left")
		text_label.pack()


def open_settings_window(self):
	settings_win = tk.Toplevel(self.root)
	settings_win.title("Einstellungen")

	# Beispiel: Checkbutton für linke Vorschau
	var_left = tk.BooleanVar(value=self.show_left_preview)

	def update_preview_setting():
		self.show_left_preview = var_left.get()
		# Neuzeichnen des Vorschau-Bereichs
		for widget in self.root.winfo_children():
			widget.destroy()
		self.create_widgets()

	tk.Checkbutton(settings_win, text="Linke Vorschau anzeigen", variable=var_left,
				   command=update_preview_setting).pack(padx=10, pady=10)


# Hier könnten weitere Einstellungen hinzugefügt werden.


if __name__ == "__main__":
	root = tk.Tk()
	app = ImageProcessorApp(root)
	root.mainloop()
