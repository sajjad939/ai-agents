/*
========================
Backend Project Structure (Sajjad & Noor)
========================

ai-drawing-coach-backend/
│
├── app/
│   ├── __init__.py
│   ├── main.py                # FastAPI app entrypoint
│   ├── config.py              # Settings/env vars
│   ├── db.py                  # Supabase/Postgres client
│   ├── models.py              # Pydantic schemas
│   ├── auth.py                # Auth logic (Supabase/JWT)
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── coach.py           # CoachAgent
│   │   ├── critique.py        # CritiqueAgent
│   │   ├── renderer.py        # RendererAgent
│   ├── api/
│   │   ├── __init__.py
│   │   ├── lessons.py         # Lesson & lesson type endpoints
│   │   ├── transcript.py      # Transcript logging/export
│   │   ├── ai.py              # Orchestration endpoint
│   │   ├── progress.py        # Progress & achievements
│   │   ├── collab.py          # WebSocket endpoints
│   │   ├── health.py          # Healthcheck
│   │   ├── test.py            # Test endpoint
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── caching.py         # Caching/retry logic
│   │   ├── export.py          # PDF/Word export helpers
│   └── errors.py              # Global error handlers
│
├── tests/
│   ├── test_api.py
│   └── ...
├── requirements.txt
├── README.md
└── .env

========================
Sample File Contents
========================
*/

/* app/main.py */
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

/* app/models.py */
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict
import datetime

class User(BaseModel):
    id: str
    email: EmailStr
    created_at: datetime.datetime

class Profile(BaseModel):
    user_id: str
    display_name: str
    avatar_url: Optional[str] = None

class LessonType(BaseModel):
    id: str
    name: str
    description: Optional[str] = None

class Lesson(BaseModel):
    id: str
    user_id: str
    lesson_type: str
    created_at: datetime.datetime

class TranscriptStep(BaseModel):
    id: str
    lesson_id: str
    step: int
    user_input: Optional[str]
    critique: Optional[str]
    render: Optional[dict]
    agent_reasoning: Optional[str]
    created_at: datetime.datetime

class Progress(BaseModel):
    user_id: str
    lesson_id: str
    progress: float
    completed: bool

class Achievement(BaseModel):
    user_id: str
    badge: str
    unlocked_at: datetime.datetime

/* app/db.py */
# Placeholder for Supabase/Postgres client
class SupabaseClient:
    def __init__(self):
        self.db = {
            "users": [],
            "profiles": [],
            "lessons": [],
            "lesson_types": [],
            "transcript_steps": [],
            "progress": [],
            "achievements": []
        }
    def insert(self, table, data):
        self.db[table].append(data)
        return data
    def select(self, table, filters=None):
        if not filters:
            return self.db[table]
        return [row for row in self.db[table] if all(row.get(k) == v for k, v in filters.items())]
    def update(self, table, filters, data):
        for row in self.db[table]:
            if all(row.get(k) == v for k, v in filters.items()):
                row.update(data)
        return True

supabase = SupabaseClient()

/* app/agents/coach.py */
class CoachAgent:
    def generate_instruction(self, lesson_type: str, step: int) -> str:
        # In production, call GPT-5 or similar
        return f"Step {step}: Draw the base ellipse for your {lesson_type}."

/* app/agents/critique.py */
class CritiqueAgent:
    def critique(self, user_input: str) -> str:
        # In production, call GPT-5 or similar
        return "Good attempt! Try to make your lines smoother."

/* app/agents/renderer.py */
class RendererAgent:
    def render(self, instruction: str) -> dict:
        # In production, translate instruction to canvas ops
        return {"op": "draw_ellipse", "params": {"cx": 100, "cy": 100, "rx": 50, "ry": 20}}

/* app/api/lessons.py */
from fastapi import APIRouter
from app.models import LessonType

router = APIRouter(prefix="/api/lessons", tags=["Lessons"])

@router.get("/types", response_model=List[LessonType])
def get_lesson_types():
    return [
        LessonType(id="cylinder", name="Cylinder", description="Learn to draw a 3D cylinder."),
        LessonType(id="ellipse", name="Ellipse", description="Master ellipses for perspective."),
        LessonType(id="cube", name="Cube", description="Draw cubes in space.")
    ]

/* app/api/transcript.py */
from fastapi import APIRouter, Depends
from app.models import TranscriptStep
from app.db import supabase

router = APIRouter(prefix="/api/transcript", tags=["Transcript"])

@router.post("/log")
def log_transcript_step(step: TranscriptStep):
    supabase.insert("transcript_steps", step.dict())
    return {"status": "logged"}

/* app/api/ai.py */
from fastapi import APIRouter, Depends
from app.models import OrchestrationRequest
from app.agents.coach import CoachAgent
from app.agents.critique import CritiqueAgent
from app.agents.renderer import RendererAgent

router = APIRouter(prefix="/api/ai", tags=["AI"])

coach_agent = CoachAgent()
critique_agent = CritiqueAgent()
renderer_agent = RendererAgent()

@router.post("/orchestrate")
def orchestrate(req: OrchestrationRequest):
    instruction = coach_agent.generate_instruction(req.lesson_type, req.step)
    render_ops = renderer_agent.render(instruction)
    critique = critique_agent.critique(req.user_input) if req.user_input else None
    return {
        "instruction": instruction,
        "render": render_ops,
        "critique": critique
    }

/* app/api/collab.py */
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, List

router = APIRouter(tags=["Collab"])

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, session_id: str, websocket: WebSocket):
        await websocket.accept()
        if session_id not in self.active_connections:
            self.active_connections[session_id] = []
        self.active_connections[session_id].append(websocket)

    def disconnect(self, session_id: str, websocket: WebSocket):
        self.active_connections[session_id].remove(websocket)
        if not self.active_connections[session_id]:
            del self.active_connections[session_id]

    async def broadcast(self, session_id: str, message: dict):
        for connection in self.active_connections.get(session_id, []):
            await connection.send_json(message)

manager = ConnectionManager()

@router.websocket("/ws/session/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await manager.connect(session_id, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            await manager.broadcast(session_id, data)
    except WebSocketDisconnect:
        manager.disconnect(session_id, websocket)

/* app/api/health.py */
from fastapi import APIRouter

router = APIRouter(tags=["System"])

@router.get("/health")
def healthcheck():
    return {"status": "ok"}

/* app/errors.py */
from fastapi import Request, HTTPException

def register_error_handlers(app):
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        return HTTPException(status_code=500, detail="Internal server error. Please try again later.")

# ... (Other files: progress.py, export.py, test.py, etc. follow similar modular structure)

"""
========================
How to Run
========================
- Place all files in the structure above.
- Install requirements: fastapi, uvicorn, pydantic, etc.
- Run: uvicorn app.main:app --reload
- All endpoints are available under /api/...
- WebSocket: ws://localhost:8000/ws/session/{session_id}
- Extend/replace mock logic with real Supabase, GPT-5, and export integrations for production.
"""

