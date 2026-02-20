from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.connection import get_async_session
from app.models.clientes import Clientes
from app.services import portfolio_services

router = APIRouter(
    prefix="/clientes",
    tags=["Clientes"],
)


@router.get("/", response_model=list[Clientes])
async def get_clients(session: AsyncSession = Depends(get_async_session)):
    """
    Obtiene una lista de todos los clientes de forma asíncrona.
    """
    return await portfolio_services.get_all_clients(session=session)
