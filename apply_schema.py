"""Aplica el esquema Oracle completo (fuente única: app/database/esquema.sql).

Regenera la vista, el trigger de auditoría, los procedimientos y la función.
Las credenciales se leen de variables de entorno (.env).
"""
import os
import re

import oracledb


def prepare_statement(stmt: str) -> str:
    """Quita el ';' final de DDL simples, pero lo conserva en bloques PL/SQL (END;)."""
    if not stmt.endswith(";"):
        return stmt
    if re.search(r"\bEND\s*;\s*$", stmt, flags=re.IGNORECASE):
        return stmt
    return stmt[:-1]


def main() -> None:
    user = os.getenv("DB_USER", "system")
    password = os.getenv("ORACLE_PWD")
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "1522")
    service = os.getenv("DB_SERVICE_NAME", "XEPDB1")

    if not password:
        raise SystemExit("ORACLE_PWD no está definido. Configúralo en el archivo .env")

    dsn = f"{host}:{port}/{service}"

    conn = oracledb.connect(user=user, password=password, dsn=dsn)
    cursor = conn.cursor()

    script_path = os.path.join("app", "database", "esquema.sql")
    with open(script_path, encoding="utf-8") as f:
        sql_script = f.read()

    statements = re.split(r"^\s*/\s*$", sql_script, flags=re.MULTILINE)

    for raw in statements:
        stmt = raw.strip()
        if not stmt:
            continue
        print("Ejecutando bloque...")
        try:
            cursor.execute(prepare_statement(stmt))
            print("Éxito.")
        except Exception as e:
            print(f"Error: {e}")

    conn.commit()
    cursor.close()
    conn.close()
    print("Terminado.")


if __name__ == "__main__":
    main()
