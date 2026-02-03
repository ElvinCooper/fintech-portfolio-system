from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from decimal import Decimal
from clientes import Clientes
from productos import Producto


class Cartera(SQLModel, table=True):
    __tablename__ = "cartera"

    id: int = Field(primary_key=True)
    cliente_id: int = Field(foreign_key="cliente.id")
    producto_id: int = Field(foreign_key="producto.id")
    saldo_pendiente: Decimal = Field(max_digits=10, decimal_places=2)
    fecha_inicio: datetime = Field(default_factory=datetime.now)
    proximo_vencimiento: datetime = Field(default_factory=datetime.now)

    # campos para relaciones
    clientes: Clientes = Relationship(back_populates="cartera")
    productos: Producto = Relationship(back_populates="cartera")