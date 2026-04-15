from pydantic import BaseModel


class EmergenciaCreate(BaseModel):
    usuario_id: int
    latitude: float
    longitude: float


class EmergenciaResponse(BaseModel):
    id: int
    usuario_id: int
    latitude: float
    longitude: float
    status: str

    class Config:
        from_attributes = True
