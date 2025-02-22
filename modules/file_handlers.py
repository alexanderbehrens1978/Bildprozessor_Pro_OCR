import os
from tkinter import filedialog, messagebox
from PIL import Image
from pdf2image import convert_from_path
from modules.poppler_manager import get_poppler_path

def load_image_file(app_instance):
    file_path = filedialog.askopenfilename(
        filetypes=[("Bilder/PDFs", "*.png;*.jpg;*.jpeg;*.pdf"), ("Alle Dateien", "*.*")]
    )
    if file_path:
        try:
            if file_path.lower().endswith(".pdf"):
                current_poppler_path = get_poppler_path(app_instance.poppler_path)
                if not current_poppler_path:
                    messagebox.showerror("Fehler", "Poppler Pfad ist nicht gesetzt. Bitte setze den Pfad unter 'Einstellungen'.")
                    return
                pages = convert_from_path(file_path, dpi=200, poppler_path=current_poppler_path)
                app_instance.original_image = pages[0]
            else:
                app_instance.original_image = Image.open(file_path).convert("RGB")
            app_instance.filename = os.path.basename(file_path)
            app_instance.filename_label.config(text=app_instance.filename)
            from modules.image_ops import show_image_op, update_image_op
            if app_instance.left_canvas:
                show_image_op(app_instance.original_image, app_instance.left_canvas)
            update_image_op(app_instance)
        except Exception as e:
            messagebox.showerror("Fehler", f"Konnte Bild laden: {str(e)}")

def save_image_file(app_instance):
    if app_instance.processed_image:
        filter_info = []
        for i, (enabled_var, filter_var, strength_var) in enumerate(app_instance.layer_vars):
            if enabled_var.get():
                filter_info.append(f"{i+1}_{filter_var.get()}_{strength_var.get():.2f}")
        default_name = ""
        if app_instance.filename:
            base = os.path.splitext(app_instance.filename)[0]
            default_name = f"{base}_" + "_".join(filter_info) if filter_info else base
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("Alle Dateien", "*.*")],
            title="Bild speichern",
            initialfile=default_name
        )
        if file_path:
            try:
                app_instance.processed_image.save(file_path)
                messagebox.showinfo("Erfolg", "Bild erfolgreich gespeichert.")
            except Exception as e:
                messagebox.showerror("Fehler", f"Speichern fehlgeschlagen: {str(e)}")
