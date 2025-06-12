# app/recommender.py

from typing import Dict, List
from .models import FullProfile, BookOut
import unicodedata

# ---------------------
# 🔹 UTILIDAD: Normalización de texto
# ---------------------

def normalize(text: str) -> str:
    if not text:
        return ""
    return unicodedata.normalize('NFKD', text.lower()).encode('ASCII', 'ignore').decode('utf-8').strip()


def normalize_list(texts: List[str]) -> List[str]:
    return [normalize(t) for t in texts if t]


# ---------------------
# 🔹 SCORE CALCULATION
# ---------------------

def compute_score(profile: FullProfile, book: Dict) -> float:
    preferences = profile.preferences

    # Normalización
    book_genres = normalize_list(book.get("genres", []))
    book_themes = normalize_list(book.get("themes", []))
    book_emotions = normalize_list(book.get("emotion_tags", []))
    book_tone = normalize(book.get("tone"))
    book_style = normalize(book.get("style"))
    book_personality = book.get("personality_match", [])
    book_age = normalize(book.get("age_range"))

    profile_genres = normalize_list(preferences.genres)
    profile_themes = normalize_list(preferences.themes)
    profile_emotions = normalize_list(preferences.emotion_tags)
    profile_tone = normalize(preferences.tone)
    profile_style = normalize(preferences.style)
    profile_age = normalize(preferences.age_range)

    # Coincidencias clave
    genre_match = len(set(book_genres) & set(profile_genres))
    theme_match = len(set(book_themes) & set(profile_themes))
    emotion_match = len(set(book_emotions) & set(profile_emotions))

    genre_score = genre_match / max(len(profile_genres), 1) if genre_match > 0 else 0
    theme_score = theme_match / max(len(profile_themes), 1) if theme_match > 0 else 0
    emotion_score = emotion_match / max(len(profile_emotions), 1) if emotion_match > 0 else 0

    tone_match = 1.0 if book_tone == profile_tone else 0.0
    style_match = 1.0 if book_style == profile_style else 0.0
    age_match = 1.0 if book_age == profile_age else 0.0

    personality_score = match_personality(profile.personality, book_personality)

    # Ponderación reajustada
    score = (
        0.25 * theme_score +
        0.25 * emotion_score +
        0.20 * genre_score +
        0.15 * tone_match +
        0.05 * (style_match + age_match) / 2 +
        0.10 * personality_score
    )

    return round(score, 4)


# ---------------------
# 🔹 PERSONALITY MATCH
# ---------------------

def match_personality(personality: Dict, tags: list) -> float:
    score = 0
    if not tags:
        return 0.0

    for tag in tags:
        if "Alta apertura" in tag and personality.O >= 60:
            score += 1
        elif "Baja apertura" in tag and personality.O <= 40:
            score += 1
        elif "Alta responsabilidad" in tag and personality.C >= 60:
            score += 1
        elif "Baja responsabilidad" in tag and personality.C <= 40:
            score += 1
        elif "Alta extraversión" in tag and personality.E >= 60:
            score += 1
        elif "Baja extraversión" in tag and personality.E <= 40:
            score += 1
        elif "Alta amabilidad" in tag and personality.A >= 60:
            score += 1
        elif "Baja amabilidad" in tag and personality.A <= 40:
            score += 1
        elif "Alto neuroticismo" in tag and personality.N >= 60:
            score += 1
        elif "Bajo neuroticismo" in tag and personality.N <= 40:
            score += 1

    return round(score / len(tags), 4)


# ---------------------
# 🔹 EXPLANATION (mejorada)
# ---------------------

def generate_explanation(book: Dict, profile: FullProfile) -> str:
    matched = []

    if set(normalize_list(book.get("genres", []))) & set(normalize_list(profile.preferences.genres)):
        matched.append("géneros favoritos")
    if set(normalize_list(book.get("themes", []))) & set(normalize_list(profile.preferences.themes)):
        matched.append("temas importantes")
    if set(normalize_list(book.get("emotion_tags", []))) & set(normalize_list(profile.preferences.emotion_tags)):
        matched.append("emociones evocadas")
    if normalize(book.get("tone")) == normalize(profile.preferences.tone):
        matched.append("tono narrativo")
    if normalize(book.get("style")) == normalize(profile.preferences.style):
        matched.append("estilo literario")

    if matched:
        explanation = f"Este libro fue seleccionado por coincidir con tus " + ", ".join(matched) + "."
    else:
        explanation = "Este libro fue sugerido por su afinidad general con tu perfil lector."

    return explanation


# ---------------------
# 🔹 PUBLIC INTERFACE
# ---------------------

def score_book(book: Dict, profile: FullProfile) -> float:
    return compute_score(profile, book)
