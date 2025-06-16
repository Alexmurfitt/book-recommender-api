✅ README.md FINAL

# 📚 Book Recommender API

Sistema backend avanzado construido con **FastAPI** y **MongoDB**, que ofrece recomendaciones de libros hiperpersonalizadas a partir de:

- 🎯 Un cuestionario literario (géneros, emociones, tono, estilo...)
- 🧠 Un test psicológico Big Five (OCEAN)
- 🔍 Un sistema heurístico de puntuación por afinidad
- 📘 Una base de datos validada con 335 libros clasificados en 67 subgéneros

---

## 🚀 Tecnologías

- FastAPI
- PyMongo + MongoDB
- Pydantic
- dotenv
- Uvicorn

---

## 📁 Estructura del Proyecto

book_recommender_api/
├── app/
│ ├── main.py # Inicializa la API y registra routers
│ ├── database.py # Conexión MongoDB
│ ├── models.py # Esquemas Pydantic: perfil, libros, respuesta
│ ├── recommender.py # Algoritmo de puntuación y explicación
│ ├── books_controller.py # Rutas principales
│ ├── quiz.py # Preferencias literarias
│ ├── personality.py # Test OCEAN
│ ├── profile.py # Perfil completo
│ ├── explain.py # Explicaciones textuales
│ ├── user_controller.py # Guardado de usuarios
│ └── init.py
├── data/
│ └── books_all_335.json # Base validada de libros
├── utils/
│ ├── import_books.py # Inserta libros en MongoDB
│ ├── validate_books.py # Verifica integridad estructural
│ └── merge_books.py # Combina versiones del dataset
├── tests/
│ └── test_recommender.py # Pruebas PyTest del sistema de puntuación
├── .env # URI MongoDB
├── requirements.txt # Dependencias
├── pytest.ini # Configuración de PyTest
└── README.md


---

## 📡 Endpoints principales

| Método | Ruta                         | Función                                                   |
|--------|------------------------------|------------------------------------------------------------|
| POST   | `/quiz`                      | Enviar preferencias literarias                             |
| POST   | `/personality-test`          | Enviar resultados del test OCEAN                           |
| POST   | `/profile`                   | Guardar perfil completo del usuario                        |
| GET    | `/recommendation`            | Obtener libro recomendado según el perfil                  |
| GET    | `/explain-recommendation`    | Justificación textual de la recomendación                  |
| GET    | `/books`                     | Listar libros disponibles (título y autor)                 |
| POST   | `/users/save`                | Guardar perfil del usuario completo en MongoDB             |

---

## ⚙️ Uso del Proyecto

### 1. Clonar el repositorio

git clone https://github.com/tu_usuario/book-recommender-api.git
cd book-recommender-api
2. Crear entorno virtual
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
3. Instalar dependencias

pip install -r requirements.txt
4. Crear .env
ini

MONGO_URI=mongodb://localhost:27017
5. Importar libros

python utils/import_books.py
6. Ejecutar servidor

uvicorn app.main:app --reload
📄 Accede a la documentación en Swagger:
http://127.0.0.1:8000/docs

🧠 Ejemplo de perfil enviado

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
✅ Estado actual
 API funcional y modular

 Sistema de recomendación heurística completo

 Dataset validado y enriquecido

 Justificación textual personalizada

 Tests automáticos básicos


