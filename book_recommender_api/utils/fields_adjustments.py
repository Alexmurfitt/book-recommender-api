import json
import unicodedata
import re
from pathlib import Path
from collections import defaultdict
from difflib import get_close_matches

# ------------------------------
# 🔧 Utilidades de Normalización
# ------------------------------

def normalize(text):
    if not text or not isinstance(text, str):
        return None
    text = unicodedata.normalize("NFKD", text).casefold()
    text = re.sub(r"[\s\-_/]+", " ", text)           # Unifica separadores
    text = re.sub(r"[^\w\s]", "", text)              # Elimina puntuación
    text = text.strip()
    return text if text not in {"", "n/a", "na", "null", "none"} else None

def normalize_list(values):
    if not isinstance(values, list):
        return []
    return [normalize(v) for v in values if normalize(v)]

# ------------------------------
# 📥 Cargar archivo JSON de libros
# ------------------------------

file_path = Path(__file__).resolve().parents[1] / "data" / "books_openlibrary_enriched.json"
with open(file_path, "r", encoding="utf-8") as f:
    books = json.load(f)

# ------------------------------
# 📊 Inicializar campos únicos y anomalías
# ------------------------------

field_values = defaultdict(set)
anomalies = []
fields_list = [
    "genres", "subgenres", "themes", "emotion_tags", 
    "tone", "style", "age_range", "language"
]

# ------------------------------
# 🔍 Analizar y normalizar campos
# ------------------------------

for i, book in enumerate(books):
    for field in fields_list:
        value = book.get(field)
        
        if isinstance(value, list):
            norm_values = normalize_list(value)
            if not norm_values:
                anomalies.append((i, field, "LISTA VACÍA O INVÁLIDA"))
            field_values[field].update(norm_values)

        elif isinstance(value, str):
            norm_value = normalize(value)
            if not norm_value:
                anomalies.append((i, field, "STRING VACÍO O INVÁLIDO"))
            else:
                field_values[field].add(norm_value)

        elif value is None:
            anomalies.append((i, field, "VALOR AUSENTE"))

        else:
            anomalies.append((i, field, f"TIPO INESPERADO: {type(value)}"))

# ------------------------------
# 💾 Guardar resultados limpios
# ------------------------------

output_json = Path(__file__).resolve().parent / "field_options_cleaned.json"
with open(output_json, "w", encoding="utf-8") as f:
    json.dump({k: sorted(list(v)) for k, v in field_values.items()}, f, ensure_ascii=False, indent=2)

# Guardar como txt por campo
fields_dir = Path(__file__).resolve().parent / "fields_cleaned"
fields_dir.mkdir(exist_ok=True)

for field, values in field_values.items():
    with open(fields_dir / f"{field}.txt", "w", encoding="utf-8") as f:
        for val in sorted(values):
            f.write(f"{val}\n")

# Guardar anomalías
anomalies_path = Path(__file__).resolve().parent / "anomalies.txt"
with open(anomalies_path, "w", encoding="utf-8") as f:
    for idx, field, issue in anomalies:
        f.write(f"Libro #{idx} | Campo '{field}': {issue}\n")

# ------------------------------
# 🔍 Detección de posibles duplicados
# ------------------------------

for field, values in field_values.items():
    sorted_vals = sorted(values)
    for i, val in enumerate(sorted_vals):
        matches = get_close_matches(val, sorted_vals, n=3, cutoff=0.85)
        if len(matches) > 1:
            print(f"🔍 Posibles duplicados en '{field}': {matches}")

# ------------------------------
# 📋 Imprimir resumen en consola
# ------------------------------

for field, values in field_values.items():
    print(f"\n📌 {field.upper()} ({len(values)} únicos):")
    for v in sorted(values):
        print(f"  - {v}")

if anomalies:
    print("\n⚠️ ANOMALÍAS DETECTADAS:")
    for idx, field, issue in anomalies:
        print(f"  - Libro #{idx} | Campo '{field}': {issue}")
else:
    print("\n✅ Sin anomalías detectadas.")
