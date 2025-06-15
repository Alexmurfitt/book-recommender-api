# utils/field_loader.py
import json
import os

def load_field_options():
    base_dir = os.path.dirname(__file__)
    json_path = os.path.join(base_dir, "field_options.json")
    with open("utils/field_options.json", "r", encoding="utf-8") as f:
        return json.load(f)


