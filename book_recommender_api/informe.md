# 📚 Proyecto API de Recomendación de Libros Personalizada

# 🌟 Descripción General

Este proyecto implementa una API avanzada de recomendación de libros personalizada, basada en un sistema híbrido que cruza:

Las preferencias literarias del usuario (géneros, temas, tono, estilo, emociones, idioma, edad recomendada).

Su perfil psicológico (modelo Big Five – OCEAN).

Utiliza FastAPI como framework principal para la API, MongoDB como base de datos, y opcionalmente Streamlit como interfaz para interacción visual.

La API analiza y puntúa libros con base en coincidencias heurísticas entre los datos del usuario y los metadatos enriquecidos de los libros. Devuelve el libro con mejor puntuación y una explicación textual clara.

# 🧱 Estructura del Proyecto

book_recommender_api/
├── app/                      # Lógica de negocio y controladores FastAPI
│   ├── main.py               # Punto de entrada de la API
│   ├── models.py             # Esquemas Pydantic para entrada/salida
│   ├── books_controller.py   # Endpoints de libros y recomendación
│   ├── recommender.py        # Algoritmo de puntuación y explicación
│   ├── database.py           # Conexión con MongoDB
│   ├── user_controller.py    # Gestión de perfiles de usuario
│   ├── quiz.py               # Cuestionario literario (en desarrollo)
│   ├── personality.py        # Test de personalidad (Big Five)
│   ├── profile.py            # Construcción de perfil completo
│   ├── explain.py            # Generación de explicaciones semánticas
│   └── __init__.py
├── data/                     # Archivos JSON con libros procesados
│   ├── books_all_335.json
│   ├── books_openlibrary_raw.json
│   └── books_openlibrary_enriched.json
├── tests/                    # Pruebas unitarias (PyTest)
│   └── test_recommender.py
├── utils/                    # Scripts de procesamiento de datos
│   ├── fetch_openlibrary_books.py
│   ├── enrich_books.py
│   ├── validate_books.py
│   ├── merge_books.py
│   ├── import_books.py
│   └── create_project_structure.py
├── streamlit_app/            # Frontend opcional
│   └── app.py
├── pytest.ini                # Configuración de PyTest
├── requirements.txt          # Dependencias del proyecto
└── README.md                 # Descripción del proyecto

# 🧠 Lógica de Recomendación (app/recommender.py)

# 🔢 compute_score(profile, book)

Calcula una puntuación basada en coincidencias semánticas:

Géneros, temas, emoción, tono, estilo, edad, perfil OCEAN.

Usa pesos ajustables por criterio (ver propuesta más abajo).

# ✔️ Ponderación actual:

{
  'genres': 0.30,
  'themes': 0.25,
  'emotion_tags': 0.20,
  'personality_match': 0.15,
  'tone_style': 0.05,
  'age_range': 0.05
}

# 📉 Propuesta optimizada:

{
  'themes': 0.30,
  'emotion_tags': 0.25,
  'genres': 0.20,
  'tone_style': 0.15,
  'personality_match': 0.10,
  'age_range': 0.00
}

📏 generate_explanation()

Genera una explicación textual de la recomendación basada en los factores coincidentes. Debe evitar paréntesis vacíos.

# 🧠 match_personality()

Compara el perfil OCEAN del usuario con los valores esperados por cada libro (personality_match).

# 🧲 Flujo de Recomendación

El usuario completa un cuestionario literario (quiz.py) y un test de personalidad (personality.py).

Se construye su FullProfile (profile.py).

Se llama al endpoint POST /api/recommendation con el perfil completo.

Se evalúan todos los libros con compute_score().

Se selecciona el mejor y se devuelve junto con una explicación (generate_explanation).

# 📌 Endpoints Clave (books_controller.py)

Endpoint

Método

Descripción

/api/books

GET

Devuelve la lista de libros disponibles

/api/recommendation

POST

Devuelve el mejor libro según el perfil enviado

/api/users/save

POST

Guarda un perfil de usuario (user_controller.py)

# 🧪 Testing (tests/test_recommender.py)

Usa pytest para comprobar:

Cálculo correcto de puntuaciones.

Coherencia en los resultados.

Respuesta de la API ante inputs válidos/erróneos.

# 🎨 Frontend en Streamlit (streamlit_app/app.py)

Ofrece UI para el cuestionario literario y test Big Five.

Muestra el resultado con explicación textual.

En desarrollo: guardar perfil automáticamente en MongoDB.

# 🛠️ Problemas Detectados y Mejoras Prioritarias

Problema

Solución recomendada

Excesiva prioridad a género

Rebalancear pesos en compute_score()

Campos vacíos en explicaciones

Validar contenido antes de mostrar

Libros en idiomas incorrectos

Filtrar por language='es' en el controlador

Fallos por tildes o mayúsculas

Normalizar datos (str.lower().strip())

# ✅ Evaluación de Factores de Recomendación

🔝 Más relevantes

Factor

Justificación

themes

Núcleo conceptual emocional

emotion_tags

Determinan conexión emocional

genres

Clasificación inicial necesaria

tone

Afecta la atmósfera lectora

🧠 Relevancia media

Factor

Justificación

style

Modula experiencia de lectura

personality_match

Ajuste psicológico opcional

🔽 Menos relevantes

Factor

Justificación

age_range

Filtrado básico (no influye mucho en afinidad)

language

Solo útil como filtro, no para puntuar

year

Decorativo, poco relevante

# 📄 Ejemplo de Entrada a /api/recommendation

{
  "preferences": {
    "genres": ["Drama"],
    "themes": ["amistad"],
    "tone": "dinámico",
    "style": "directo",
    "emotion_tags": ["tristeza"],
    "age_range": "16+",
    "language": "es"
  },
  "personality": {
    "O": 80,
    "C": 70,
    "E": 50,
    "A": 90,
    "N": 30
  }
}

🧹 Posible Versión Simplificada del Sistema

Para entornos con recursos limitados, es viable una implementación que solo utilice:

themes, emotion_tags, genres, y opcionalmente tone

Esto reduce la complejidad sin perder calidad de recomendación

Se pueden desactivar módulos como personality_match y style sin comprometer la lógica principal

# 📌 Conclusión

Este proyecto representa un sistema modular, funcional y adaptable de recomendación de libros con una arquitectura clara y mantenible. Aún con ajustes por hacer, su diseño permite gran precisión en la afinidad lector-libro.

Para lograr la máxima calidad, se recomienda:

Ajustar los pesos y filtros.

Mejorar explicaciones.

Automatizar el guardado de perfiles.

Normalizar todos los datos de entrada.

El sistema puede ampliarse a futuro con clustering de usuarios, ranking de libros, compatibilidad social entre lectores y uso de modelos LLM para explicaciones generativas.
