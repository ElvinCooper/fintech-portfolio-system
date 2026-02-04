from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from decimal import Decimal


class Cartera(SQLModel, table=True):
    __tablename__ = "cartera"

    id: int = Field(primary_key=True)
    cliente_id: int = Field(foreign_key="clientes.id")
    producto_id: int = Field(foreign_key="productos.id")
    saldo_pendiente: Decimal = Field(max_digits=10, decimal_places=2)
    fecha_inicio: datetime = Field(default_factory=datetime.now)
    proximo_vencimiento: datetime = Field(default_factory=datetime.now)

    # campos para relaciones
    clientes: "Clientes" = Relationship(back_populates="cartera")
    productos: "Producto" = Relationship(back_populates="cartera")
    facturas: list["Factura"] = Relationship(back_populates="cartera")