"""
Chat API endpoint.
POST /chat — receives user message + JWT, returns agent response.
Agno session state is persisted in SQLite (via SqliteDb).
Redis is retained for lightweight session metadata (account_id, last message).
"""

import uuid
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.core.security import get_current_user, extract_token
from app.core.redis_client import get_session, set_session
from app.agents.orchestrator import build_orchestrator

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None


class ChatResponse(BaseModel):
    session_id: str
    message: str
    account_id: str


@router.post("", response_model=ChatResponse)
async def chat(
    payload: ChatRequest,
    current_user: dict = Depends(get_current_user),
    jwt_token: str = Depends(extract_token),
):
    """
    Send a message to the BancoBot AI agent.

    - JWT is verified by the agent (extracts user_id and account_id)
    - The same JWT is forwarded to all backend API calls
    - Agno session state is persisted in SQLite and keyed by session_id
    - Redis stores lightweight metadata (account_id, last_message) for 30 min
    """
    account_id = current_user.get("account_id")
    session_id = payload.session_id or str(uuid.uuid4())

    # Build agent with user's JWT and session context for agno session_state
    agent = build_orchestrator(
        jwt_token=jwt_token,
        session_id=session_id,
        account_id=account_id,
    )

    try:
        # Explicitly load session_state since it might not be auto-loaded
        try:
            db_state = agent.get_session_state()
            if db_state:
                agent.session_state = db_state
        except Exception:
            pass # Fresh session, DB record not created yet
        
        # Initialize default state variables if this is a new session
        if agent.session_state is None:
            agent.session_state = {}
        if "account_id" not in agent.session_state:
            agent.session_state["account_id"] = account_id
        if "pending_operation" not in agent.session_state:
            agent.session_state["pending_operation"] = None
        if "last_query" not in agent.session_state:
            agent.session_state["last_query"] = None

        response = await agent.arun(payload.message)
        answer = response.content if hasattr(response, "content") else str(response)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro no agente: {str(exc)}")

    # Persist lightweight metadata in Redis (TTL 30 min)
    session = await get_session(session_id)
    session.update({"account_id": account_id, "last_message": payload.message[:200]})
    await set_session(session_id, session)

    return ChatResponse(
        session_id=session_id,
        message=answer,
        account_id=account_id,
    )


@router.delete("/{session_id}", status_code=204)
async def end_session(
    session_id: str,
    _: dict = Depends(get_current_user),
):
    """Explicitly end a chat session and clear Redis context."""
    from app.core.redis_client import delete_session
    await delete_session(session_id)
