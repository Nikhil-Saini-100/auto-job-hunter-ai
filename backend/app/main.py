from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.api import api_router
from app.core.config import settings
import app.models # Register all models

app = FastAPI(
    title="Auto Job Hunter AI",
    description="API for the autonomous job hunting platform",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to Auto Job Hunter AI API"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/debug-env")
def debug_env():
    import os
    keys = list(os.environ.keys())
    masked_env = {}
    for k in keys:
        val = os.environ.get(k, "")
        if any(sec in k.upper() for sec in ["KEY", "PASS", "SECRET", "TOKEN", "URI", "URL"]):
            masked_env[k] = f"PRESENT (length: {len(val)})" if val else "EMPTY"
        else:
            masked_env[k] = val
    return masked_env

app.include_router(api_router, prefix=settings.API_V1_STR)
