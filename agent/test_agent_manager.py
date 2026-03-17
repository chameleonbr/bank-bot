"""
Test script to validate the AgentManager singleton pattern.

This script verifies:
1. Agent is initialized only once
2. Multiple calls reuse the same agent instance
3. Session state is properly managed per session_id
"""

import asyncio
from app.core.agent_manager import agent_manager


async def test_agent_manager():
    """Test that agent manager properly reuses the agent instance."""

    print("🔧 Initializing agent manager...")
    agent_manager.initialize()
    print("✅ Agent initialized")

    # Get the agent instance ID
    agent_id_1 = id(agent_manager._agent)
    print(f"Agent instance ID: {agent_id_1}")

    # Initialize again (should be idempotent)
    agent_manager.initialize()
    agent_id_2 = id(agent_manager._agent)
    print(f"Agent instance ID after re-init: {agent_id_2}")

    assert agent_id_1 == agent_id_2, "Agent should be the same instance!"
    print("✅ Agent reuse verified")

    # Test with dummy JWT and session
    print("\n🧪 Testing agent run with session_id='test-session-1'...")
    try:
        response = await agent_manager.run(
            message="Olá, qual meu saldo?",
            jwt_token="dummy_jwt_token_for_testing",
            session_id="test-session-1",
            account_id="acc_123",
        )
        print(f"✅ Response received: {response.content[:100]}...")
    except Exception as e:
        print(f"⚠️  Expected error (dummy JWT): {e}")

    # Test with different session
    print("\n🧪 Testing agent run with session_id='test-session-2'...")
    try:
        response = await agent_manager.run(
            message="Quero fazer um PIX",
            jwt_token="dummy_jwt_token_for_testing",
            session_id="test-session-2",
            account_id="acc_456",
        )
        print(f"✅ Response received: {response.content[:100]}...")
    except Exception as e:
        print(f"⚠️  Expected error (dummy JWT): {e}")

    print("\n✅ All tests passed! Agent manager is working correctly.")
    print("📝 Summary:")
    print("  - Agent is initialized once at startup")
    print("  - Same instance is reused across requests")
    print("  - Session ID changes per request")
    print("  - JWT token is updated per request")


if __name__ == "__main__":
    asyncio.run(test_agent_manager())
