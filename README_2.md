# 📚 Book Recommender API

Sistema backend avanzado construido con **FastAPI** y **MongoDB**, que ofrece recomendaciones de libros hiperpersonalizadas a partir de:

* 🌟 Un cuestionario literario (géneros, emociones, tono, estilo...)
* 🧠 Un test psicológico Big Five (OCEAN)
* 🔍 Un sistema heurístico de puntuación por afinidad
* 📘 Una base de datos validada con 335 libros clasificados en 67 subgéneros

---

## ✨ Características destacadas

* Recomendaciones hiperpersonalizadas según personalidad y gustos literarios.
* Algoritmo de puntuación ajustable y explicable (matching heurístico).
* Justificación textual generada dinámicamente.
* Base de datos JSON validada y fácilmente ampliable.
* Arquitectura modular extensible con FastAPI.
* Compatible con MongoDB Compass y despliegue local o remoto.

---

## 🚀 Tecnologías utilizadas

* **FastAPI**: Framework moderno para APIs asíncronas en Python.
* **MongoDB + PyMongo**: Base de datos NoSQL flexible para almacenar perfiles y libros.
* **Pydantic**: Validación automática de datos con modelos tipados.
* **dotenv**: Manejo de variables de entorno sensibles (como la URI).
* **Uvicorn**: Servidor ASGI para ejecución en desarrollo.
* **PyTest**: Testing automatizado del sistema de puntuación.

---

## 📁 Estructura del Proyecto

```
book_recommender_api/
├── app/
│   ├── main.py               # Inicializa la API y registra routers
│   ├── database.py           # Conexión MongoDB
│   ├── models.py             # Esquemas Pydantic: perfil, libros, respuesta
│   ├── recommender.py        # Algoritmo de puntuación y explicación
│   ├── books_controller.py   # Rutas principales
│   ├── quiz.py               # Preferencias literarias
│   ├── personality.py        # Test OCEAN
│   ├── profile.py            # Perfil completo
│   ├── explain.py            # Explicaciones textuales
│   ├── user_controller.py    # Guardado de usuarios
│   └── __init__.py
├── data/
│   └── books_all_335.json    # Base validada de libros
├── utils/
│   ├── import_books.py       # Inserta libros en MongoDB
│   ├── validate_books.py     # Verifica integridad estructural
│   ├── merge_books.py        # Combina versiones del dataset
│   ├── extract_fields.py     # Extrae campos dinámicos
│   └── field_options.json    # Opciones para el frontend
├── tests/
│   └── test_recommender.py   # Pruebas PyTest del sistema de puntuación
├── .env                      # URI MongoDB
├── requirements.txt          # Dependencias
├── pytest.ini                # Configuración de PyTest
└── README.md
```

---

## 📀 Endpoints principales

| Método | Ruta                      | Descripción                                    |
| ------ | ------------------------- | ---------------------------------------------- |
| POST   | `/quiz`                   | Enviar preferencias literarias                 |
| POST   | `/personality-test`       | Enviar resultados del test OCEAN               |
| POST   | `/profile`                | Guardar perfil completo del usuario            |
| GET    | `/recommendation`         | Obtener libro recomendado según el perfil      |
| GET    | `/explain-recommendation` | Justificación textual de la recomendación      |
| GET    | `/books`                  | Listar libros disponibles (título y autor)     |
| POST   | `/users/save`             | Guardar perfil del usuario completo en MongoDB |

---

## ⚙️ Uso del Proyecto

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu_usuario/book-recommender-api.git
cd book-recommender-api
```

### 2. Crear entorno virtual

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Crear archivo .env

```
MONGO_URI=mongodb://localhost:27017
```

### 5. Importar libros a la base de datos

```bash
python utils/import_books.py
```

### 6. Ejecutar el servidor

```bash
uvicorn app.main:app --reload
```

### 7. Acceder a la documentación Swagger

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🧐 Ejemplo de perfil enviado (JSON)

```json
{
  "preferences": {
    "genres": ["Fantasía", "Romance"],
    "themes": ["amistad", "superación"],
    "tone": "reflexivo",
    "style": "literario",
    "emotion_tags": ["esperanza", "tristeza"],
    "age_range": "14-18",
    "language": "es"
  },
  "personality": {
    "O": 82,
    "C": 65,
    "E": 47,
    "A": 74,
    "N": 32
  }
}
```

---

## 🔄 Mejoras futuras (roadmap)

* ✅ Ampliación a 670 libros con metadatos enriquecidos.
* 🧠 Integración con IA generativa para explicar y resumir libros.
* 🧬 Algoritmo híbrido con embeddings semánticos (spaCy, Sentence Transformers).
* 🌐 Multilingüismo: perfiles y libros en varios idiomas.
* 🔐 Autenticación con JWT y gestión de usuarios.
* 📊 Dashboard de métricas y feedback del usuario.
* ⚖️ Ajustes dinámicos de pesos en el sistema de puntuación.
* 🧰 Interfaz de administrador para añadir/editar libros desde frontend.

---

✅ **Estado actual: funcional, validado, y listo para ampliaciones profesionales.**

