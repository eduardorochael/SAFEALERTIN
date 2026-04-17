from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate
from app.schemas.usuario_response import UsuarioResponse
from app.services.auth import gerar_hash

router = APIRouter()


@router.get("/usuarios", response_model=list[UsuarioResponse])
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuario).order_by(Usuario.id.asc()).all()


@router.post("/usuarios", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    usuario_existente = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ja existe um usuario com este email.",
        )

    cpf_existente = db.query(Usuario).filter(Usuario.cpf == usuario.cpf).first()
    if cpf_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ja existe um usuario com este CPF.",
        )

    novo = Usuario(
        nome=usuario.nome,
        email=usuario.email,
        cpf=usuario.cpf,
        telefone=usuario.telefone,
        senha=gerar_hash(usuario.senha),
        tipo=usuario.tipo,
    )

    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo
