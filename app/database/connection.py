import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import create_engine, Session

load_dotenv()

# Variables de entorno
DB_USER = os.getenv("DB_USER", "system")
DB_PASSWORD = os.getenv("ORACLE_PWD", "oracle")
DB_HOST = os.getenv("DB_HOST", "db")  # 'db' es el nombre del servicio en docker-compose
DB_PORT = os.getenv("DB_PORT", "1521")
DB_SERVICE = os.getenv("DB_SERVICE_NAME", "XEPDB1")

# URL para conexión Sincrónica (Útil para Alembic y scripts simples)
SYNC_DATABASE_URL = f"oracle+oracledb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/?service_name={DB_SERVICE}"

# URL para conexión Asincrónica (Para la API FastAPI)
ASYNC_DATABASE_URL = f"oracle+oracledb_async://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/?service_name={DB_SERVICE}"

# Motores de base de datos
sync_engine = create_engine(SYNC_DATABASE_URL, echo=True)
async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=True, future=True)

# Fábrica de sesiones asíncronas
AsyncSessionLocal = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)

# Dependencia para obtener sesión sincrónica (si se requiere)
def get_session():
    with Session(sync_engine) as session:
        yield session

# Dependencia para obtener sesión asíncrona (Recomendada para FastAPI)
async def get_async_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
