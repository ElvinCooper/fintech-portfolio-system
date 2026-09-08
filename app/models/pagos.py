from datetime import datetime
from decimal import Decimal

from sqlmodel import Field, Relationship, SQLModel


class Pagos(SQLModel, table=True):
    __tablename__ = "pagos"

    id: int = Field(default=None, primary_key=True)
    factura_id: int = Field(foreign_key="facturas.id")
    fecha_pago: datetime = Field(default_factory=datetime.now)
    monto_pago: Decimal = Field(max_digits=10, decimal_places=2)
    metodo_pago: str = Field(nullable=False, max_length=20)  # Aumentado de 12 a 20

    # campo para relaciones corregido
    factura: "Factura" = Relationship(back_populates="pagos")
