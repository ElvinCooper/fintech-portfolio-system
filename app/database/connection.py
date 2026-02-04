from sqlmodel import create_engine, Session
import os
from dotenv import load_dotenv

load_dotenv()
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("ORACLE_PWD")

# Cadena de conexión Oracle
DATABASE_URL = f"oracle+oracledb://{DB_USER}:{DB_PASSWORD}@db:1521/XE"


engine = create_engine(
    DATABASE_URL,
    echo=True,  # Para ver queries SQL en consola
)


# Función para obtener sesión
def get_session():
    with Session(engine) as session:
        yield session