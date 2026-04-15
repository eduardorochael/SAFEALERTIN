from pydantic import BaseModel


class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: str
    telefone: str | None = None
    tipo: str

    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    usuario_id: int
    tipo: str