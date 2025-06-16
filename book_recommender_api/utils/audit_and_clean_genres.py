import json
import re
import os

# -------------------------------
# 📥 Cargar dataset original
# -------------------------------
DATASET_PATH = "../data/books_openlibrary_enriched.json"
with open(DATASET_PATH, "r", encoding="utf-8") as f:
    books = json.load(f)

# -------------------------------
# 📘 Leer géneros válidos desde .md
# -------------------------------
GENRES_MD_PATH = "../genres_classification.md"
with open(GENRES_MD_PATH, "r", encoding="utf-8") as f:
    md_text = f.read()

# -------------------------------
# 🧠 Extraer lista jerárquica de géneros válidos
# -------------------------------
def extract_genres_from_md(text):
    valid_genres = set()
    lines = text.splitlines()
    bullet_regex = re.compile(r"^[\-\*\+●\d]+\s+(.*)$")
    skip_headers = {"Ficción", "No Ficción", "Poesía", "Teatro", "Cómic", "Géneros Especiales o Cruzados"}
    for line in lines:
        line = line.strip()
        if not line or any(line.startswith(prefix) for prefix in ["#", "*", ">"]):
            continue
        if any(header.lower() in line.lower() for header in skip_headers):
            continue
        match = bullet_regex.match(line)
        if match:
            genre = match.group(1).strip()
            # Normalizamos
            genre = re.sub(r"\(.*?\)", "", genre).strip().lower()
            valid_genres.add(genre)
        elif len(line.split()) <= 4:  # línea corta potencialmente relevante
            genre = line.strip().lower()
            valid_genres.add(genre)
    return valid_genres

valid_genres = extract_genres_from_md(md_text)

# -------------------------------
# 🧹 Auditoría y limpieza
# -------------------------------
def clean_genre(genre):
    return genre.strip().lower()

total_modified = 0
for book in books:
    original_genres = book.get("genres", [])
    if isinstance(original_genres, str):
        original_genres = [original_genres]

    cleaned_genres = []
    for g in original_genres:
        g_clean = clean_genre(g)
        if g_clean in valid_genres:
            cleaned_genres.append(g_clean)

    if cleaned_genres != original_genres:
        book["genres"] = cleaned_genres
        total_modified += 1

# -------------------------------
# 💾 Guardar nuevo archivo limpio
# -------------------------------
OUTPUT_PATH = "books_openlibrary_cleaned.json"
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(books, f, indent=2, ensure_ascii=False)

# -------------------------------
# ✅ Reporte final
# -------------------------------
print("✅ Proceso completado con éxito.")
print(f"📁 Archivo generado: {OUTPUT_PATH}")
print(f"🔍 Registros modificados: {total_modified}")
print(f"📚 Géneros válidos reconocidos: {len(valid_genres)}")
