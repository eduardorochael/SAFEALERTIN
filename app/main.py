from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routes.auth import router as auth_router
from app.routes.emergencia import router as emergencia_router
from app.routes.usuario import router as usuario_router

app = FastAPI(title="SafeAlert API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(usuario_router)
app.include_router(emergencia_router)
app.include_router(auth_router)


@app.get("/")
def home():
    return {"msg": "SafeAlert rodando", "docs": "/docs"}
