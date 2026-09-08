from connection import engine
from sqlmodel import SQLModel


def migrate():
    print("Creando tablas...")
    SQLModel.metadata.create_all(engine)
    print("Migración completa")


if __name__ == "__main__":
    migrate()
