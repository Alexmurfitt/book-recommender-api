from typing import Dict, List
from .models import FullProfile
import unicodedata
import re

# -------------------------
# 🔹 CONSTANTES DE PONDERACIÓN
# -------------------------

WEIGHTS = {
    'themes': 0.25,
    'emotion_tags': 0.25,
    'genres': 0.20,
    'tone': 0.15,
    'style': 0.05,
    'age_range': 0.00,  # Solo como filtro
    'personality_match': 0.10
}

# -------------------------
# 🔹 UTILIDADES DE NORMALIZACIÓN
# -------------------------

def normalize(text: str) -> str:
    if not text:
        return ""
    text = unicodedata.normalize('NFKD', text.casefold())
    text = text.encode('ascii', 'ignore').decode('utf-8')
    text = re.sub(r'[^\w\s]', '', text)
    return text.strip()

def normalize_list(texts: List[str]) -> List[str]:
    return [normalize(t) for t in texts if t]


# -------------------------
# 🔹 CÁLCULO DE COINCIDENCIA
# -------------------------

def compute_score(profile: FullProfile, book: Dict) -> float:
    prefs = profile.preferences

    # Normalización de campos del libro
    book_data = {
        'genres': normalize_list(book.get("genres", [])),
        'themes': normalize_list(book.get("themes", [])),
        'emotion_tags': normalize_list(book.get("emotion_tags", [])),
        'tone': normalize(book.get("tone")),
        'style': normalize(book.get("style")),
        'age_range': normalize(book.get("age_range")),
        'personality_match': book.get("personality_match", [])
    }

    # Normalización del perfil del usuario
    user_data = {
        'genres': normalize_list(prefs.genres),
        'themes': normalize_list(prefs.themes),
        'emotion_tags': normalize_list(prefs.emotion_tags),
        'tone': normalize(prefs.tone),
        'style': normalize(prefs.style),
        'age_range': normalize(prefs.age_range)
    }

    # Similaridad por campos (Jaccard para listas)
    def jaccard(list1, list2):
        return len(set(list1) & set(list2)) / max(len(set(list2)), 1)

    scores = {
        'genres': jaccard(book_data['genres'], user_data['genres']),
        'themes': jaccard(book_data['themes'], user_data['themes']),
        'emotion_tags': jaccard(book_data['emotion_tags'], user_data['emotion_tags']),
        'tone': 1.0 if book_data['tone'] and book_data['tone'] == user_data['tone'] else 0.0,
        'style': 1.0 if book_data['style'] and book_data['style'] == user_data['style'] else 0.0,
        'age_range': 1.0 if book_data['age_range'] and book_data['age_range'] == user_data['age_range'] else 0.0,
        'personality_match': match_personality(profile.personality, book_data['personality_match'])
    }

    # Ponderación final
    score = sum(scores[key] * WEIGHTS[key] for key in WEIGHTS)
    return round(score, 4)


# -------------------------
# 🔹 PERSONALITY MATCH AVANZADO
# -------------------------

RULES = {
    "alta apertura": lambda p: p.O >= 60,
    "baja apertura": lambda p: p.O <= 40,
    "alta responsabilidad": lambda p: p.C >= 60,
    "baja responsabilidad": lambda p: p.C <= 40,
    "alta extraversion": lambda p: p.E >= 60,
    "baja extraversion": lambda p: p.E <= 40,
    "alta amabilidad": lambda p: p.A >= 60,
    "baja amabilidad": lambda p: p.A <= 40,
    "alto neuroticismo": lambda p: p.N >= 60,
    "bajo neuroticismo": lambda p: p.N <= 40
}

def match_personality(personality: Dict, tags: List[str]) -> float:
    if not tags:
        return 0.0

    matched = 0
    for tag in tags:
        tag_norm = normalize(tag)
        if tag_norm in RULES and RULES[tag_norm](personality):
            matched += 1

    return round(matched / len(tags), 4)


# -------------------------
# 🔹 GENERADOR DE EXPLICACIONES
# -------------------------

def generate_explanation(book: Dict, profile: FullProfile) -> str:
    prefs = profile.preferences
    explanation = []

    # Normalizar campos
    book_data = {
        'genres': normalize_list(book.get("genres", [])),
        'themes': normalize_list(book.get("themes", [])),
        'emotion_tags': normalize_list(book.get("emotion_tags", [])),
        'tone': normalize(book.get("tone")),
        'style': normalize(book.get("style")),
        'age_range': normalize(book.get("age_range")),
        'personality_match': book.get("personality_match", [])
    }

    user_data = {
        'genres': normalize_list(prefs.genres),
        'themes': normalize_list(prefs.themes),
        'emotion_tags': normalize_list(prefs.emotion_tags),
        'tone': normalize(prefs.tone),
        'style': normalize(prefs.style),
        'age_range': normalize(prefs.age_range)
    }

    # Comparaciones y frases
    if set(book_data['genres']) & set(user_data['genres']):
        explanation.append("géneros que te interesan")
    if set(book_data['themes']) & set(user_data['themes']):
        explanation.append("temas que has indicado como relevantes")
    if set(book_data['emotion_tags']) & set(user_data['emotion_tags']):
        explanation.append("emociones que valoras en tus lecturas")
    if book_data['tone'] and book_data['tone'] == user_data['tone']:
        explanation.append("tono narrativo que prefieres")
    if book_data['style'] and book_data['style'] == user_data['style']:
        explanation.append("estilo narrativo afín a tus gustos")
    if book_data['age_range'] and book_data['age_range'] == user_data['age_range']:
        explanation.append("rango de edad adecuado para ti")
    if match_personality(profile.personality, book_data['personality_match']) >= 0.5:
        explanation.append("afinidad psicológica con tu perfil de personalidad")

    # Generar texto final
    if explanation:
        if len(explanation) == 1:
            return f"📌 Este libro ha sido seleccionado por su coincidencia con {explanation[0]}."
        joined = ", ".join(explanation[:-1]) + " y " + explanation[-1]
        return f"📌 Este libro ha sido seleccionado por su coincidencia con {joined}."
    else:
        return "📌 Este libro fue sugerido por afinidad general con tu perfil lector, aunque no hubo coincidencias exactas destacadas."


# -------------------------
# 🔹 INTERFAZ PÚBLICA
# -------------------------

def score_book(book: Dict, profile: FullProfile) -> float:
    return compute_score(profile, book)
