from typing import AsyncGenerator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from src.main import app


@pytest_asyncio.fixture
async def async_client() -> AsyncGenerator:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://loc.tst.srv"
    ) as client:
        yield client
