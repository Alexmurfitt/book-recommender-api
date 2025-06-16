# ✅ utils/normalize_and_clean_genres.py
import json
import os
import re
import unicodedata
from pathlib import Path

# ---------------------------
# 📍 Rutas
# ---------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "books_openlibrary_enriched.json"
TAXONOMY_PATH = BASE_DIR / "genres_classification.md"
OUTPUT_PATH = BASE_DIR / "data" / "books_openlibrary_cleaned.json"

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

# ---------------------------
# 📘 Extraer géneros válidos
# ---------------------------
def extract_valid_genres(md_text):
    valid_genres = set()
    bullet_regex = re.compile(r"^[\-\*\+\d\u2022]+\s+(.*)$")
    skip_headers = {"Ficción", "No Ficción", "Poesía", "Teatro", "Cómic", "Géneros Especiales o Cruzados"}
    
    for line in md_text.splitlines():
        line = line.strip()
        if not line or any(line.startswith(prefix) for prefix in ["#", ">"]):
            continue
        if any(h.lower() in line.lower() for h in skip_headers):
            continue
        match = bullet_regex.match(line)
        if match:
            genre = match.group(1).strip()
            norm = normalize(genre)
            if norm:
                valid_genres.add(norm)
        elif len(line.split()) <= 4:
            norm = normalize(line)
            if norm:
                valid_genres.add(norm)
    return valid_genres

# ---------------------------
# 🧹 Limpieza del dataset
# ---------------------------
def clean_dataset():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        books = json.load(f)

    with open(TAXONOMY_PATH, "r", encoding="utf-8") as f:
        taxonomy = f.read()

    valid_genres = extract_valid_genres(taxonomy)
    total_modified = 0

    for book in books:
        raw_genres = book.get("genres", [])
        if isinstance(raw_genres, str):
            raw_genres = [raw_genres]

        cleaned = [normalize(g) for g in raw_genres if normalize(g) in valid_genres]

        if cleaned != raw_genres:
            book["genres"] = cleaned
            total_modified += 1

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(books, f, indent=2, ensure_ascii=False)

    print("✅ Dataset limpiado y normalizado correctamente.")
    print(f"📁 Archivo guardado: {OUTPUT_PATH}")
    print(f"🔍 Registros modificados: {total_modified}")
    print(f"📚 Géneros válidos usados: {len(valid_genres)}")

# ---------------------------
# 🚀 Ejecutar
# ---------------------------
if __name__ == "__main__":
    clean_dataset()
