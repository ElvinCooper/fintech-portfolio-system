from sqlalchemy import create_engine, text

user = "system"
password = "Myoraclesecret"
host = "localhost"
port = "1522"
service = "XEPDB1"

url = f"oracle+oracledb://{user}:{password}@{host}:{port}/?service_name={service}"
engine = create_engine(url)

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
