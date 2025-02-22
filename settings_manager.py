# settings_manager.py
import json
import os
from tkinter import messagebox
from utils import get_program_path

def load_settings(file_name="settings.json"):
    prog_path = get_program_path()
    settings_file = os.path.join(prog_path, file_name)
    if os.path.exists(settings_file):
        try:
            with open(settings_file, "r") as f:
                settings = json.load(f)
            return settings
        except Exception as e:
            messagebox.showerror("Fehler", f"Einstellungen konnten nicht geladen werden: {str(e)}")
    else:
        messagebox.showwarning("Einstellungen nicht gefunden", "Die Datei settings.json wurde nicht gefunden.")
    return {}

def save_settings(settings, file_name="settings.json"):
    prog_path = get_program_path()
    file_path = os.path.join(prog_path, file_name)
    try:
        with open(file_path, "w") as f:
            json.dump(settings, f, indent=4)
        return file_path
    except Exception as e:
        messagebox.showerror("Fehler", f"Speichern fehlgeschlagen: {str(e)}")
        return None
