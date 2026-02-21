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
