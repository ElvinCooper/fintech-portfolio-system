from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest


@pytest.mark.asyncio
async def test_health_check(client):
    """Prueba el endpoint de salud."""
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "portfolio-api"}


@pytest.mark.asyncio
async def test_get_clientes(client):
    """Prueba el endpoint de listar clientes usando mock de servicio."""
    mock_clientes = [
        {"id": 1, "nombre": "Cliente Test", "email": "test@test.com", "direccion": "Calle Test", "estado": "ACTIVO"}
    ]

    with patch("app.services.portfolio_services.get_all_clients", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = mock_clientes
        response = await client.get("/clientes/")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["nombre"] == "Cliente Test"
        assert data[0]["email"] == "test@test.com"
        mock_get.assert_called_once()


@pytest.mark.asyncio
async def test_transferir_saldo_success(client):
    """Prueba la transferencia exitosa de saldo."""
    payload = {"id_origen": 1, "id_destino": 2, "monto": 500.0}
    mock_res = {"codigo": 0, "mensaje": "Transferencia exitosa."}

    with patch("app.services.portfolio_services.transferir_saldo", new_callable=AsyncMock) as mock_service:
        mock_service.return_value = mock_res
        response = await client.post("/cartera/transferir", json=payload)

        assert response.status_code == 200
        assert response.json() == {"message": "Transferencia exitosa."}
        mock_service.assert_called_once()


@pytest.mark.asyncio
async def test_transferir_saldo_error(client):
    """Prueba el error en la transferencia de saldo."""
    payload = {"id_origen": 1, "id_destino": 2, "monto": 50000.0}
    mock_res = {"codigo": 1, "mensaje": "Saldo insuficiente."}

    with patch("app.services.portfolio_services.transferir_saldo", new_callable=AsyncMock) as mock_service:
        mock_service.return_value = mock_res
        response = await client.post("/cartera/transferir", json=payload)

        assert response.status_code == 400
        assert response.json()["detail"] == "Saldo insuficiente."


@pytest.mark.asyncio
async def test_get_movimientos(client):
    """Prueba el endpoint de movimientos usando mock de servicio."""
    mock_movimientos = [
        {"id_cartera": 1, "tipo_operacion": "INSERT", "valor_anterior": None, "valor_nuevo": "500.00"}
    ]

    with patch("app.services.portfolio_services.get_movimientos", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = mock_movimientos
        response = await client.get("/cartera/movimientos/1")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["tipo_operacion"] == "INSERT"
        mock_get.assert_called_once()


@pytest.mark.asyncio
async def test_get_resumen(client):
    """Prueba el endpoint del resumen consolidado usando mock de servicio."""
    mock_resumen = [{"cliente": "Cliente Test", "saldo_pendiente": "1500.00"}]

    with patch("app.services.portfolio_services.get_resumen_cartera_vista", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = mock_resumen
        response = await client.get("/cartera/resumen")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["saldo_pendiente"] == "1500.00"
        mock_get.assert_called_once()
