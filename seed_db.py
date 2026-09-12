from datetime import datetime, timedelta
from decimal import Decimal

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Reutiliza la construcción de URL de la capa de base de datos (fuente única)
from app.database.connection import build_dsn
from app.models.cartera import Cartera
from app.models.clientes import Clientes, TipoClientes
from app.models.facturas import Factura
from app.models.pagos import Pagos
from app.models.productos import CategoriaProducto, Producto

engine = create_engine(build_dsn(), echo=True)
SessionLocal = sessionmaker(bind=engine)


def seed():
    session = SessionLocal()
    try:
        print("Poblando tipos de clientes...")
        tipos = [
            TipoClientes(id=1, descripcion="Persona Física"),
            TipoClientes(id=2, descripcion="Empresa Corporativa"),
            TipoClientes(id=3, descripcion="PYME"),
        ]
        session.add_all(tipos)

        print("Poblando categorías de productos...")
        categorias = [
            CategoriaProducto(id=1, descripcion="Préstamos Personales"),
            CategoriaProducto(id=2, descripcion="Tarjetas de Crédito"),
            CategoriaProducto(id=3, descripcion="Líneas de Crédito"),
        ]
        session.add_all(categorias)

        print("Poblando productos...")
        productos = [
            Producto(
                id=1,
                descripcion="Préstamo Rápido 12m",
                precio_standar=Decimal("1500.00"),
                categoria_producto_id=1,
            ),
            Producto(
                id=2,
                descripcion="Visa Platinum FinTech",
                precio_standar=Decimal("5000.00"),
                categoria_producto_id=2,
            ),
            Producto(
                id=3,
                descripcion="Crédito PYME Expansión",
                precio_standar=Decimal("25000.00"),
                categoria_producto_id=3,
            ),
        ]
        session.add_all(productos)

        print("Poblando clientes...")
        clientes = [
            Clientes(
                id=1,
                nombre="Juan Pérez",
                email="juan.perez@email.com",
                telefono="8091112222",
                direccion="Calle Central 10, SD",
                estado="ACTIVO",
                id_tipo_cliente=1,
            ),
            Clientes(
                id=2,
                nombre="Tech Solutions SRL",
                email="contacto@techsolutions.com",
                telefono="8093334444",
                direccion="Av. Lope de Vega 45",
                estado="ACTIVO",
                id_tipo_cliente=2,
            ),
        ]
        session.add_all(clientes)

        session.flush()  # Para asegurar IDs antes de carteras

        print("Poblando carteras iniciales...")
        carteras = [
            Cartera(
                id=1,
                cliente_id=1,
                producto_id=1,
                saldo_pendiente=Decimal("12500.50"),
                fecha_inicio=datetime.now() - timedelta(days=30),
                proximo_vencimiento=datetime.now() + timedelta(days=5),
            ),
            Cartera(
                id=2,
                cliente_id=1,
                producto_id=2,
                saldo_pendiente=Decimal("4500.00"),
                fecha_inicio=datetime.now() - timedelta(days=15),
                proximo_vencimiento=datetime.now() + timedelta(days=15),
            ),
            Cartera(
                id=3,
                cliente_id=2,
                producto_id=3,
                saldo_pendiente=Decimal("150000.00"),
                fecha_inicio=datetime.now() - timedelta(days=60),
                proximo_vencimiento=datetime.now() + timedelta(days=1),
            ),
        ]
        session.add_all(carteras)

        print("Poblando facturas de prueba...")
        facturas = [
            Factura(
                id=1,
                num_factura="F00001",
                monto_total=Decimal("1200.00"),
                monto_pagado=Decimal("0.00"),
                estado_pago="PENDIENTE",
                cartera_id=1,
            ),
            Factura(
                id=2,
                num_factura="F00002",
                monto_total=Decimal("500.00"),
                monto_pagado=Decimal("500.00"),
                estado_pago="PAGADO",
                cartera_id=2,
            ),
        ]
        session.add_all(facturas)

        print("Poblando pagos realizados...")
        pagos = [
            Pagos(
                id=1,
                factura_id=2,
                monto_pago=Decimal("500.00"),
                metodo_pago="TRANSFERENCIA",
                fecha_pago=datetime.now() - timedelta(days=2),
            )
        ]
        session.add_all(pagos)

        session.commit()
        print("¡Base de datos poblada con éxito! 🚀")
    except Exception as e:
        session.rollback()
        print(f"Error poblando la base de datos: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    seed()
