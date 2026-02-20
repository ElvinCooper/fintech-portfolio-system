from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any
from pydantic import BaseModel

from app.database.connection import get_async_session
from app.services import portfolio_services

router = APIRouter(
    prefix="/cartera",
    tags=["Cartera"],
)

# Esquemas para la transferencia
class TransferenciaRequest(BaseModel):
    id_origen: int
    id_destino: int
    monto: float

@router.post("/transferir", status_code=200)
async def transferir_saldo(
    request: TransferenciaRequest,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Realiza una transferencia de saldo entre dos carteras mediante un procedimiento almacenado nativo.
    """
    res = await portfolio_services.transferir_saldo(
        session=session,
        id_origen=request.id_origen,
        id_destino=request.id_destino,
        monto=request.monto
    )
    
    if res["codigo"] != 0:
        raise HTTPException(status_code=400, detail=res["mensaje"])
    
    return {"message": res["mensaje"]}


@router.get("/movimientos/{id_cartera}", response_model=List[Dict[str, Any]])
async def get_movimientos(
    id_cartera: int,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Obtiene el historial de movimientos de una cartera desde un SYS_REFCURSOR de Oracle.
    """
    return await portfolio_services.get_movimientos(session=session, id_cartera=id_cartera)


@router.get("/resumen", response_model=List[Dict[str, Any]])
async def get_resumen_consolidado(
    session: AsyncSession = Depends(get_async_session)
):
    """
    Consulta la vista consolidada VW_RESUMEN_CARTERA para un reporte rápido.
    """
    return await portfolio_services.get_resumen_cartera_vista(session=session)
