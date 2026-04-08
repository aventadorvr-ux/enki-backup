from fastapi import FastAPI
from app.api_routes import router

app = FastAPI(title="NZ Real Estate AI API")

@app.get("/")
async def root():
    return {"message": "NZ Real Estate AI API"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

app.include_router(router, prefix="/api/v1")
