from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.chat import router as chat_router

app = FastAPI(
    title="BancoBot AI — Agent",
    description="Agente de IA bancário com Agno Framework para o FinBank S.A.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
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
