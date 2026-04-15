from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String

from app.database import Base


class Emergencia(Base):
    __tablename__ = "emergencias"

    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, nullable=False, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    data = Column(DateTime, default=datetime.utcnow, nullable=False)
    status = Column(String(50), default="pendente", nullable=False)
