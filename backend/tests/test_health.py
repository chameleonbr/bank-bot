import httpx
import pytest

@pytest.mark.asyncio
async def test_health_check():
    async with httpx.AsyncClient(base_url="http://127.0.0.1:8000") as client:
        response = await client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "service" in data
        assert "version" in data
