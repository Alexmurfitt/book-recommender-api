# 📚 Informe del Proyecto: API de Recomendación de Libros Personalizada

## 🌟 Descripción General

Este proyecto implementa una API avanzada para recomendar libros de forma hiperpersonalizada. La recomendación se basa en dos pilares:

1. **Preferencias literarias**: géneros, temas, emociones, tono, estilo, idioma, edad preferida.
2. **Perfil de personalidad**: test psicológico Big Five (modelo OCEAN).

La API está construida con **FastAPI** como framework backend, **MongoDB** como base de datos documental y **Streamlit** como interfaz visual (opcional).

La lógica del sistema puntúa los libros mediante una heurística de afinidad entre las preferencias del usuario y los metadatos enriquecidos de cada libro. La API devuelve el libro con mejor puntuación y una explicación textual.

---

## 🪡 Estructura del Proyecto

```
book_recommender_api/
├── app/                    # Lógica de negocio y controladores FastAPI
│   ├── main.py             # Punto de entrada de la API
│   ├── models.py           # Esquemas Pydantic
│   ├── books_controller.py # Endpoints de recomendación
│   ├── recommender.py      # Algoritmo de puntuación y explicación
│   ├── database.py         # Conexión con MongoDB
│   ├── user_controller.py  # Endpoint para guardar perfiles
│   ├── quiz.py             # Cuestionario de preferencias
│   ├── personality.py      # Test OCEAN (Big Five)
│   ├── profile.py          # Ensamblado de FullProfile
│   ├── explain.py          # Explicación semántica generada
│   └── __init__.py
├── data/                  # Archivos con libros procesados
│   ├── books_all_335.json
│   ├── books_openlibrary_raw.json
│   └── books_openlibrary_enriched.json
├── tests/                 # Pruebas PyTest
│   └── test_recommender.py
├── utils/                 # Scripts de enriquecimiento de datos
│   ├── fetch_openlibrary_books.py
│   ├── enrich_books.py
│   ├── validate_books.py
│   └── import_books.py
├── streamlit_app/         # UI opcional en Streamlit
│   └── app.py
├── requirements.txt
├── pytest.ini
└── README.md
```

---

## 🧬 Lógica de Recomendación (app/recommender.py)

### ✅ `compute_score(profile, book)`

Calcula una puntuación heurística basada en las coincidencias entre el perfil y los campos del libro. Criterios:

* Géneros
* Temas
* Emociones
* Tono
* Estilo
* Edad
* Personalidad (OCEAN)

### 🔢 Ponderación recomendada:

```python
{
  'themes': 0.30,
  'emotion_tags': 0.25,
  'genres': 0.20,
  'tone_style': 0.15,
  'personality_match': 0.10,
  'age_range': 0.00
}
```

### 📊 `generate_explanation()`

Genera una explicación textual personalizada según los factores que coincidieron. Asegura consistencia y evita paréntesis vacíos.

### 🨓 `match_personality()`

Compara los valores OCEAN del usuario con los tags deseados del libro.

---

## 🧲 Flujo de Recomendación

1. El usuario completa el cuestionario literario (`quiz.py`) y el test Big Five (`personality.py`).
2. Se construye el perfil completo (`FullProfile`) en `profile.py`.
3. Se envía al endpoint `/recommendation`.
4. Se puntúan todos los libros con `compute_score()`.
5. Se devuelve el libro con mayor puntuación junto con la explicación.

---

## 👉 Endpoints Clave

| Método | Ruta                  | Descripción                                    |
| ------ | --------------------- | ---------------------------------------------- |
| GET    | `/api/books`          | Devuelve la lista de libros disponibles        |
| POST   | `/api/recommendation` | Devuelve el mejor libro para el perfil enviado |
| POST   | `/api/users/save`     | Guarda el perfil de usuario en MongoDB         |

---

## 🔮 Testing con PyTest

Archivo `tests/test_recommender.py`:

* Prueba el cálculo de puntuaciones
* Verifica la coherencia de las explicaciones
* Asegura el correcto funcionamiento de los endpoints

---

## 🎨 Frontend en Streamlit (streamlit\_app/app.py)

* UI para cuestionario y test OCEAN
* Muestra el libro recomendado y explicación
* (En desarrollo): guardado automático en MongoDB

---

## ⚡ Problemas Detectados y Mejoras

| Problema                       | Solución Propuesta                |
| ------------------------------ | --------------------------------- |
| Peso excesivo de género        | Reajustar ponderación             |
| Campos vacíos en explicaciones | Validar antes de mostrar          |
| Idioma incorrecto en libros    | Filtrar por `language = 'es'`     |
| Fallos por tildes o mayúsculas | Normalizar textos con unicodedata |

---

## 🔢 Evaluación de Variables de Recomendación

### 📈 Alta relevancia:

* `themes`: Clave para afinidad intelectual
* `emotion_tags`: Impacto emocional directo
* `genres`: Clasificación base de la lectura
* `tone`: Clima narrativo

### 🧠 Media relevancia:

* `style`: Modula experiencia literaria
* `personality_match`: Personalización psicológica

### 🔽 Baja relevancia:

* `age_range`: Sólo como filtro de entrada
* `language`: Crítico para filtrado, no para puntuación
* `year`: Irrelevante para afinidad semántica

---

## 📄 Ejemplo de Perfil Enviado a /recommendation

```json
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
```

---

## 🪮 Versión Ligera del Sistema

En entornos con pocos recursos, puede implementarse una versión simplificada basada sólo en:

* `themes`
* `emotion_tags`
* `genres`
* (opcionalmente) `tone`

Esto reduce complejidad sin sacrificar calidad. Se pueden desactivar `style`, `age_range` y `personality_match`.

---

## 📅 Conclusión

Este sistema representa una arquitectura modular, precisa y flexible para recomendar libros. Sus puntos fuertes:

* Combina psicología y semántica para recomendaciones personalizadas
* Tiene una arquitectura clara y expandible
* Ofrece explicaciones razonadas

📅 Recomendaciones futuras:

* Ajustar pesos y normalizar datos
* Mejorar explicaciones con LLMs (opcional)
* Incorporar clustering de usuarios y ranking de libros
* Automatizar el guardado e interfaz con Streamlit

El sistema está listo para producir recomendaciones de alta calidad y puede escalar hacia nuevas funcionalidades como recomendaciones colaborativas o sociales.
