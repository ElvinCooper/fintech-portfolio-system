from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlmodel import Field, Relationship, SQLModel


class Cartera(SQLModel, table=True):
    __tablename__ = "cartera"

    id: int = Field(default=None, primary_key=True)
    cliente_id: int = Field(foreign_key="clientes.id")
    producto_id: int = Field(foreign_key="productos.id")
    saldo_pendiente: Decimal = Field(max_digits=10, decimal_places=2)
    fecha_inicio: datetime = Field(default_factory=datetime.now)
    proximo_vencimiento: datetime = Field(default_factory=datetime.now)

    # campos para relaciones
    clientes: Clientes = Relationship(back_populates="cartera")
    producto: Producto = Relationship(back_populates="carteras")
    facturas: list[Factura] = Relationship(back_populates="cartera")


class AudCartera(SQLModel, table=True):
    __tablename__ = "aud_cartera"

    id: int = Field(default=None, primary_key=True)
    id_cartera: int = Field(nullable=False)
    tipo_operacion: str = Field(max_length=10)
    valor_anterior: str = Field(nullable=True, max_length=20)
    valor_nuevo: str = Field(nullable=True, max_length=20)
    usuario_bd: str = Field(max_length=30)
    fecha_hora: datetime = Field(default_factory=datetime.now)
