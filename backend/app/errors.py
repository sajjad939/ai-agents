# app/errors.py
from fastapi import Request, HTTPException

def register_error_handlers(app):
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        return HTTPException(status_code=500, detail="Internal server error. Please try again later.")