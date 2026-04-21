from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.database import Base, engine, run_migrations
from app.routes.auth import router as auth_router
from app.routes.emergencia import router as emergencia_router
from app.routes.usuario import router as usuario_router

BASE_DIR = Path(__file__).resolve().parent.parent
FRONT_DIR = BASE_DIR / "safealert_front"

app = FastAPI(title="SafeAlert API")
app.mount("/app", StaticFiles(directory="app"), name="app")
app.include_router(auth_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
run_migrations()

app.include_router(usuario_router)
app.include_router(emergencia_router)
app.include_router(auth_router)

if FRONT_DIR.exists():
    app.mount("/front/static", StaticFiles(directory=FRONT_DIR), name="front-static")


@app.get("/")
def home():
    return {"msg": "SafeAlert rodando", "docs": "/docs"}


@app.get("/front")
def front():
    return FileResponse(FRONT_DIR / "index.html")
