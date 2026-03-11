import traceback
from app.agents.orchestrator import _DB_FILE, build_orchestrator
from agno.db.sqlite import SqliteDb

def test_agno_persistence():
    session_id = "test-session-final-123" 
    
    print("--- Turn 1 ---")
    agent1 = build_orchestrator(jwt_token="fake", session_id=session_id)
    # Give the LLM a command to save something in its state
    response1 = agent1.run("Por favor, guarde a informação de que eu quero fazer um pix de 50 reais.")
    print("Agent Response:", response1.content)
    print("State after Turn 1:", agent1.session_state)
    
    print("\n--- Turn 2 ---")
    agent2 = build_orchestrator(jwt_token="fake", session_id=session_id)
    # The state should be populated if Agno's db is working properly
    # However, Agno may only load the state automatically during `.run()` or if we read it manually.
    response2 = agent2.run("Qual era o valor do PIX que eu pedi antes?")
    print("Agent Response:", response2.content)
    print("State after Turn 2:", agent2.session_state)

if __name__ == "__main__":
    try:
        test_agno_persistence()
    except Exception as e:
        traceback.print_exc()
