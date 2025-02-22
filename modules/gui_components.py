# modules/gui_components.py
import tkinter as tk
from tkinter import ttk


def create_menu(root, app_instance):
	menu_bar = tk.Menu(root)

	file_menu = tk.Menu(menu_bar, tearoff=0)
	file_menu.add_command(label="Bild laden", command=app_instance.load_image)
	file_menu.add_command(label="Bild speichern", command=app_instance.save_image)
	file_menu.add_separator()
	file_menu.add_command(label="Einstellungen laden", command=app_instance.load_settings)
	file_menu.add_command(label="Einstellungen speichern", command=app_instance.save_settings)
	file_menu.add_separator()
	file_menu.add_command(label="Beenden", command=root.quit)
	menu_bar.add_cascade(label="Datei", menu=file_menu)

	settings_menu = tk.Menu(menu_bar, tearoff=0)
	settings_menu.add_command(label="Poppler Pfad setzen", command=app_instance.set_poppler_path)
	settings_menu.add_command(label="Poppler installieren", command=app_instance.install_poppler)
	menu_bar.add_cascade(label="Einstellungen", menu=settings_menu)

	extras_menu = tk.Menu(menu_bar, tearoff=0)
	extras_menu.add_command(label="OCR ausführen", command=app_instance.run_ocr)
	menu_bar.add_cascade(label="Extras", menu=extras_menu)

	root.config(menu=menu_bar)


def create_image_canvas(parent, height=480, bg="white"):
	frame = tk.Frame(parent)
	frame.pack(fill=tk.BOTH, expand=True)
	canvas = tk.Canvas(frame, bg=bg, height=height)
	canvas.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
	scrollbar_y = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
	scrollbar_y.grid(row=0, column=1, sticky="ns")
	scrollbar_x = tk.Scrollbar(frame, orient=tk.HORIZONTAL, command=canvas.xview)
	scrollbar_x.grid(row=1, column=0, sticky="ew")
	canvas.config(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
	frame.grid_rowconfigure(0, weight=1)
	frame.grid_columnconfigure(0, weight=1)
	return canvas


def create_layers_ui(parent, layer_vars, filter_options, update_callback):
	layers_frame = tk.Frame(parent)
	layers_frame.pack(fill=tk.X)
	layers_frame.grid_columnconfigure(0, weight=1)
	for i in range(5):
		sub_frame = tk.Frame(layers_frame, borderwidth=1, relief=tk.GROOVE)
		sub_frame.grid(row=0, column=i + 1, padx=5, pady=5, sticky="nsew")
		label = tk.Label(sub_frame, text=f"Filter {i + 1}", font=("Arial", 10, "bold"))
		label.grid(row=0, column=0, columnspan=2, pady=(2, 5))
		enabled_var = tk.BooleanVar(value=False)
		chk = tk.Checkbutton(sub_frame, variable=enabled_var, command=update_callback)
		chk.grid(row=1, column=0, sticky="w", padx=5)
		filter_var = tk.StringVar()
		cb = ttk.Combobox(sub_frame, textvariable=filter_var, values=filter_options, state="readonly", width=15)
		cb.current(0)
		cb.grid(row=1, column=1, padx=5, pady=2)
		strength_var = tk.DoubleVar(value=1.0)
		slider = tk.Scale(sub_frame, from_=0.0, to=1.0, resolution=0.01, orient=tk.HORIZONTAL,
						  variable=strength_var, command=lambda val: update_callback(), length=150)
		slider.grid(row=2, column=0, columnspan=2, padx=5, pady=(2, 5))
		layer_vars.append((enabled_var, filter_var, strength_var))


def create_widgets(root, show_left_preview):
	main_frame = tk.Frame(root)
	main_frame.pack(fill=tk.BOTH, expand=True)

	top_frame = tk.Frame(main_frame)
	top_frame.pack(fill=tk.X, padx=10, pady=5)
	filename_label = tk.Label(top_frame, text="Kein Bild geladen", anchor="w")
	filename_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
	settings_label = tk.Label(top_frame, text="Einstellungen: Keine", anchor="e")
	settings_label.pack(side=tk.RIGHT)

	preview_frame = tk.Frame(main_frame)
	preview_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

	if show_left_preview:
		left_frame = tk.Frame(preview_frame, bg="lightgray")
		left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
		left_canvas = create_image_canvas(left_frame)
	else:
		left_canvas = None

	right_frame = tk.Frame(preview_frame, bg="lightyellow")
	if show_left_preview:
		right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
	else:
		right_frame.pack(fill=tk.BOTH, expand=True)
	right_canvas = create_image_canvas(right_frame)

	slider_frame = tk.Frame(main_frame)
	slider_frame.pack(fill=tk.X, padx=10, pady=10)

	return main_frame, top_frame, preview_frame, slider_frame, left_canvas, right_canvas, filename_label, settings_label
