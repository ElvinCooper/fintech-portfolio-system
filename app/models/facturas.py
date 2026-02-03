from sqlmodel import SQLModel, Field, Relationship
from decimal import Decimal
from cartera import Cartera
from pagos import Pagos


class Factura(SQLModel, table=True):
    __tablename__ = "facturas"

    id: int = Field(primary_key=True)
    num_factura:str = Field(unique=True, index=True, max_length=6)
    monto_total: Decimal = Field(max_digits=10, decimal_places=2)
    monto_pagado: Decimal = Field(max_digits=10, decimal_places=2)
    estado_pago: str = Field(nullable=False, max_length=12)
    cartera_id: int = Field(foreign_key="cartera.id")

    # campos para relaciones
    cartera: Cartera = Relationship(back_populates="facturas")
    pagos: Pagos = Relationship(back_populates="facturas")