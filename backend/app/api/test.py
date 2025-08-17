# ========== app/api/test.py ==========
from fastapi import APIRouter

router = APIRouter(tags=["Test"])

@router.get("/test")
def test_endpoint():
    return {"message": "Test successful"}