from pydantic import BaseModel


class EmergenciaCreate(BaseModel):
    usuario_id: int
    latitude: float
    longitude: float


class EmergenciaUsuarioResponse(BaseModel):
    id: int
    nome: str
    cpf: str | None = None
    telefone: str | None = None

    class Config:
        from_attributes = True


class EmergenciaResponse(BaseModel):
    id: int
    usuario_id: int
    latitude: float
    longitude: float
    status: str
    usuario: EmergenciaUsuarioResponse

    class Config:
        from_attributes = True
