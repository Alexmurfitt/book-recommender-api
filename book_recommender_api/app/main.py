# ✅ main.py — Punto de entrada de la API

from fastapi import FastAPI
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# ✅ Routers de cada módulo
from book_recommender_api.app.quiz import router as quiz_router
from book_recommender_api.app.personality import router as personality_router
from book_recommender_api.app.explain import router as explain_router
from book_recommender_api.app.profile import router as profile_router
from book_recommender_api.app.books_controller import router as books_router
from book_recommender_api.app.user_controller import router as user_router

# ✅ Cargar variables de entorno
load_dotenv()

# ✅ Crear aplicación FastAPI
app = FastAPI(
    title="Book Recommender API",
    version="0.1.0",
    description="API para recomendar libros personalizados en base a perfil psicológico y gustos literarios."
)

# ✅ Conexión MongoDB para comprobación de estado
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)

# ✅ Registrar routers
app.include_router(quiz_router, prefix="/quiz", tags=["Quiz"])
app.include_router(personality_router, prefix="/personality", tags=["Personality Test"])
app.include_router(explain_router, prefix="/explain", tags=["Explain Recommendation"])
app.include_router(profile_router, prefix="/profile", tags=["User Profile"])
app.include_router(books_router, prefix="/api", tags=["Book Recommendation"])
app.include_router(user_router, prefix="/api/users", tags=["User Preferences"])

# ✅ Endpoint raíz
@app.get("/")
def root():
    return {"message": "API de Recomendación de Libros activa"}

# ✅ Endpoint de comprobación de salud
@app.get("/health")
def health_check():
    try:
        client.admin.command("ping")
        return {"status": "ok", "mongodb": "conectado"}
    except Exception as e:
        return {
            "status": "error",
            "mongodb": "no conectado",
            "error": str(e)
        }
