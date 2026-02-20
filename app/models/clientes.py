from __future__ import annotations

from datetime import datetime

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel


class TipoClientes(SQLModel, table=True):
    __tablename__ = "tipo_clientes"

    id: int = Field(default=None, primary_key=True)
    descripcion: str = Field(nullable=False, max_length=40)

    # Relación corregida: el nombre del campo debe coincidir con back_populates en Clientes
    clientes: list[Clientes] = Relationship(back_populates="tipo_cliente")


class Clientes(SQLModel, table=True):
    __tablename__ = "clientes"

    id: int = Field(default=None, primary_key=True)
    nombre: str = Field(nullable=False, max_length=40)
    telefono: str = Field(nullable=True, max_length=15)
    email: EmailStr = Field(nullable=False, max_length=40)
    direccion: str = Field(nullable=False, max_length=40)
    fecha_registro: datetime = Field(default_factory=datetime.now)
    estado: str = Field(nullable=False, max_length=12)
    id_tipo_cliente: int = Field(foreign_key="tipo_clientes.id")

    # Relación corregida
    tipo_cliente: TipoClientes = Relationship(back_populates="clientes")

    # Relación con cartera (añadida para consistencia)
    cartera: list[Cartera] = Relationship(back_populates="clientes")
