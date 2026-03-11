import asyncio
from app.agents.orchestrator import build_orchestrator

def main():
    agent = build_orchestrator(session_id="test", jwt_token="fake")
    print("Type of save_session:", type(agent.save_session))
    print("Type of update_session_state:", type(agent.update_session_state))

if __name__ == "__main__":
    main()
