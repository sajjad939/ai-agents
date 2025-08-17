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