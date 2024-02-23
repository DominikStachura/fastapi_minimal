import pytest
import httpx

from fastapi import status


@pytest.mark.asyncio
async def test_health_check(test_client: httpx.AsyncClient):
    response = await test_client.get("/healthcheck")
    assert response.status_code == status.HTTP_200_OK
