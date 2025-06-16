# 📚 API de Recomendación de Libros Personalizada

**Tecnologías:** FastAPI · MongoDB · PyMongo · Pydantic · Python · Postman

## 🎯 ¿En qué consiste esta API?

Se trata de una API backend desarrollada con FastAPI y MongoDB cuyo objetivo es recomendar libros con precisión y objetividad a cada usuario, combinando:

1. **📝 Cuestionario literario inteligente**, donde el usuario indica sus géneros favoritos, temas, emociones deseadas, tono y estilo narrativo, y edad lectora.
2. **🧠 Test psicológico basado en el modelo Big Five (OCEAN)**, que genera un perfil psicométrico con puntuaciones en apertura, responsabilidad, extraversión, amabilidad y neuroticismo.
3. **⚙️ Algoritmo heurístico de recomendación**, que compara el perfil completo del usuario con una base de datos enriquecida de 335 libros (67 subgéneros, 11 géneros), para encontrar los libros más afines, acompañados de una explicación textual del porqué.

---

## 🧱 Estructura del proyecto

```
book_recommender_api/
├── app/
│   ├── main.py              ← Punto de entrada FastAPI
│   ├── database.py          ← Conexión MongoDB con PyMongo
│   ├── models.py            ← Esquemas Pydantic (UserProfile, Book, Personality, etc.)
│   ├── quiz.py              ← Endpoint para preferencias literarias
│   ├── personality.py       ← Endpoint para test OCEAN
│   ├── profile.py           ← Combinación de quiz + personalidad
│   ├── recommender.py       ← Lógica de matching y puntuación
│   ├── explain.py           ← Generación de explicación semántica
│   ├── books_controller.py  ← Gestión de libros (GET/POST)
├── data/
│   └── books_all_335.json   ← Dataset enriquecido de libros
├── utils/
│   ├── import_books.py      ← Importación del dataset
│   └── create_project_structure.py
├── requirements.txt         ← Dependencias del proyecto
└── .env                     ← Variables de entorno (MONGO_URI)
```

---

## 🧠 Lógica de recomendación

El algoritmo evalúa el perfil del usuario frente a cada libro con una fórmula ponderada:

```python
score = (
    0.4 * genre_match +
    0.3 * emotion_match +
    0.2 * personality_match +
    0.1 * style_tone_match
)
```

Se seleccionan los 5 libros con mayor puntuación y se genera una explicación transparente basada en coincidencias reales (géneros, emociones, personalidad, estilo).

---

## 🧪 Endpoints implementados

| Endpoint                  | Método   | Descripción                                                     |
| ------------------------- | -------- | --------------------------------------------------------------- |
| `/quiz`                   | POST     | Guarda las respuestas del cuestionario literario                |
| `/personality-test`       | POST     | Guarda el perfil OCEAN del usuario                              |
| `/user-profile`           | POST     | Combina preferencias y personalidad en un perfil único          |
| `/recommendation`         | GET      | Devuelve los libros más compatibles con el perfil del usuario   |
| `/explain-recommendation` | GET      | Devuelve explicación detallada del porqué de cada recomendación |
| `/books`                  | GET/POST | Consultar o añadir libros a la base de datos                    |

---

## 🔧 Qué he implementado paso a paso

1. **Diseño y estructura del sistema**

   * Creación de arquitectura modular siguiendo patrón MVC.
   * Separación de la lógica por responsabilidad (quiz, personalidad, perfil, recomendación, explicación, base de datos).
   * Uso de clases Pydantic para modelado de datos validado.

2. **Gestión de usuarios y perfiles**

   * Registro por ID único (UUID) y validación de email.
   * Almacenamiento de quiz y test OCEAN por usuario.
   * Composición del perfil completo combinando ambas respuestas.

3. **Dataset enriquecido**

   * Selección manual y estructurada de 335 libros reales desde Open Library, Goodreads, etc.
   * Clasificación por género, subgénero, temas, emociones, estilo, tono, idioma, edad lectora y personalidad compatible.
   * Importación a MongoDB y validación de formato con `jq`.

4. **Desarrollo del sistema de recomendación**

   * Implementación del motor de puntuación heurística (`compute_score`).
   * Filtro por idioma, edad y afinidad semántica.
   * Generación automática de explicaciones (`generate_explanation`) con campos coincidentes.

5. **Testing y resolución de errores**

   * Pruebas exhaustivas con Postman.
   * Validación de integridad de la base de datos en MongoDB Compass.
   * Corrección de múltiples errores: rutas incorrectas, conflictos de dependencias, incompatibilidad con Python 3.13 (migración a 3.10), uso de `__init__.py`, normalización de imports absolutos.

---

## 🧯 Problemas técnicos superados

| Problema                                   | Solución aplicada                                         |
| ------------------------------------------ | --------------------------------------------------------- |
| `ModuleNotFoundError` con `utils` o `quiz` | Uso de imports absolutos y archivos `__init__.py`         |
| Conflicto con `pydantic 2.x`               | Migración estable a `pydantic 1.10.13`                    |
| Error con `uvicorn` al lanzar la app       | Cambio a ejecución desde raíz con ruta explícita correcta |
| MongoDB no conectado                       | Añadido endpoint `/ping` para comprobación                |

---

## ✅ Conocimientos y habilidades adquiridas

✔️ Diseño de APIs RESTful con FastAPI
✔️ Modelado y validación de datos con Pydantic
✔️ Conexión y manipulación de datos en MongoDB con PyMongo
✔️ Diseño de sistemas de recomendación heurísticos
✔️ Testing con Postman
✔️ Depuración de errores y despliegue en entorno local
✔️ Organización modular y buenas prácticas de ingeniería backend

---

## 🌟 Conclusión final

Este proyecto representa una solución profesional, robusta y escalable para la recomendación de contenido cultural personalizado. He trabajado desde cero en la arquitectura, diseño, implementación, depuración y validación de todos los módulos necesarios para que el sistema funcione con precisión y eficiencia. Es un ejemplo claro de cómo integrar procesamiento semántico, evaluación psicométrica y estructuración de datos para ofrecer recomendaciones realmente inteligentes.

Este sistema puede escalarse fácilmente con un frontend en Streamlit o React, autenticación JWT, clustering de usuarios, sinopsis generadas por IA, y recomendaciones multilingües.


