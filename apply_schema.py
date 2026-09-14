"""Aplica el esquema Oracle completo (fuente única: app/database/esquema.sql).

Regenera la vista, el trigger de auditoría, los procedimientos y la función.
La conexión se construye desde la fuente única build_dsn()
(app/database/connection.py), que lee las variables de entorno (.env).

Si falla la aplicación de cualquier objeto, se registra el error, se hace
rollback y el script termina con código de salida distinto de cero.
"""

import os
import re
import sys

from sqlalchemy import create_engine

from app.database.connection import build_dsn


def prepare_statement(stmt: str) -> str:
    """Quita el ';' final de DDL simples, pero lo conserva en bloques PL/SQL (END;)."""
    if not stmt.endswith(";"):
        return stmt
    if re.search(r"\bEND\s*;\s*$", stmt, flags=re.IGNORECASE):
        return stmt
    return stmt[:-1]


def main() -> None:
    if not os.getenv("ORACLE_PWD"):
        raise SystemExit("ORACLE_PWD no está definido. Configúralo en el archivo .env")

    # Fuente única de conexión. Importar connection.py también ejecuta load_dotenv(),
    # por lo que el .env local se carga correctamente fuera de Docker Compose.
    engine = create_engine(build_dsn())
    conn = engine.raw_connection()
    cursor = conn.cursor()

    try:
        script_path = os.path.join("app", "database", "esquema.sql")
        with open(script_path, encoding="utf-8") as f:
            sql_script = f.read()

        statements = re.split(r"^\s*/\s*$", sql_script, flags=re.MULTILINE)
        errores: list[str] = []

        for raw in statements:
            stmt = raw.strip()
            if not stmt:
                continue
            print("Ejecutando bloque...")
            try:
                cursor.execute(prepare_statement(stmt))
                print("Éxito.")
            except Exception as e:
                cabecera = stmt.splitlines()[0]
                detalle = f"Error aplicando objeto ({cabecera}): {e}"
                print(detalle, file=sys.stderr)
                errores.append(detalle)

        if errores:
            conn.rollback()
            print(f"{len(errores)} objeto(s) fallaron. No se confirma el esquema.", file=sys.stderr)
            sys.exit(1)

        conn.commit()
        print("Terminado.")
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    main()
