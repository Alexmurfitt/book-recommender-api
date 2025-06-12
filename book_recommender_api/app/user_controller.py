# ✅ user_controller.py — Guarda perfiles de usuario en MongoDB

from fastapi import APIRouter, HTTPException
from datetime import datetime
from pymongo.collection import Collection
from book_recommender_api.app.models import FullProfile
from book_recommender_api.app.database import get_db

router = APIRouter()

@router.post("/api/users/save")
def save_user_profile(profile: FullProfile):
    try:
        db = get_db()
        users: Collection = db["users"]

        user_doc = {
            "preferences": profile.preferences.dict(),
            "personality": profile.personality.dict(),
            "timestamp": datetime.utcnow().isoformat()
        }

        result = users.insert_one(user_doc)
        return {"status": "success", "inserted_id": str(result.inserted_id)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
