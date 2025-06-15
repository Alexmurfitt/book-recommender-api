# ✅ streamlit_app/app.py
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import requests
from utils.field_loader import load_field_options

# Cargar opciones desde JSON preprocesado
options = load_field_options()

# Configuración de la página
st.set_page_config(page_title="Recomendador de Libros", layout="centered")

# Título
st.title("📚 Recomendador Personalizado de Libros")
st.subheader("Contesta el siguiente cuestionario para obtener una recomendación literaria única.")

# ---------------------------
# 1. Cuestionario literario
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
# 2. Test Big Five (OCEAN)
# ---------------------------
st.header("🧠 Test de Personalidad Big Five")

likert = {
    "Muy en desacuerdo": 1,
    "En desacuerdo": 2,
    "Neutral": 3,
    "De acuerdo": 4,
    "Muy de acuerdo": 5
}

st.markdown("Responde del 1 (Muy en desacuerdo) al 5 (Muy de acuerdo):")

O = likert[st.radio("Me gusta experimentar cosas nuevas y tengo mucha imaginación.", list(likert.keys()), key="O1")]
O += likert[st.radio("Disfruto aprendiendo sobre temas filosóficos o abstractos.", list(likert.keys()), key="O2")]

C = likert[st.radio("Soy organizado y me gusta planificar con antelación.", list(likert.keys()), key="C1")]
C += likert[st.radio("Cumplo mis responsabilidades con disciplina.", list(likert.keys()), key="C2")]

E = likert[st.radio("Disfruto interactuando con la gente y soy sociable.", list(likert.keys()), key="E1")]
E += likert[st.radio("Me siento lleno de energía cuando estoy rodeado de personas.", list(likert.keys()), key="E2")]

A = likert[st.radio("Me preocupo por los demás y trato de ayudar.", list(likert.keys()), key="A1")]
A += likert[st.radio("Confío en los demás y soy cooperativo.", list(likert.keys()), key="A2")]

N = likert[st.radio("Me estreso con facilidad.", list(likert.keys()), key="N1")]
N += likert[st.radio("A menudo me siento ansioso o inseguro.", list(likert.keys()), key="N2")]

def scale(val):
    return int((val / 10) * 100)

personality = {
    "O": scale(O),
    "C": scale(C),
    "E": scale(E),
    "A": scale(A),
    "N": scale(N)
}

# ---------------------------
# 3. Envío a la API
# ---------------------------
if st.button("🔍 Obtener recomendación"):
    if not genre or not themes or not emotion_tags:
        st.warning("⚠️ Por favor, completa al menos género, tema y emociones.")
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

        with st.expander("📦 Datos enviados a la API"):
            st.json(payload)

        try:
            response = requests.post("http://127.0.0.1:8001/api/recommendation", json=payload)
            if response.status_code == 200:
                data = response.json()["recommendation"]
                explanation = response.json()["explanation"]

                st.success("✅ ¡Libro recomendado!")
                st.markdown(f"""
                ### 📖 {data['title']}
                **Autor:** {data['author']}
                **Edad recomendada:** {data['age_range']}
                **Tono:** {data['tone']}  
                **Estilo:** {data['style']}  
                **Temas:** {', '.join(data['themes'])}  
                **Emociones evocadas:** {', '.join(data['emotion_tags'])}  

                📝 *{data['description']}*

                💡 **Motivo de la recomendación:**  
                {explanation}
                """)
            else:
                st.error(f"⚠️ {response.json().get('detail', 'Error en la respuesta de la API.')}")

        except Exception as e:
            st.error("🚫 Error al conectar con la API.")
            st.text(str(e))
