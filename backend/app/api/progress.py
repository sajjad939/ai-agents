# ========== app/api/progress.py ==========
from fastapi import APIRouter

router = APIRouter(prefix="/progress", tags=["Progress"])

@router.get("/")
def get_progress():
    return []