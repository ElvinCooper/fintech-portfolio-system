from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship
from pydantic import EmailStr


class TipoClientes(SQLModel, table=True):
    __tablename__ = 'tipo_clientes'

    id: int = Field(default = 0, primary_key=True)
    descripcion: str = Field(nullable=False, max_length=40)

    cliente: list["Clientes"] = Relationship(back_populates="tipo_clientes")


class Clientes(SQLModel, table=True):
    __tablename__ = "clientes"

    id: int = Field(default = 0, primary_key=True)
    nombre: str = Field(nullable=False, max_length=40)
    telefono: str = Field(nullable=True, max_length=15)
    email: EmailStr = Field(nullable=False, max_length=40)
    direccion: str = Field(nullable=False, max_length=40)
    fecha_registro: datetime = Field(default_factory=datetime.now)
    estado: str = Field(nullable=False, max_length=12)
    id_tipo_cliente: int = Field(foreign_key="tipo_clientes.id")

    # campo para relaciones
    tipo_cliente: "TipoClientes" = Relationship(back_populates="clientes")



