from sqlmodel import SQLModel, Field, Relationship
from decimal import Decimal
from datetime import datetime
from facturas import Factura


class Pagos(SQLModel, table=True):
    __tablename__ = "pagos"

    id: int = Field(primary_key=True)
    factura_id: int = Field(foreign_key="facturas.id")
    fecha_pago: datetime = Field(default_factory=datetime.now)
    monto_pago: Decimal = Field(max_digits=10, decimal_places=2)
    metodo_pago: str = Field(nullable=False, max_length=12)

    # campo para relaciones
    factura: Factura = Relationship(back_populates="pagos")