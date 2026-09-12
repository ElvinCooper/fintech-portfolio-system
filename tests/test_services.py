from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.services import portfolio_services


@pytest.mark.asyncio
async def test_get_all_clients_service():
    """Prueba la lógica del servicio de listar clientes."""
    mock_session = MagicMock(spec=AsyncSession)
    mock_result = MagicMock()
    mock_scalars = MagicMock()

    # Configurar mocks
    mock_scalars.all.return_value = ["Cliente 1", "Cliente 2"]
    mock_result.scalars.return_value = mock_scalars
    mock_session.execute = AsyncMock(return_value=mock_result)

    res = await portfolio_services.get_all_clients(mock_session)

    assert res == ["Cliente 1", "Cliente 2"]
    mock_session.execute.assert_called_once()


@pytest.mark.asyncio
async def test_transferir_saldo_service():
    """Prueba la lógica del servicio de transferencia invocando PL/SQL."""
    mock_session = MagicMock(spec=AsyncSession)
    mock_result = MagicMock()

    # Simular result.out_parameters de SQLAlchemy
    mock_result.out_parameters = {"codigo_res": 0, "mensaje_res": "Éxito"}
    mock_session.execute = AsyncMock(return_value=mock_result)
    mock_session.commit = AsyncMock()

    res = await portfolio_services.transferir_saldo(mock_session, 1, 2, 100.0)

    assert res["codigo"] == 0
    assert res["mensaje"] == "Éxito"
    mock_session.execute.assert_called_once()
    mock_session.commit.assert_called_once()


@pytest.mark.asyncio
async def test_get_movimientos_service():
    """Prueba la lógica del servicio de consultar movimientos desde AUD_CARTERA."""
    mock_session = MagicMock(spec=AsyncSession)
    mock_result = MagicMock()
    mock_scalars = MagicMock()
    mock_row = MagicMock()
    mock_row.id_cartera = 1
    mock_row.tipo_operacion = "INSERT"
    mock_row.valor_anterior = None
    mock_row.valor_nuevo = "500.00"
    mock_row.usuario_bd = "SYSTEM"
    mock_row.fecha_hora = "2026-02-20 12:00:00"

    mock_scalars.all.return_value = [mock_row]
    mock_result.scalars.return_value = mock_scalars
    mock_session.execute = AsyncMock(return_value=mock_result)

    res = await portfolio_services.get_movimientos(mock_session, id_cartera=1)

    assert res == [
        {
            "id_cartera": 1,
            "tipo_operacion": "INSERT",
            "valor_anterior": None,
            "valor_nuevo": "500.00",
            "usuario_bd": "SYSTEM",
            "fecha_hora": "2026-02-20 12:00:00",
        }
    ]
    mock_session.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_resumen_vista_service():
    """Prueba la lógica del servicio de consultar la vista VW_RESUMEN_CARTERA."""
    mock_session = MagicMock(spec=AsyncSession)
    mock_result = MagicMock()
    mock_result.keys.return_value = ["cliente", "saldo_pendiente"]
    mock_result.all.return_value = [
        ("Cliente Test", "1500.00"),
        ("Cliente Dos", "2500.00"),
    ]
    mock_session.execute = AsyncMock(return_value=mock_result)

    res = await portfolio_services.get_resumen_cartera_vista(mock_session)

    assert res == [
        {"cliente": "Cliente Test", "saldo_pendiente": "1500.00"},
        {"cliente": "Cliente Dos", "saldo_pendiente": "2500.00"},
    ]
    mock_session.execute.assert_called_once()
