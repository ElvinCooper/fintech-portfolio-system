import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

# Variables de entorno (defaults orientados a desarrollo local)
DB_USER = os.getenv("DB_USER", "system")
DB_PASSWORD = os.getenv("ORACLE_PWD", "oracle")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "1522")
DB_SERVICE = os.getenv("DB_SERVICE_NAME", "XEPDB1")


def build_dsn(
    user: str = DB_USER,
    password: str = DB_PASSWORD,
    host: str = DB_HOST,
    port: str = DB_PORT,
    service: str = DB_SERVICE,
) -> str:
    """Construye la cadena de conexion Oracle para el driver oracledb."""
    return f"oracle+oracledb://{user}:{password}@{host}:{port}/?service_name={service}"


# URL para conexión Sincrónica (Útil para Alembic y scripts simples)
SYNC_DATABASE_URL = build_dsn()

# URL para conexión Asincrónica (Para la API FastAPI)
ASYNC_DATABASE_URL = SYNC_DATABASE_URL.replace("oracle+oracledb://", "oracle+oracledb_async://", 1)

# Motor de base de datos asíncrono
async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=True, future=True)

# Fábrica de sesiones asíncronas
AsyncSessionLocal = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)


# Dependencia para obtener sesión asíncrona (Recomendada para FastAPI)
async def get_async_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
