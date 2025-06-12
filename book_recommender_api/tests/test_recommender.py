# ✅ book_recommender_api/tests/test_recommender.py

import pytest
from book_recommender_api.app.models import FullProfile, Preferences, Personality
from book_recommender_api.app.recommender import compute_score, match_personality, generate_explanation, score_book

# 📘 Libro ficticio con coincidencias parciales reales
mock_book = {
    "title": "Test Book",
    "author": "Author A",
    "genres": ["Ciencia Ficción", "Distopía"],
    "subgenres": ["Utopía"],
    "themes": ["libertad", "control social"],
    "emotion_tags": ["angustia", "alerta"],
    "tone": "oscuro",
    "style": "directo",
    "age_range": "16+",
    "personality_match": ["Alta apertura", "Alta extraversión"],
    "year": 2000,
    "description": "Un libro de prueba."
}

# 🧠 Perfil ficticio con coincidencia emocional y temática
mock_profile = FullProfile(
    preferences=Preferences(
        genres=["Ciencia Ficción"],
        themes=["libertad", "futurismo"],
        tone="oscuro",
        style="directo",
        emotion_tags=["alerta", "curiosidad"],
        age_range="16+",
        language="es"
    ),
    personality=Personality(O=75, C=55, E=80, A=50, N=30)
)

# 🔻 Perfil sin coincidencias (para detectar falsos positivos)
profile_sin_match = FullProfile(
    preferences=Preferences(
        genres=["Romántica"],
        themes=["amistad"],
        tone="luminoso",
        style="poético",
        emotion_tags=["alegría"],
        age_range="infantil",
        language="es"
    ),
    personality=Personality(O=30, C=30, E=30, A=30, N=30)
)

# 🔹 Test 1: compute_score
def test_compute_score():
    score = compute_score(mock_profile, mock_book)
    assert isinstance(score, float), "La puntuación debe ser un número decimal"
    assert 0 <= score <= 1, "La puntuación debe estar entre 0 y 1"
    assert score > 0.3, "Debe reflejar coincidencia parcial significativa"

# 🔹 Test 2: match_personality
def test_match_personality():
    tags = ["Alta apertura", "Alta extraversión", "Alta amabilidad"]
    result = match_personality(mock_profile.personality, tags)
    assert 0 < result <= 1, "Debe haber coincidencias de personalidad"
    assert round(result, 2) == round(2 / 3, 2), "Coincidencias esperadas: 2 de 3"

# 🔹 Test 3: generate_explanation
def test_generate_explanation():
    explanation = generate_explanation(mock_book, mock_profile)
    assert isinstance(explanation, str)
    assert "géneros favoritos" in explanation
    assert "temas" in explanation
    assert "emociones" in explanation
    assert "tono narrativo" in explanation
    assert "estilo literario" in explanation
    assert "()" not in explanation, "No debe haber paréntesis vacíos"

# 🔹 Test 4: score_book
def test_score_book():
    score = score_book(mock_book, mock_profile)
    expected_score = compute_score(mock_profile, mock_book)
    assert abs(score - expected_score) < 1e-6, "score_book debe coincidir con compute_score"

# 🔹 Test 5: perfil sin coincidencias — score bajo
def test_score_no_match():
    score = compute_score(profile_sin_match, mock_book)
    assert score < 0.1, "Puntuación debe ser baja con perfil no relacionado"

# 🔹 Test 6: explicación vacía debe evitarse incluso con perfil sin match
def test_generate_explanation_no_match():
    explanation = generate_explanation(mock_book, profile_sin_match)
    assert isinstance(explanation, str)
    assert "()" not in explanation, "La explicación no debe tener campos vacíos aunque no haya coincidencias"
