# utils/eliminar_duplicados_json.py
import json
import os
import shutil

BOOKS_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "books_openlibrary_enriched.json")
BACKUP_FILE = BOOKS_FILE.replace(".json", "_backup.json")

def eliminar_duplicados():
    with open(BOOKS_FILE, "r", encoding="utf-8") as f:
        libros_raw = json.load(f)

    # Aplanar listas anidadas si las hubiera
    libros = []
    for item in libros_raw:
        if isinstance(item, list):
            libros.extend(item)
        elif isinstance(item, dict):
            libros.append(item)

    libros_unicos = []
    vistos = set()

    for libro in libros:
        if not isinstance(libro, dict):
            continue
        title = libro.get("title", "").strip().lower()
        author = libro.get("author", "").strip().lower()
        if title and author:
            clave = (title, author)
            if clave not in vistos:
                libros_unicos.append(libro)
                vistos.add(clave)

    print(f"Antes: {len(libros)} libros")
    print(f"Después: {len(libros_unicos)} libros únicos")

    # Crear backup
    shutil.copy(BOOKS_FILE, BACKUP_FILE)
    print(f"Backup creado: {BACKUP_FILE}")

    # Guardar sin duplicados
    with open(BOOKS_FILE, "w", encoding="utf-8") as f:
        json.dump(libros_unicos, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    eliminar_duplicados()
