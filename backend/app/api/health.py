# ========== app/api/health.py ==========
from fastapi import APIRouter

router = APIRouter(tags=["System"])

@router.get("/health")
def healthcheck():
    return {"status": "ok"}
