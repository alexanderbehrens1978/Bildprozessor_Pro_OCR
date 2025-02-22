import os
import sys

def get_program_path():
    """Gibt den Ordner zurück, in dem die EXE liegt (bei gebündelter Anwendung)
    oder in dem das Skript liegt."""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))
