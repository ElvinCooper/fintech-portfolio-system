from __future__ import annotations

from unittest.mock import MagicMock

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.connection import get_async_session
from app.main import app


@pytest.fixture
def mock_session():
    """Fixture para crear un mock de AsyncSession."""
    session = MagicMock(spec=AsyncSession)
    return session


@pytest_asyncio.fixture
async def client(mock_session):
    """Fixture para el cliente de pruebas de FastAPI con sesión inyectada."""

    async def override_get_async_session():
        yield mock_session

    app.dependency_overrides[get_async_session] = override_get_async_session
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
