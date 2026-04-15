from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.database import SessionLocal
from app.models.usuario import Usuario
from app.services.auth import gerar_hash

db = SessionLocal()

try:
    existente = db.query(Usuario).filter(Usuario.email == "admin@admin.com").first()

    if existente:
        existente.nome = "Administrador"
        existente.telefone = "000"
        existente.senha = gerar_hash("123456")
        existente.tipo = "admin"
        print("Admin atualizado com sucesso.")
    else:
        admin = Usuario(
            nome="Administrador",
            email="admin@admin.com",
            telefone="000",
            senha=gerar_hash("123456"),
            tipo="admin",
        )
        db.add(admin)
        print("Admin criado com sucesso.")

    db.commit()
finally:
    db.close()
