from sqlmodel import Field, SQLModel, Relationship
from decimal import Decimal


class Producto(SQLModel, table=True):
    __tablename__ = "productos"

    id: int = Field(primary_key=True)
    descripcion: str = Field(nullable=False, max_length=40)
    precio_standar: Decimal = Field(max_digits=10, decimal_places=2)
    categoria_producto_id: int = Field(foreign_key="categoria_productos.id", nullable=False)

    # campos para relaciones
    categoria: "CategoriaProducto" = Relationship(back_populates="productos")
    carteras: list["Cartera"] = Relationship(back_populates="producto")


class CategoriaProducto(SQLModel, table=True):
    __tablename__ = "categoria_productos"

    id: int = Field(primary_key=True)
    descripcion: str = Field(nullable=False, max_length=40)

    # campo para relaciones
    productos: list["Producto"] = Relationship(back_populates="categoria")
