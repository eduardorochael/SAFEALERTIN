from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.database import SessionLocal
from app.models.usuario import Usuario

db = SessionLocal()

try:
    usuarios = db.query(Usuario).all()

    for usuario in usuarios:
        print(
            f"ID: {usuario.id} | Nome: {usuario.nome} | "
            f"Email: {usuario.email} | Tipo: {usuario.tipo}"
        )
finally:
    db.close()