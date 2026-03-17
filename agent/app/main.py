from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api.chat import router as chat_router
from app.core.agent_manager import agent_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize agent on startup, cleanup on shutdown."""
    # Startup: Initialize the agent once
    agent_manager.initialize()
    yield
    # Shutdown: cleanup if needed
    pass


app = FastAPI(
    title="BankBot AI — Agent",
    description="Banking AI Agent powered by Agno Framework for FinBank S.A.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)


@app.get("/", tags=["health"])
def health():
    return {"status": "ok", "service": "BancoBot Agent", "version": "1.0.0"}
