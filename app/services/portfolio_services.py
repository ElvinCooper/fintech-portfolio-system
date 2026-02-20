from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select
from app.models.clientes import Clientes
from app.models.cartera import Cartera, AudCartera
from typing import List, Dict, Any


async def get_all_clients(session: AsyncSession):
    """
    Recupera todos los clientes de la base de datos de forma asíncrona.
    """
    result = await session.execute(select(Clientes))
    return result.scalars().all()


async def transferir_saldo(
    session: AsyncSession, 
    id_origen: int, 
    id_destino: int, 
    monto: float
) -> Dict[str, Any]:
    """
    Invoca el procedimiento SP_TRANSFERIR_SALDO en Oracle para transferir saldo entre carteras.
    """
    # Definimos los parámetros, incluyendo los de salida (OUT)
    # En oracledb + sqlalchemy, los OUT se pasan como parámetros normales y se recuperan del result
    sql = text("""
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
    
    # Ejecutamos con bind parameters
    # Nota: Para parámetros OUT en llamadas directas de texto, a veces es necesario usar el cursor crudo
    # pero intentaremos la vía estándar de SQLAlchemy primero.
    result = await session.execute(
        sql,
        {
            "id_origen": id_origen,
            "id_destino": id_destino,
            "monto": monto,
            "codigo_res": 0,    # Marcadores de posición
            "mensaje_res": ""
        }
    )
    
    # Recuperamos los parámetros de salida del contexto de ejecución
    out_params = result.out_parameters
    
    return {
        "codigo": out_params["codigo_res"],
        "mensaje": out_params["mensaje_res"]
    }


async def get_movimientos(session: AsyncSession, id_cartera: int) -> List[Dict[str, Any]]:
    """
    Invoca SP_GET_MOVIMIENTOS para obtener el historial de movimientos vía SYS_REFCURSOR.
    """
    # Para RefCursors en modo asíncrono con oracledb, necesitamos usar el cursor nativo
    # ya que SQLAlchemy no mapea automáticamente RefCursors a objetos de Python en async aún.
    
    # Obtenemos la conexión cruda de oracledb
    conn = await session.connection()
    raw_conn = await conn.get_raw_connection()
    
    # Creamos un cursor de oracledb nativo
    # Nota: raw_conn es un objeto de oracledb.AsyncConnection
    cursor = raw_conn.cursor()
    
    # Definimos la variable de salida para el cursor
    ref_cursor = raw_conn.cursor()
    
    try:
        # Llamada al procedimiento usando la API nativa asíncrona de oracledb
        await cursor.callproc("SP_GET_MOVIMIENTOS", [id_cartera, ref_cursor])
        
        # Recuperamos los datos del RefCursor
        rows = await ref_cursor.fetchall()
        
        # Convertimos a lista de diccionarios (mapeando columnas)
        movimientos = []
        for row in rows:
            movimientos.append({
                "id_cartera": row[0],
                "tipo_operacion": row[1],
                "valor_anterior": row[2],
                "valor_nuevo": row[3],
                "usuario_bd": row[4],
                "fecha_hora": row[5]
            })
        
        return movimientos
    finally:
        await ref_cursor.close()
        await cursor.close()


async def calcular_tasa_interes(
    session: AsyncSession, 
    monto: float, 
    tasa: float, 
    dias: int
) -> float:
    """
    Invoca la función FN_CALCULAR_TASAS de Oracle.
    """
    result = await session.execute(
        text("SELECT FN_CALCULAR_TASAS(:monto, :tasa, :dias) FROM DUAL"),
        {"monto": monto, "tasa": tasa, "dias": dias}
    )
    return result.scalar() or 0.0


async def get_resumen_cartera_vista(session: AsyncSession) -> List[Dict[str, Any]]:
    """
    Consulta la vista VW_RESUMEN_CARTERA.
    """
    result = await session.execute(text("SELECT * FROM VW_RESUMEN_CARTERA"))
    columns = result.keys()
    return [dict(zip(columns, row)) for row in result.all()]
