from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.routes.auth import router as auth_router
from app.routes.usuario import router as usuario_router
from app.routes.emergencia import router as emergencia_router

BASE_DIR = Path(__file__).resolve().parent.parent
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

# 🔥 SERVE HTML
app.mount("/app", StaticFiles(directory=BASE_DIR / "app"), name="app")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(usuario_router)
app.include_router(emergencia_router)

@app.get("/")
def home():
    return {"msg": "SafeAlert rodando"}