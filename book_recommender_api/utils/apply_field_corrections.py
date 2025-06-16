import json
from pathlib import Path
from collections import defaultdict

# -----------------------------
# 📍 Rutas
# -----------------------------
base_path = Path(__file__).resolve().parents[1]
input_path = base_path / "data" / "books_openlibrary_enriched.json"
corrections_path = Path(__file__).resolve().parent / "field_options_corrected.json"
output_path = base_path / "data" / "books_openlibrary_corrected.json"

# -----------------------------
# 📥 Cargar archivos
# -----------------------------
with open(input_path, "r", encoding="utf-8") as f:
    books = json.load(f)

with open(corrections_path, "r", encoding="utf-8") as f:
    corrected_fields = json.load(f)

# -----------------------------
# 🧠 Construir diccionario de correcciones inverso
# -----------------------------
reverse_map = defaultdict(dict)

for field, corrected_list in corrected_fields.items():
    for correct_value in corrected_list:
        reverse_map[field][correct_value] = correct_value  # valor correcto mapeado a sí mismo

    # Generar mapping inverso desde posibles errores al valor corregido
    originals = set()
    for book in books:
        val = book.get(field)
        if isinstance(val, list):
            originals.update(val)
        elif isinstance(val, str):
            originals.add(val)

    for original in originals:
        for correct_value in corrected_list:
            if original != correct_value and original.casefold() == correct_value.casefold():
                reverse_map[field][original] = correct_value

# -----------------------------
# 🧹 Aplicar correcciones
# -----------------------------
corrected_books = []
modification_count = defaultdict(int)

for book in books:
    corrected_book = book.copy()

    for field, mapping in reverse_map.items():
        original = corrected_book.get(field)

        if isinstance(original, list):
            new_values = [mapping.get(v, v) for v in original]
            if new_values != original:
                corrected_book[field] = sorted(set(new_values))
                modification_count[field] += 1

        elif isinstance(original, str):
            new_value = mapping.get(original, original)
            if new_value != original:
                corrected_book[field] = new_value
                modification_count[field] += 1

    corrected_books.append(corrected_book)

# -----------------------------
# 💾 Guardar archivo corregido
# -----------------------------
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(corrected_books, f, ensure_ascii=False, indent=2)

# -----------------------------
# 📊 Reporte final
# -----------------------------
print("✅ Correcciones aplicadas con éxito.")
print(f"📁 Archivo generado: {output_path.name}\n")

for field, count in modification_count.items():
    print(f"🔧 Campo '{field}': {count} registros modificados")
