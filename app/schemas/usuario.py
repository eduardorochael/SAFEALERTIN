from pydantic import BaseModel


class UsuarioCreate(BaseModel):
    nome: str
    email: str
    cpf: str
    telefone: str
    senha: str
    tipo: str = "usuario"


class LoginRequest(BaseModel):
    email: str
    senha: str
