"""
FixFit Backend - FastAPI Application Entry Point
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router

app = FastAPI(
    title="FixFit API",
    description="AI-powered squat form analyzer",
    version="1.0.0",
)

# CORS Configuration
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api/v1")


@app.get("/health")
async def health_check() -> dict:
    """Health check endpoint for container orchestration."""
    return {"status": "ok", "service": "fixfit-backend"}

