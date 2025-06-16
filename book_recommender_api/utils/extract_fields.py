import json
import unicodedata
import re
from pathlib import Path
from collections import defaultdict

# ------------------------------
# 🔧 Funciones de normalización
# ------------------------------

def normalize(text):
    if not isinstance(text, str):
        return None
    text = unicodedata.normalize("NFKD", text).casefold()
    text = re.sub(r"[\s\-_/]+", " ", text)  # Unifica separadores
    text = re.sub(r"[^\w\s]", "", text)     # Elimina puntuación
    text = text.strip()
    return text if text not in {"", "n/a", "na", "null", "none"} else None

def normalize_list(values):
    if not isinstance(values, list):
        return []
    return [normalize(v) for v in values if normalize(v)]

# ------------------------------
# 📥 Cargar libros
# ------------------------------

file_path = Path(__file__).resolve().parents[1] / "data" / "books_openlibrary_enriched.json"
with open(file_path, "r", encoding="utf-8") as f:
    books = json.load(f)

# ------------------------------
# 📊 Inicializar contenedores
# ------------------------------

field_sets = defaultdict(set)
anomalies = []

# Campos objetivo
fields_list = [
    "genres", "subgenres", "themes", "emotion_tags", 
    "tone", "style", "age_range", "language"
]

# ------------------------------
# 🔍 Recorrer libros y extraer campos
# ------------------------------

for i, book in enumerate(books):
    for field in fields_list:
        value = book.get(field)

        if isinstance(value, list):
            cleaned = normalize_list(value)
            if not cleaned:
                anomalies.append((i, field, "LISTA VACÍA O MAL FORMADA"))
            field_sets[field].update(cleaned)

        elif isinstance(value, str):
            norm = normalize(value)
            if not norm:
                anomalies.append((i, field, "CADENA VACÍA O INVÁLIDA"))
            else:
                field_sets[field].add(norm)

        elif value is None:
            anomalies.append((i, field, "VALOR AUSENTE"))

        else:
            anomalies.append((i, field, f"TIPO INVÁLIDO: {type(value)}"))

# ------------------------------
# 💾 Guardar resultados
# ------------------------------

output_path = Path(__file__).resolve().parent / "field_options_cleaned.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump({k: sorted(list(v)) for k, v in field_sets.items()}, f, ensure_ascii=False, indent=2)

# ------------------------------
# 📋 Imprimir resumen riguroso
# ------------------------------

for field in fields_list:
    print(f"\n📌 {field.upper()} ({len(field_sets[field])} únicos):")
    for v in sorted(field_sets[field]):
        print(f"  - {v}")

if anomalies:
    print("\n⚠️ ANOMALÍAS DETECTADAS:")
    for idx, field, issue in anomalies:
        print(f"  - Libro #{idx} | Campo '{field}': {issue}")
else:
    print("\n✅ Sin anomalías detectadas.")
# ------------------------------
# 📝 Guardar resumen en TXT
# ------------------------------

txt_output_path = Path(__file__).resolve().parent / "extract_fields.txt"
with open(txt_output_path, "w", encoding="utf-8") as f:
    for field in fields_list:
        f.write(f"\n📌 {field.upper()} ({len(field_sets[field])} únicos):\n")
        for v in sorted(field_sets[field]):
            f.write(f"  - {v}\n")

    if anomalies:
        f.write("\n⚠️ ANOMALÍAS DETECTADAS:\n")
        for idx, field, issue in anomalies:
            f.write(f"  - Libro #{idx} | Campo '{field}': {issue}\n")
    else:
        f.write("\n✅ Sin anomalías detectadas.\n")
