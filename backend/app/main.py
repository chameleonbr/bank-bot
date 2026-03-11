from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.mock.seed import seed_database
from app.routers import auth, banking, pix, ted, investments, credit, support

app = FastAPI(
    title="BancoBot AI — Backend",
    description="API bancária REST para o chatbot FinBank S.A.",
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

# Seed mock data on startup
@app.on_event("startup")
def on_startup():
    seed_database()

# Register routers
app.include_router(auth.router)
app.include_router(banking.router)
app.include_router(pix.router)
app.include_router(ted.router)
app.include_router(investments.router)
app.include_router(credit.router)
app.include_router(support.router)


@app.get("/", tags=["health"])
def health():
    return {"status": "ok", "service": "BancoBot Backend", "version": "1.0.0"}
