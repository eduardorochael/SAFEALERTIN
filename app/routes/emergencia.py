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


# 🔥 CRIAR EMERGÊNCIA
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
        status="pendente"  # 🔥 garante status inicial
    )

    db.add(nova)
    db.commit()
    db.refresh(nova)

    return serializar_emergencia(nova, usuario)


# 🔥 LISTAR SOMENTE PENDENTES
@router.get("/emergencias", response_model=list[EmergenciaResponse])
def listar_emergencias(db: Session = Depends(get_db)):

    emergencias = db.query(Emergencia)\
        .filter(Emergencia.status != "atendida")\
        .order_by(Emergencia.data.desc())\
        .all()

    usuarios = {
        usuario.id: usuario
        for usuario in db.query(Usuario).filter(
            Usuario.id.in_([e.usuario_id for e in emergencias])
        ).all()
    }

    return [
        serializar_emergencia(e, usuarios[e.usuario_id])
        for e in emergencias
        if e.usuario_id in usuarios
    ]


# 🔥 MARCAR COMO ATENDIDA
@router.put("/emergencias/{id}/atender")
def atender_emergencia(id: int, db: Session = Depends(get_db)):

    emergencia = db.query(Emergencia).filter(Emergencia.id == id).first()

    if not emergencia:
        raise HTTPException(status_code=404, detail="Emergencia nao encontrada")

    emergencia.status = "atendida"
    db.commit()

    return {"msg": "Emergencia atendida"}