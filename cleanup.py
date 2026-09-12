from sqlalchemy import create_engine, text

from app.database.connection import build_dsn

engine = create_engine(build_dsn())

tables = [
    "ALEMBIC_VERSION",
    "CARTERA",
    "AUD_CARTERA",
    "CATEGORIA_PRODUCTOS",
    "CLIENTES",
    "FACTURAS",
    "PAGOS",
    "PRODUCTOS",
    "TIPO_CLIENTES",
    "TIPO_CLIENTE",
]

with engine.connect() as conn:
    for table in tables:
        try:
            conn.execute(text(f"DROP TABLE {table} CASCADE CONSTRAINTS"))
            print(f"Borrando {table}...")
        except Exception:
            pass
    conn.commit()
print("Limpieza completa.")
