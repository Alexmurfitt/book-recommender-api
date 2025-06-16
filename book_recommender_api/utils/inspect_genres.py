# utils/inspect_genres.py
import json
from collections import Counter
from pathlib import Path

DATASET_PATH = Path(__file__).resolve().parent.parent / "data" / "books_openlibrary_cleaned.json"

with open(DATASET_PATH, "r", encoding="utf-8") as f:
    books = json.load(f)

all_genres = []
for book in books:
    g = book.get("genres", [])
    if isinstance(g, str):
        g = [g]
    all_genres.extend(g)

counter = Counter(all_genres)
print(f"✅ Géneros únicos encontrados: {len(counter)}\n")
for genre, count in counter.most_common():
    print(f"- {genre} ({count})")
