import tkinter as tk


def build_view(root, show_left_preview):
	"""
	Baut das Layout der Anwendung. In dieser Datei kannst du das Aussehen einstellen.
	Gibt ein Dictionary mit den folgenden Widgets zurück:
	  - main_frame
	  - top_frame
	  - preview_frame
	  - slider_frame
	  - left_canvas (optional, wenn show_left_preview True)
	  - right_canvas
	  - filename_label
	  - settings_label
	"""
	main_frame = tk.Frame(root, bg="white")
	main_frame.pack(fill=tk.BOTH, expand=True)

	top_frame = tk.Frame(main_frame, bg="lightblue")
	top_frame.pack(fill=tk.X, padx=10, pady=5)
	filename_label = tk.Label(top_frame, text="Kein Bild geladen", anchor="w", bg="lightblue", font=("Arial", 12))
	filename_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
	settings_label = tk.Label(top_frame, text="Einstellungen: Keine", anchor="e", bg="lightblue", font=("Arial", 12))
	settings_label.pack(side=tk.RIGHT)

	preview_frame = tk.Frame(main_frame, bg="gray")
	preview_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

	if show_left_preview:
		left_frame = tk.Frame(preview_frame, bg="lightgray")
		left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
		left_canvas = create_canvas(left_frame)
	else:
		left_canvas = None

	right_frame = tk.Frame(preview_frame, bg="lightyellow")
	if show_left_preview:
		right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
	else:
		right_frame.pack(fill=tk.BOTH, expand=True)
	right_canvas = create_canvas(right_frame)

	slider_frame = tk.Frame(main_frame, bg="white")
	slider_frame.pack(fill=tk.X, padx=10, pady=10)

	return {
		"main_frame": main_frame,
		"top_frame": top_frame,
		"preview_frame": preview_frame,
		"slider_frame": slider_frame,
		"left_canvas": left_canvas,
		"right_canvas": right_canvas,
		"filename_label": filename_label,
		"settings_label": settings_label
	}


import tkinter as tk


def create_canvas(parent, height=480, bg="white"):
	# Container-Frame, der den Canvas und die Scrollbars enthält
	container = tk.Frame(parent)
	container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

	# Canvas erstellen und im Grid platzieren
	canvas = tk.Canvas(container, bg=bg, height=height)
	canvas.grid(row=0, column=0, sticky="nsew")

	# Vertikale Scrollbar
	v_scroll = tk.Scrollbar(container, orient=tk.VERTICAL, command=canvas.yview)
	v_scroll.grid(row=0, column=1, sticky="ns")

	# Horizontale Scrollbar
	h_scroll = tk.Scrollbar(container, orient=tk.HORIZONTAL, command=canvas.xview)
	h_scroll.grid(row=1, column=0, sticky="ew")

	# Scrollbars mit dem Canvas verknüpfen
	canvas.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

	# Container-Grid so konfigurieren, dass der Canvas den verfügbaren Platz einnimmt
	container.grid_rowconfigure(0, weight=1)
	container.grid_columnconfigure(0, weight=1)

	def _on_mousewheel(event):
		"""
		Beim Scrollen mit dem Mausrad soll der Inhalt des Canvas skaliert werden.
		Bei Windows wird event.delta verwendet, bei Linux die Button-Nummern.
		"""
		if event.delta:
			# Windows: event.delta > 0 bedeutet Scroll-up
			scale = 1.1 if event.delta > 0 else 0.9
		else:
			# Linux: Button 4 = scroll up, Button 5 = scroll down
			scale = 1.1 if event.num == 4 else 0.9
		# Zoom relativ zur Cursorposition
		canvas.scale("all", event.x, event.y, scale, scale)
		canvas.configure(scrollregion=canvas.bbox("all"))

	# Bindings für Windows und Linux (für Mausrad)
	canvas.bind("<MouseWheel>", _on_mousewheel)
	canvas.bind("<Button-4>", _on_mousewheel)
	canvas.bind("<Button-5>", _on_mousewheel)

	return canvas
