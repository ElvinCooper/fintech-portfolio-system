from sqlmodel import Field, SQLModel, Relationship
from decimal import Decimal
from cartera import Cartera


class Producto(SQLModel, table=True):
    __tablename__ = "productos"

    id : int = Field(primary_key=True)
    descripcion: str = Field(nullable=False, max_length=40)
    precio_standar: Decimal = Field(max_digits=10, decimal_places=2)
    cartera_id: int = Field(foreign_key="cartera.id", nullable=False)
    categoria_producto_id: int = Field(foreign_key="categoria_producto.id", nullable=False)

    # campos para relaciones
    categoria: "CategoriaProducto" = Relationship(back_populates="productos")
    cartera: "Cartera" = Relationship(back_populates="productos")


class CategoriaProducto(SQLModel, table=True):
    __tablename__ = "categoria_productos"

    id: int = Field(primary_key=True)
    descripcion: str = Field(nullable=False, max_length=40)

    # campo para relaciones
    producto: Producto = Relationship(back_populates="categoria_productos")