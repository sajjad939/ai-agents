# app/config.py
import os

class Settings:
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecret")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

settings = Settings()