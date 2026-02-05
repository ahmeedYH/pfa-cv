from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from backend/.env
load_dotenv(Path(__file__).resolve().parent / ".env")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.main_api import router as api_router
from backend.api.cv_controller import router as cv_router

app = FastAPI(
    title="pfa-cv",
    description="Upload a CV (PDF, image, or text), extract text and analyze it with AI.",
    version="0.1.0",
)

# -------------------- CORS --------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
        "http://localhost:3002",
        "http://127.0.0.1:3002",
        "http://localhost:3003",
        "http://127.0.0.1:3003",
        "http://localhost:3004",
        "http://127.0.0.1:3004",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- Static files (optional) --------------------
static_dir = Path("static")
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=static_dir, html=True), name="static")

# -------------------- Routers --------------------
app.include_router(api_router)
app.include_router(cv_router)

# -------------------- Health & Root --------------------
@app.get("/")
def root():
    return {
        "message": "pfa-cv API is running",
        "docs": "/docs",
        "health": "/api/health",
        "port": 8001,
    }

@app.get("/api/health")
def health():
    return {"status": "ok"}
