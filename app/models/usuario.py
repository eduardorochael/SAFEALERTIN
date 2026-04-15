from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from app.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    telefone = Column(String(20))
    senha = Column(String(255), nullable=False)
    tipo = Column(String(20), nullable=False, default="usuario")
    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)
