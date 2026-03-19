# FastAPI Main Application
# Location: EC2 3.25.170.226:/home/ubuntu/nz-realestate-ai/app/main.py
# Status: Running on port 8000

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.api.routes import router

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    description="Multi-agent AI system for NZ Real Estate",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix=settings.API_V1_PREFIX)

@app.get("/")
async def root():
    return {
        "message": "NZ Real Estate AI API",
        "version": "1.0.0",
        "agents": ["lead", "content", "scheduling", "market_intel", "transaction"]
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}
