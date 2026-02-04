from sqlmodel import SQLModel
from connection import engine
from app.models.clientes import Clientes, TipoClientes
from app.models.facturas import Factura
from app.models.productos import Producto, CategoriaProducto
from app.models.cartera import Cartera
from app.models.pagos import Pagos


def migrate():
    print("Creando tablas...")
    SQLModel.metadata.create_all(engine)
    print("Migración completa")


if __name__ == "__main__":
    migrate()
