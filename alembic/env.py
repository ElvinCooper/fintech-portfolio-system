import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, create_engine
from sqlalchemy import pool
from dotenv import load_dotenv

from alembic import context

# --- ESTO ES LO NUEVO PARA SQLMODEL ---
from sqlmodel import SQLModel
# Añadir el directorio raíz al path para importar los modelos
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))

# Importar modelos a través del __init__ corregido
from app.models import Clientes, TipoClientes, Cartera, Factura, Producto, CategoriaProducto, Pagos
# ---------------------------------------

load_dotenv()

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# target_metadata
target_metadata = SQLModel.metadata

def include_object(object, name, type_, reflected, compare_to):
    if type_ == "table":
        if name.lower().startswith("logmnr") or name.lower().startswith("logstdby"):
            return False
        if name.lower().startswith("ol$") or name.lower().startswith("sys_"):
            return False
    return True

def get_url():
    user = os.getenv("DB_USER", "system")
    password = os.getenv("ORACLE_PWD", "oracle")
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "1522")
    service = os.getenv("DB_SERVICE_NAME", "XEPDB1")
    # Formato más robusto para oracledb
    return f"oracle+oracledb://{user}:{password}@{host}:{port}/?service_name={service}"

def run_migrations_offline() -> None:
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_object=include_object,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    # Crear engine directamente para evitar problemas con engine_from_config y el driver
    url = get_url()
    connectable = create_engine(url, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata,
            include_object=include_object,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
