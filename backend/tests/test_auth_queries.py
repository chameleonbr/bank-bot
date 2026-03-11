import httpx
import pytest

BASE_URL = "http://127.0.0.1:8000"

@pytest.mark.asyncio
async def test_auth_and_queries():
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        # 1. Login
        login_data = {
            "account_id": "ACC001",
            "pin": "1234"
        }
        login_response = await client.post("/auth/login", json=login_data)
        assert login_response.status_code == 200
        
        auth_data = login_response.json()
        token = auth_data["access_token"]
        assert token is not None
        assert auth_data["account_id"] == "ACC001"
        
        headers = {"Authorization": f"Bearer {token}"}
        
        # 2. Query Balance
        balance_response = await client.get("/banking/balance", headers=headers)
        assert balance_response.status_code == 200
        balance_data = balance_response.json()
        assert "balance_total" in balance_data
        assert balance_data["account_id"] == "ACC001"
        
        # 3. Query Statement
        statement_response = await client.get("/banking/statement", headers=headers)
        assert statement_response.status_code == 200
        statement_data = statement_response.json()
        assert "transactions" in statement_data
        assert len(statement_data["transactions"]) > 0
        
        # 4. Query Investment Products
        investments_response = await client.get("/investments/products", headers=headers)
        assert investments_response.status_code == 200
        investments_data = investments_response.json()
        assert isinstance(investments_data, list)
        assert len(investments_data) > 0
        assert "name" in investments_data[0]
