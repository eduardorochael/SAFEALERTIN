from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.emergencia import Emergencia
from app.models.usuario import Usuario
from app.schemas.emergencia import EmergenciaCreate, EmergenciaResponse

router = APIRouter()


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
    return nova


@router.get("/emergencias", response_model=list[EmergenciaResponse])
def listar_emergencias(db: Session = Depends(get_db)):
    return db.query(Emergencia).order_by(Emergencia.data.desc()).all()
