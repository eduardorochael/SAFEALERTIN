from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.database import SessionLocal
from app.models.usuario import Usuario
from app.services.auth import gerar_hash

db = SessionLocal()

try:
    novo_usuario = Usuario(
        nome="Eduardo",
        email="eduardo@email.com",
        telefone="11999999999",
        senha=gerar_hash("123456"),
        tipo="usuario",
    )

    db.add(novo_usuario)
    db.commit()
    print("Usuario inserido com sucesso.")
finally:
    db.close()