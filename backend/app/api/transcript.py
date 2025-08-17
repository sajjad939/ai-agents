# app/api/transcript.py
from fastapi import APIRouter
from app.models import TranscriptStep
from app.db import supabase

router = APIRouter(prefix="/transcript", tags=["Transcript"])

@router.get("/")
def get_transcript():
    return supabase.select("transcript_steps")