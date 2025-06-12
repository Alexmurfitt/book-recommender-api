# ✅ books_controller.py (optimizado con filtros mínimos y explicaciones robustas)

from fastapi import APIRouter, HTTPException
from book_recommender_api.app.models import FullProfile, RecommendationResponse, BookOut
from book_recommender_api.app.database import get_books_collection
from book_recommender_api.app.recommender import score_book, generate_explanation
import unicodedata


router = APIRouter()


# 🔹 Utilidad: normalización de texto
def normalize(text: str) -> str:
    if not text:
        return ""
    return unicodedata.normalize('NFKD', text.lower()).encode('ascii', 'ignore').decode('utf-8').strip()


def normalize_list(texts):
    return [normalize(t) for t in texts if t]


# 🔹 Limpieza de proyección para endpoint básico
def clean_projection(book):
    return {
        "title": book.get("title", "Sin título"),
        "author": book.get("author", "Desconocido")
    }


# 🔹 Endpoint: Lista básica de libros
@router.get("/books")
def list_books():
    books_col = get_books_collection()
    books = list(books_col.find({}, {"_id": 0, "title": 1, "author": 1}))
    return [clean_projection(book) for book in books]


# 🔹 Función auxiliar: filtro mínimo de coincidencias clave
def has_minimum_match(book, profile: FullProfile) -> bool:
    book_genres = normalize_list(book.get("genres", []))
    book_themes = normalize_list(book.get("themes", []))
    book_emotions = normalize_list(book.get("emotion_tags", []))

    profile_genres = normalize_list(profile.preferences.genres)
    profile_themes = normalize_list(profile.preferences.themes)
    profile_emotions = normalize_list(profile.preferences.emotion_tags)

    genre_match = bool(set(book_genres) & set(profile_genres))
    theme_match = bool(set(book_themes) & set(profile_themes))
    emotion_match = bool(set(book_emotions) & set(profile_emotions))

    # Exigimos al menos dos coincidencias clave (tema, emoción, género)
    return sum([genre_match, theme_match, emotion_match]) >= 2


# 🔹 Endpoint: Recomendación personalizada robusta
@router.post("/recommendation", response_model=RecommendationResponse)
def recommend(profile: FullProfile):
    books_col = get_books_collection()
    books = list(books_col.find({}, {"_id": 0}))

    if not books:
        raise HTTPException(status_code=404, detail="No hay libros disponibles para recomendar.")

    scored_books = []
    for book in books:
        if not has_minimum_match(book, profile):
            continue  # descartamos libros con baja afinidad

        score = score_book(book, profile)
        if score > 0:
            scored_books.append((book, score))

    if not scored_books:
        raise HTTPException(status_code=404, detail="Ningún libro coincide con tu perfil.")

    # Ordenar por score descendente
    scored_books.sort(key=lambda x: x[1], reverse=True)
    best_book, best_score = scored_books[0]
    explanation = generate_explanation(best_book, profile)

    return RecommendationResponse(
        recommendation=BookOut(**best_book),
        explanation=explanation
    )
