# utils/comparar_backup_eliminados.py
import json
import os

FILE_ACTUAL = os.path.join(os.path.dirname(__file__), "..", "data", "books_openlibrary_enriched.json")
FILE_BACKUP = os.path.join(os.path.dirname(__file__), "..", "data", "books_openlibrary_enriched_backup.json")

def comparar_libros():
    with open(FILE_BACKUP, "r", encoding="utf-8") as f:
        libros_backup = json.load(f)

    with open(FILE_ACTUAL, "r", encoding="utf-8") as f:
        libros_actuales = json.load(f)

    def clave(libro):
        return (libro.get("title", "").strip().lower(), libro.get("author", "").strip().lower())

    claves_actuales = set(clave(libro) for libro in libros_actuales if isinstance(libro, dict))
    eliminados = [libro for libro in libros_backup if isinstance(libro, dict) and clave(libro) not in claves_actuales]

    print(f"📚 Libros eliminados: {len(eliminados)}")
    for libro in eliminados:
        print(f"- {libro.get('title')} | {libro.get('author')}")

if __name__ == "__main__":
    comparar_libros()
