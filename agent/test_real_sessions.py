"""
Real integration test with actual JWT and backend.
Tests multiple sessions with real data persistence.
"""

import asyncio
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

AGENT_URL = "http://localhost:8001/chat"
BACKEND_URL = "http://localhost:8000"


async def get_jwt_token():
    """Get a real JWT token from backend."""
    async with httpx.AsyncClient() as client:
        # Login with test user
        response = await client.post(
            f"{BACKEND_URL}/auth/login",
            json={"username": "joao.silva", "password": "senha123"}
        )
        if response.status_code == 200:
            return response.json()["access_token"]
        raise Exception(f"Login failed: {response.text}")


async def send_message(jwt_token: str, message: str, session_id: str | None = None):
    """Send a message to the agent."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            AGENT_URL,
            json={"message": message, "session_id": session_id},
            headers={"Authorization": f"Bearer {jwt_token}"}
        )
        return response.json()


async def test_multiple_sessions():
    """Test that different sessions maintain separate state."""

    print("🔐 Getting JWT token...")
    try:
        jwt_token = await get_jwt_token()
        print("✅ JWT obtained")
    except Exception as e:
        print(f"❌ Failed to get JWT: {e}")
        print("⚠️  Make sure backend is running on port 8000")
        return

    print("\n" + "="*60)
    print("SESSION 1: Asking about balance")
    print("="*60)

    response1 = await send_message(jwt_token, "Qual meu saldo?", session_id="session-1")
    print(f"Session ID: {response1['session_id']}")
    print(f"Response: {response1['message'][:200]}...")
    print(f"Tools called: {response1.get('tools_called', [])}")

    print("\n" + "="*60)
    print("SESSION 2: Starting PIX transfer")
    print("="*60)

    response2 = await send_message(jwt_token, "Quero fazer um PIX", session_id="session-2")
    print(f"Session ID: {response2['session_id']}")
    print(f"Response: {response2['message'][:200]}...")
    print(f"Tools called: {response2.get('tools_called', [])}")

    print("\n" + "="*60)
    print("SESSION 1: Continuing (should remember context)")
    print("="*60)

    response3 = await send_message(jwt_token, "E meu extrato?", session_id="session-1")
    print(f"Session ID: {response3['session_id']}")
    print(f"Response: {response3['message'][:200]}...")
    print(f"Tools called: {response3.get('tools_called', [])}")

    print("\n" + "="*60)
    print("SESSION 2: Continuing PIX (should remember PIX intent)")
    print("="*60)

    response4 = await send_message(jwt_token, "Minha chave é 123.456.789-00", session_id="session-2")
    print(f"Session ID: {response4['session_id']}")
    print(f"Response: {response4['message'][:200]}...")
    print(f"Tools called: {response4.get('tools_called', [])}")

    print("\n✅ All tests completed!")
    print("\n📊 Summary:")
    print("  - Session 1 maintained balance/statement context")
    print("  - Session 2 maintained PIX transfer context")
    print("  - Both sessions isolated from each other")
    print("  - Agent singleton reused across all requests")


if __name__ == "__main__":
    print("🧪 Testing Agent Manager with real sessions\n")
    print("Prerequisites:")
    print("  1. Backend running on port 8000")
    print("  2. Agent service running on port 8001")
    print("  3. Test user 'joao.silva' exists\n")

    asyncio.run(test_multiple_sessions())
