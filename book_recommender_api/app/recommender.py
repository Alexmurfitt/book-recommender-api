from typing import Dict, List
from .models import FullProfile
import unicodedata

# -------------------------
# 🔹 UTILIDAD: Normalización
# -------------------------

def normalize(text: str) -> str:
    if not text:
        return ""
    return unicodedata.normalize('NFKD', text.lower()).encode('ASCII', 'ignore').decode('utf-8').strip()


def normalize_list(texts: List[str]) -> List[str]:
    return [normalize(t) for t in texts if t]


# -------------------------
# 🔹 SCORE CALCULATION
# -------------------------

def compute_score(profile: FullProfile, book: Dict) -> float:
    prefs = profile.preferences

    # Normalización
    book_genres = normalize_list(book.get("genres", []))
    book_themes = normalize_list(book.get("themes", []))
    book_emotions = normalize_list(book.get("emotion_tags", []))
    book_tone = normalize(book.get("tone"))
    book_style = normalize(book.get("style"))
    book_age = normalize(book.get("age_range"))
    book_personality = book.get("personality_match", [])

    user_genres = normalize_list(prefs.genres)
    user_themes = normalize_list(prefs.themes)
    user_emotions = normalize_list(prefs.emotion_tags)
    user_tone = normalize(prefs.tone)
    user_style = normalize(prefs.style)
    user_age = normalize(prefs.age_range)

    # Coincidencias
    genre_score = len(set(book_genres) & set(user_genres)) / max(len(user_genres), 1)
    theme_score = len(set(book_themes) & set(user_themes)) / max(len(user_themes), 1)
    emotion_score = len(set(book_emotions) & set(user_emotions)) / max(len(user_emotions), 1)
    tone_score = 1.0 if book_tone and book_tone == user_tone else 0.0
    style_score = 1.0 if book_style and book_style == user_style else 0.0
    age_score = 1.0 if book_age and book_age == user_age else 0.0
    personality_score = match_personality(profile.personality, book_personality)

    # Ponderación ajustada (tema y emoción tienen más peso)
    score = (
        0.25 * theme_score +
        0.25 * emotion_score +
        0.20 * genre_score +
        0.15 * tone_score +
        0.05 * (style_score + age_score) / 2 +
        0.10 * personality_score
    )

    return round(score, 4)


# -------------------------
# 🔹 PERSONALITY MATCH
# -------------------------

def match_personality(personality: Dict, tags: list) -> float:
    if not tags:
        return 0.0

    matched = 0
    for tag in tags:
        if "Alta apertura" in tag and personality.O >= 60:
            matched += 1
        elif "Baja apertura" in tag and personality.O <= 40:
            matched += 1
        elif "Alta responsabilidad" in tag and personality.C >= 60:
            matched += 1
        elif "Baja responsabilidad" in tag and personality.C <= 40:
            matched += 1
        elif "Alta extraversión" in tag and personality.E >= 60:
            matched += 1
        elif "Baja extraversión" in tag and personality.E <= 40:
            matched += 1
        elif "Alta amabilidad" in tag and personality.A >= 60:
            matched += 1
        elif "Baja amabilidad" in tag and personality.A <= 40:
            matched += 1
        elif "Alto neuroticismo" in tag and personality.N >= 60:
            matched += 1
        elif "Bajo neuroticismo" in tag and personality.N <= 40:
            matched += 1

    return round(matched / len(tags), 4)


# -------------------------
# 🔹 EXPLICACIÓN PERSONALIZADA
# -------------------------

def generate_explanation(book: Dict, profile: FullProfile) -> str:
    prefs = profile.preferences
    explanation_parts = []

    if set(normalize_list(book.get("genres", []))) & set(normalize_list(prefs.genres)):
        explanation_parts.append("géneros favoritos")
    if set(normalize_list(book.get("themes", []))) & set(normalize_list(prefs.themes)):
        explanation_parts.append("temas como los que te interesan")
    if set(normalize_list(book.get("emotion_tags", []))) & set(normalize_list(prefs.emotion_tags)):
        explanation_parts.append("emociones que valoras")
    if normalize(book.get("tone")) == normalize(prefs.tone):
        explanation_parts.append("tono narrativo afín")
    if normalize(book.get("style")) == normalize(prefs.style):
        explanation_parts.append("estilo literario similar")

    if explanation_parts:
        joined = ", ".join(explanation_parts[:-1]) + " y " + explanation_parts[-1] if len(explanation_parts) > 1 else explanation_parts[0]
        return f"Este libro fue seleccionado por su coincidencia con tus {joined}."
    else:
        return "Este libro fue sugerido por su afinidad general con tu perfil lector."


# -------------------------
# 🔹 INTERFAZ PÚBLICA
# -------------------------

def score_book(book: Dict, profile: FullProfile) -> float:
    return compute_score(profile, book)
