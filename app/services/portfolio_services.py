from __future__ import annotations

from decimal import Decimal
from typing import Any

from sqlalchemy import Integer, String, bindparam, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.cartera import AudCartera
from app.models.clientes import Clientes


async def get_all_clients(session: AsyncSession):
    """
    Recupera todos los clientes de la base de datos de forma asíncrona.
    """
    result = await session.execute(select(Clientes))
    return result.scalars().all()


async def transferir_saldo(session: AsyncSession, id_origen: int, id_destino: int, monto: Decimal) -> dict[str, Any]:
    """
    Invoca el procedimiento SP_TRANSFERIR_SALDO manejando parámetros OUT de forma manual para máxima compatibilidad.
    """
    # Definimos la sentencia SIN bindparams previos para evitar conflictos de caché
    stmt = text("""
        BEGIN
            SP_TRANSFERIR_SALDO(
                p_id_origen => :id_origen,
                p_id_destino => :id_destino,
                p_monto => :monto,
                p_codigo_res => :codigo_res,
                p_mensaje_res => :mensaje_res
            );
        END;
    """)

    # Declaramos explícitamente los tipos OUT usando bindparams pero en una sola línea
    stmt = stmt.bindparams(
        bindparam("codigo_res", type_=Integer, isoutparam=True),
        bindparam("mensaje_res", type_=String, isoutparam=True),
    )

    # IMPORTANTE: Pasamos valores iniciales para los parámetros OUT
    params = {
        "id_origen": id_origen,
        "id_destino": id_destino,
        "monto": monto,
        "codigo_res": 0,  # Valor inicial requerido
        "mensaje_res": "",  # Valor inicial requerido
    }

    result = await session.execute(stmt, params)

    # Si no se pueden recuperar los parámetros OUT es un error controlado:
    # jamás se convierte un fallo en un éxito.
    try:
        res = {
            "codigo": result.out_parameters["codigo_res"],
            "mensaje": result.out_parameters["mensaje_res"],
        }
    except Exception as e:
        await session.rollback()
        return {"codigo": 2, "mensaje": f"No se pudieron recuperar los parámetros de salida de la transferencia: {e}"}

    # El procedimiento interno gestiona COMMIT/ROLLBACK; se deja la transacción consistente.
    await session.commit()
    return res


async def get_movimientos(session: AsyncSession, id_cartera: int) -> list[dict[str, Any]]:
    """
    Obtiene el historial de movimientos consultando directamente la tabla de auditoría.
    """
    query = select(AudCartera).where(AudCartera.id_cartera == id_cartera).order_by(AudCartera.fecha_hora.desc())
    result = await session.execute(query)
    movs = result.scalars().all()

    return [
        {
            "id_cartera": m.id_cartera,
            "tipo_operacion": m.tipo_operacion,
            "valor_anterior": m.valor_anterior,
            "valor_nuevo": m.valor_nuevo,
            "usuario_bd": m.usuario_bd,
            "fecha_hora": m.fecha_hora,
        }
        for m in movs
    ]


async def calcular_tasa_interes(session: AsyncSession, monto: float, tasa: float, dias: int) -> float:
    """
    Invoca la función FN_CALCULAR_TASAS de Oracle.
    """
    result = await session.execute(
        text("SELECT FN_CALCULAR_TASAS(:monto, :tasa, :dias) FROM DUAL"),
        {"monto": monto, "tasa": tasa, "dias": dias},
    )
    return result.scalar() or 0.0


async def get_resumen_cartera_vista(session: AsyncSession) -> list[dict[str, Any]]:
    """
    Consulta la vista VW_RESUMEN_CARTERA.
    """
    result = await session.execute(text("SELECT * FROM VW_RESUMEN_CARTERA"))
    columns = result.keys()
    return [dict(zip(columns, row)) for row in result.all()]
