# poppler_manager.py
import os
import sys
import subprocess
from tkinter import messagebox, Toplevel, Label, Entry, Button
from utils import get_program_path


def get_poppler_path(user_defined_path=""):
	"""
	Gibt den Poppler-Pfad zurück, abhängig davon, ob das Skript als EXE läuft oder nicht.

	:param user_defined_path: Vom Benutzer gesetzter Pfad (falls vorhanden).
	:return: Pfad zu den Poppler-Binärdateien oder ein leerer String, falls nicht gefunden.
	"""
	if getattr(sys, 'frozen', False):
		return os.path.join(sys._MEIPASS, "poppler_bin", "bin")
	else:
		auto_path = os.path.join(get_program_path(), "poppler_bin", "bin")
		if os.path.exists(auto_path):
			return auto_path
		if user_defined_path and os.path.exists(user_defined_path):
			return user_defined_path
		return ""


def install_poppler():
	"""
	Versucht, Poppler automatisch zu installieren, abhängig vom Betriebssystem.
	Bei Windows wird Chocolatey genutzt, bei Linux apt-get und bei macOS Homebrew.
	Falls die benötigten Paketmanager nicht verfügbar sind, wird eine entsprechende Meldung angezeigt.
	"""
	try:
		if sys.platform.startswith("win"):
			try:
				subprocess.check_call(["choco", "--version"],
									  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
			except Exception:
				show_poppler_url()
				return
			subprocess.check_call(["choco", "install", "poppler", "-y"])
			messagebox.showinfo("Poppler Installation", "Poppler wurde erfolgreich installiert.")
		elif sys.platform.startswith("linux"):
			subprocess.check_call(["sudo", "apt-get", "install", "poppler-utils", "-y"])
			messagebox.showinfo("Poppler Installation", "Poppler wurde erfolgreich installiert.")
		elif sys.platform.startswith("darwin"):
			try:
				subprocess.check_call(["brew", "--version"],
									  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
			except Exception:
				messagebox.showerror("Fehler", "Homebrew ist nicht installiert.\n"
											   "Bitte installiere Homebrew oder installiere Poppler manuell.")
				return
			subprocess.check_call(["brew", "install", "poppler"])
			messagebox.showinfo("Poppler Installation", "Poppler wurde erfolgreich installiert.")
		else:
			messagebox.showerror("Fehler",
								 "Automatische Installation von Poppler wird für dein Betriebssystem nicht unterstützt.\n"
								 "Bitte installiere Poppler manuell.")
	except Exception as e:
		messagebox.showerror("Fehler", f"Fehler bei der Installation von Poppler: {str(e)}")


def show_poppler_url():
	"""
	Öffnet ein kleines Fenster mit dem Download-Link für Poppler, falls Chocolatey nicht installiert ist.
	"""
	top = Toplevel()
	top.title("Poppler Download URL")
	Label(top,
		  text="Chocolatey ist nicht installiert.\n"
			   "Bitte installiere Chocolatey oder installiere Poppler manuell.\n"
			   "Kopiere folgenden Link für den Download:",
		  justify="left").pack(padx=10, pady=10)
	url = "https://github.com/oschwartz10612/poppler-windows/releases/"
	entry = Entry(top, width=60)
	entry.insert(0, url)
	entry.pack(padx=10, pady=5)
	Button(top, text="Schließen", command=top.destroy).pack(pady=10)
