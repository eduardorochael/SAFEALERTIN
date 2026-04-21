from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.emergencia import Emergencia
from app.models.usuario import Usuario
from app.schemas.emergencia import EmergenciaCreate, EmergenciaResponse

router = APIRouter()


def serializar_emergencia(emergencia: Emergencia, usuario: Usuario) -> dict:
    return {
        "id": emergencia.id,
        "usuario_id": emergencia.usuario_id,
        "latitude": emergencia.latitude,
        "longitude": emergencia.longitude,
        "status": emergencia.status,
        "usuario": {
            "id": usuario.id,
            "nome": usuario.nome,
            "cpf": usuario.cpf,
            "telefone": usuario.telefone,
        },
    }


@router.post("/emergencia", response_model=EmergenciaResponse, status_code=status.HTTP_201_CREATED)
def criar_emergencia(dados: EmergenciaCreate, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == dados.usuario_id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario nao encontrado.",
        )

    nova = Emergencia(
        usuario_id=dados.usuario_id,
        latitude=dados.latitude,
        longitude=dados.longitude,
    )

    db.add(nova)
    db.commit()
    db.refresh(nova)
    return serializar_emergencia(nova, usuario)


@router.get("/emergencias", response_model=list[EmergenciaResponse])
def listar_emergencias(db: Session = Depends(get_db)):
    emergencias = db.query(Emergencia).order_by(Emergencia.data.desc()).all()
    usuarios = {
        usuario.id: usuario
        for usuario in db.query(Usuario).filter(
            Usuario.id.in_([emergencia.usuario_id for emergencia in emergencias])
        ).all()
    }

    return [
        serializar_emergencia(emergencia, usuarios[emergencia.usuario_id])
        for emergencia in emergencias
        if emergencia.usuario_id in usuarios
    ]
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.emergencia import Emergencia
from app.models.usuario import Usuario
from app.schemas.emergencia import EmergenciaCreate, EmergenciaResponse

router = APIRouter()


def serializar_emergencia(emergencia: Emergencia, usuario: Usuario) -> dict:
    return {
        "id": emergencia.id,
        "usuario_id": emergencia.usuario_id,
        "latitude": emergencia.latitude,
        "longitude": emergencia.longitude,
        "status": emergencia.status,
        "usuario": {
            "id": usuario.id,
            "nome": usuario.nome,
            "cpf": usuario.cpf,
            "telefone": usuario.telefone,
        },
    }


@router.post("/emergencia", response_model=EmergenciaResponse, status_code=status.HTTP_201_CREATED)
def criar_emergencia(dados: EmergenciaCreate, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == dados.usuario_id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario nao encontrado.",
        )

    nova = Emergencia(
        usuario_id=dados.usuario_id,
        latitude=dados.latitude,
        longitude=dados.longitude,
    )

    db.add(nova)
    db.commit()
    db.refresh(nova)
    return serializar_emergencia(nova, usuario)


@router.get("/emergencias", response_model=list[EmergenciaResponse])
def listar_emergencias(db: Session = Depends(get_db)):
    emergencias = db.query(Emergencia).order_by(Emergencia.data.desc()).all()
    usuarios = {
        usuario.id: usuario
        for usuario in db.query(Usuario).filter(
            Usuario.id.in_([emergencia.usuario_id for emergencia in emergencias])
        ).all()
    }

    return [
        serializar_emergencia(emergencia, usuarios[emergencia.usuario_id])
        for emergencia in emergencias
        if emergencia.usuario_id in usuarios
    ]
