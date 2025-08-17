from fastapi import FastAPI
from app.api import lessons, transcript, ai, progress, collab, health, test
from app.errors import register_error_handlers

app = FastAPI(
    title="AI Drawing Coach Backend",
    description="FastAPI + Supabase backend for collaborative AI-powered drawing lessons.",
    version="0.1.0"
)

# Register routers
app.include_router(lessons.router)
app.include_router(transcript.router)
app.include_router(ai.router)
app.include_router(progress.router)
app.include_router(collab.router)
app.include_router(health.router)
app.include_router(test.router)

register_error_handlers(app)