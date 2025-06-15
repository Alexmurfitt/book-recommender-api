# utils/field_loader.py
import json
import os

def load_field_options():
    base_path = os.path.dirname(__file__)  # Ruta absoluta del archivo actual (field_loader.py)
    file_path = os.path.join(base_path, "field_options.json")

    with open(file_path, "r", encoding="utf-8") as f:
        options = json.load(f)
    return options


