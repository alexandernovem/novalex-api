from unittest import mock

import pytest


from httpx import AsyncClient
from http import HTTPStatus


@pytest.mark.asyncio
async def test_index(async_client: AsyncClient):
    expected_data = {"status": 200, "coins": []}

    client_mock = mock.AsyncMock(spec=AsyncClient)
    response_mock = mock.AsyncMock(
        status_code=200, json=mock.AsyncMock(return_value={"status": 200, "coins": []})
    )
    client_mock.get.return_value = response_mock

    response = await client_mock.get("api/v1/coins")
    data = await response.json()

    assert response.status_code == HTTPStatus.OK
    assert data == expected_data
