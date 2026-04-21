import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).resolve().parent / "test.db"


def print_section(title: str) -> None:
    print(f"\n{title}")
    print("-" * len(title))


def main() -> None:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    print(f"Banco: {DB_PATH}")

    print_section("TABELAS")
    tables = cur.execute(
        "select name from sqlite_master where type='table' order by name"
    ).fetchall()
    for row in tables:
        print(row[0])

    print_section("USUARIOS")
    usuarios = cur.execute(
        """
        select id, nome, email, cpf, telefone, tipo
        from usuarios
        order by id
        """
    ).fetchall()
    if not usuarios:
        print("Nenhum usuario encontrado.")
    for row in usuarios:
        print(row)

    print_section("EMERGENCIAS")
    emergencias = cur.execute(
        """
        select id, usuario_id, latitude, longitude, status
        from emergencias
        order by id desc
        """
    ).fetchall()
    if not emergencias:
        print("Nenhuma emergencia encontrada.")
    for row in emergencias:
        print(row)

    conn.close()


if __name__ == "__main__":
    main()
