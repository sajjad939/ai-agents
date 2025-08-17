from fastapi import APIRouter
from app.models import Lesson, LessonType
from app.db import supabase

router = APIRouter(prefix="/lessons", tags=["Lessons"])

@router.get("/")
def list_lessons():
    return supabase.select("lessons")