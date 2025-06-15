# utils/analyze_books_tags.py
from book_recommender_api.app.database import get_books_collection
from collections import Counter
import pprint

def extract_tags():
    books_col = get_books_collection()
    books = list(books_col.find({}, {"genres": 1, "themes": 1, "emotion_tags": 1}))
    
    genres = Counter()
    themes = Counter()
    emotions = Counter()

    for book in books:
        genres.update(book.get("genres", []))
        themes.update(book.get("themes", []))
        emotions.update(book.get("emotion_tags", []))

    print("\n📚 GÉNEROS MÁS COMUNES:")
    pprint.pprint(genres.most_common(10))
    print("\n🎭 TEMAS MÁS COMUNES:")
    pprint.pprint(themes.most_common(10))
    print("\n💫 EMOCIONES MÁS COMUNES:")
    pprint.pprint(emotions.most_common(10))

if __name__ == "__main__":
    extract_tags()
