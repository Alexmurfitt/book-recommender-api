# ✅ streamlit_app/app.py
import os
import sys
import requests
import streamlit as st

# Ajustar path para importar módulos desde nivel superior
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.field_loader import load_field_options

# ---------------------------
# 🔧 Configuración
# ---------------------------
st.set_page_config(page_title="Recomendador de Libros", layout="centered")

API_URL = st.secrets.get("API_URL", "http://127.0.0.1:8001/api/recommendation")

if "history" not in st.session_state:
    st.session_state.history = []
if "last_payload" not in st.session_state:
    st.session_state.last_payload = None

# ---------------------------
# 🏷️ Cargar opciones
# ---------------------------
options = load_field_options()
st.caption("🧹 Géneros y campos cargados desde archivo auditado (géneros verificados con taxonomía oficial).")
st.write("📚 Géneros disponibles:", options["genres"])  # ✅ Mostramos los géneros para verificar que están bien

# ---------------------------
# 🧠 Escala de personalidad
# ---------------------------
likert = {
    "Muy en desacuerdo": 1,
    "En desacuerdo": 2,
    "Neutral": 3,
    "De acuerdo": 4,
    "Muy de acuerdo": 5
}

questions = {
    "O": [
        "Me gusta experimentar cosas nuevas y tengo mucha imaginación.",
        "Disfruto aprendiendo sobre temas filosóficos o abstractos."
    ],
    "C": [
        "Soy organizado y me gusta planificar con antelación.",
        "Cumplo mis responsabilidades con disciplina."
    ],
    "E": [
        "Disfruto interactuando con la gente y soy sociable.",
        "Me siento lleno de energía cuando estoy rodeado de personas."
    ],
    "A": [
        "Me preocupo por los demás y trato de ayudar.",
        "Confío en los demás y soy cooperativo."
    ],
    "N": [
        "Me estreso con facilidad.",
        "A menudo me siento ansioso o inseguro."
    ]
}

def scale(val: int) -> int:
    return int((val / 10) * 100)

# ---------------------------
# 🧾 Título e introducción
# ---------------------------
st.title("📚 Recomendador Personalizado de Libros")
st.subheader("Contesta este cuestionario para obtener una recomendación literaria adaptada a ti.")
st.divider()

# ---------------------------
# 1️⃣ Preferencias literarias
# ---------------------------
st.header("🎯 Tus preferencias literarias")

genre = st.multiselect("¿Qué géneros te gustan?", options["genres"])
themes = st.multiselect("¿Qué temas te interesan?", options["themes"])
tone = st.selectbox("¿Qué tono prefieres?", options["tone"])
style = st.selectbox("¿Qué estilo narrativo prefieres?", options["style"])
emotion_tags = st.multiselect("¿Qué emociones te gusta que evoque un libro?", options["emotion_tags"])
age_range = st.selectbox("¿Cuál es tu rango de edad preferido para los libros?", options["age_range"])
language = st.selectbox("¿En qué idioma prefieres leer?", options.get("language", ["es", "en"]))

# ---------------------------
# 2️⃣ Test de Personalidad
# ---------------------------
st.header("🧠 Test de Personalidad Big Five")

personality = {}
for trait, q_list in questions.items():
    score = sum(likert[st.radio(q, list(likert.keys()), key=q)] for q in q_list)
    personality[trait] = scale(score)

# ---------------------------
# 3️⃣ Enviar a la API
# ---------------------------
if st.button("🔍 Obtener recomendación"):

    if not genre or not themes or not emotion_tags:
        st.warning("⚠️ Por favor, completa al menos los campos de género, tema y emociones.")
    else:
        payload = {
            "preferences": {
                "genres": genre,
                "themes": themes,
                "tone": tone,
                "style": style,
                "emotion_tags": emotion_tags,
                "age_range": age_range,
                "language": language
            },
            "personality": personality
        }

        st.session_state.last_payload = payload

        with st.expander("📦 Datos enviados a la API"):
            st.json(payload)

        with st.spinner("🔍 Buscando tu recomendación personalizada..."):
            try:
                response = requests.post(API_URL, json=payload, timeout=10)
                if response.status_code == 200:
                    result = response.json()
                    book = result["recommendation"]
                    explanation = result["explanation"]

                    st.session_state.history.append({
                        "input": payload,
                        "output": book,
                        "reason": explanation
                    })

                    st.success("✅ ¡Libro recomendado!")
                    st.markdown(f"""
                    ### 📖 {book['title']}
                    **Autor:** {book['author']}
                    **Edad recomendada:** {book['age_range']}
                    **Tono:** {book['tone']}  
                    **Estilo:** {book['style']}  
                    **Temas:** {', '.join(book['themes'])}  
                    **Emociones evocadas:** {', '.join(book['emotion_tags'])}  

                    📝 *{book['description']}*

                    💡 **Motivo de la recomendación:**  
                    {explanation}
                    """)

                else:
                    st.error(f"⚠️ La API respondió con un error: {response.json().get('detail', 'Sin detalles disponibles.')}")

            except Exception as e:
                st.error("🚫 Error al conectar con la API.")
                st.exception(e)

# ---------------------------
# 📊 Sidebar con historial
# ---------------------------
if st.session_state.history:
    with st.sidebar.expander("🕘 Historial de recomendaciones"):
        for i, entry in enumerate(reversed(st.session_state.history[-3:]), 1):
            st.markdown(f"**#{i}** – *{entry['output']['title']}*")
            st.caption(entry["reason"])
