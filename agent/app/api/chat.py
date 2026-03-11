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


class FileResponse(BaseModel):
    content_type: str
    content: str  # Base64
    filename: str


class ChatResponse(BaseModel):
    session_id: str
    message: str
    account_id: str
    files: list[FileResponse] = []
    tools_called: list[str] = []


@router.post("", response_model=ChatResponse)
async def chat(
    payload: ChatRequest,
    current_user: dict = Depends(get_current_user),
    jwt_token: str = Depends(extract_token),
):
    """
    Send a message to the BankBot AI agent.

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
        response = await agent.arun(payload.message)
        answer = response.content if hasattr(response, "content") else str(response)
        
        # Extract and clear files from session state
        files_to_send = response.session_state.get("files", [])
        tools_called = [tool.tool_name for tool in response.tools]

        response.session_state["files"] = []
        
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Agent error: {str(exc)}")

    # Persist lightweight metadata in Redis (TTL 30 min)
    session = await get_session(session_id)
    session.update({"account_id": account_id, "last_message": payload.message[:200]})
    await set_session(session_id, session)

    return ChatResponse(
        session_id=session_id,
        message=answer,
        account_id=account_id,
        files=files_to_send,
        tools_called=tools_called
    )


@router.delete("/{session_id}", status_code=204)
async def end_session(
    session_id: str,
    _: dict = Depends(get_current_user),
):
    """Explicitly end a chat session and clear Redis context."""
    from app.core.redis_client import delete_session
    await delete_session(session_id)
