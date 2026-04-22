import os
from pathlib import Path

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import declarative_base, sessionmaker

BASE_DIR = Path(__file__).resolve().parent.parent

# 🔥 PEGA DO RENDER
DATABASE_URL = os.getenv("DATABASE_URL")

# 🔥 FALLBACK (caso rode local sem variável)
if not DATABASE_URL:
    DATABASE_URL = f"sqlite:///{BASE_DIR / 'test.db'}"

# 🔥 CORREÇÃO IMPORTANTE DO RENDER
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://")

# 🔥 ENGINE
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def run_migrations():
    inspector = inspect(engine)

    if "usuarios" not in inspector.get_table_names():
        return

    colunas_usuarios = {coluna["name"] for coluna in inspector.get_columns("usuarios")}

    with engine.begin() as connection:
        if "cpf" not in colunas_usuarios:
            connection.execute(text("ALTER TABLE usuarios ADD COLUMN cpf VARCHAR(20)"))