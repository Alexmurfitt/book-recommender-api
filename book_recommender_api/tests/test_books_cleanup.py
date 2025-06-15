# tests/test_books_cleanup.py

import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def test_books_fields_removed():
    """
    Verifica que no existan los campos 'language' ni 'year' en ningún documento de la colección 'books'.
    """
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    client = MongoClient(MONGO_URI)
    db = client["book_recommender"]
    books_col = db["books"]

    remaining = list(books_col.find(
        {"$or": [{"language": {"$exists": True}}, {"year": {"$exists": True}}]},
        {"_id": 1, "title": 1, "language": 1, "year": 1}
    ))

    assert len(remaining) == 0, f"❌ Aún existen libros con 'language' o 'year': {remaining}"


def test_no_pycache():
    """
    Verifica que no existan carpetas __pycache__ en el proyecto.
    """
    for root, dirs, _ in os.walk("."):
        for d in dirs:
            assert d != "__pycache__", f"❌ __pycache__ encontrada en {os.path.join(root, d)}"


def test_env_not_committed():
    """
    Verifica que el archivo .env esté correctamente listado en .gitignore.
    """
    # Ruta absoluta a la raíz del proyecto
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    gitignore_path = os.path.join(project_root, ".gitignore")

    assert os.path.exists(gitignore_path), f"❌ Falta archivo .gitignore en {project_root}"

    with open(gitignore_path, "r", encoding="utf-8") as f:
        gitignore_content = f.read()

    assert any(line.strip() in [".env", "*.env", "*.env.*"] for line in gitignore_content.splitlines()), \
        "❌ .env no está listado correctamente en .gitignore"
