# ✅ utils/field_loader.py

import json
import unicodedata
import re
from pathlib import Path
from collections import defaultdict
import os

# 📁 Ruta del archivo limpio (actualizado con géneros válidos)

# ---------------------------
# 🔧 Normalización
# ---------------------------
def normalize(text):
    if not isinstance(text, str):
        return None
    text = unicodedata.normalize("NFKD", text).casefold()
    text = re.sub(r"[\s\-_/]+", " ", text)
    text = re.sub(r"[^\w\s]", "", text)
    return text.strip()

def normalize_list(values):
    return [normalize(v) for v in values if normalize(v)]

# ---------------------------
# 📥 Cargar archivo limpio
# ---------------------------
DATASET_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/books_openlibrary_cleaned.json"))
def load_field_options():
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        books = json.load(f)

    fields = defaultdict(set)

    for book in books:
        for key in ["genres", "themes", "tone", "style", "emotion_tags", "age_range", "language"]:
            value = book.get(key)
            if isinstance(value, list):
                fields[key].update(normalize_list(value))
            elif isinstance(value, str):
                norm = normalize(value)
                if norm:
                    fields[key].add(norm)

    return {k: sorted(v) for k, v in fields.items()}
