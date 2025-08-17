# =========================
# README.md
# AI Drawing Coach Backend

A FastAPI backend for collaborative AI-powered drawing lessons.

## Setup

1. Install requirements:
   ```
   pip install -r requirements.txt
   ```
2. Run the server:
   ```
   uvicorn app.main:app --reload
   ```

## Endpoints

- All endpoints are available under `/api/...`
- WebSocket: `ws://localhost:8000/ws/session/{session_id}`