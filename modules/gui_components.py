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


def create_layers_ui(parent, layer_vars, filter_options, update_callback):
	layers_frame = tk.Frame(parent, bg="white")
	layers_frame.pack(fill=tk.X)
	layers_frame.grid_columnconfigure(0, weight=1)
	for i in range(5):
		sub_frame = tk.Frame(layers_frame, borderwidth=1, relief=tk.GROOVE, bg="white")
		sub_frame.grid(row=0, column=i + 1, padx=5, pady=5, sticky="nsew")
		label = tk.Label(sub_frame, text=f"Filter {i + 1}", font=("Arial", 10, "bold"), bg="white")
		label.grid(row=0, column=0, columnspan=2, pady=(2, 5))
		enabled_var = tk.BooleanVar(value=False)
		chk = tk.Checkbutton(sub_frame, variable=enabled_var, command=update_callback, bg="white")
		chk.grid(row=1, column=0, sticky="w", padx=5)
		filter_var = tk.StringVar()
		cb = ttk.Combobox(sub_frame, textvariable=filter_var, values=filter_options, state="readonly", width=15)
		cb.current(0)
		cb.grid(row=1, column=1, padx=5, pady=2)
		strength_var = tk.DoubleVar(value=1.0)
		slider = tk.Scale(sub_frame, from_=0.0, to=1.0, resolution=0.01, orient=tk.HORIZONTAL,
						  variable=strength_var, command=lambda val: update_callback(), length=150, bg="white")
		slider.grid(row=2, column=0, columnspan=2, padx=5, pady=(2, 5))
		layer_vars.append((enabled_var, filter_var, strength_var))
