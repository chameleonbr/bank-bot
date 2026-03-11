# 🏦 BancoBot AI

**BancoBot AI** is an intelligent banking virtual assistant developed for the fictional bank **FinBank S.A.** It provides customers with a complete, secure, and efficient digital service experience via chat, 24/7.

Built using the [Agno Framework](https://agno.com), it leverages a multi-agent architecture to handle different banking domains such as transactions, investments, credit, and customer support.

---

## ✨ Key Features

- **Banking Operations**: Check balances, view statements, and manage contact lists.
- **Transfers**: Seamless PIX and TED transfers with validation and scheduling.
- **Investments**: Portfolio overview, product simulations, and simplified investment/redemption.
- **Credit & Loans**: Loan simulations (Personal, Mortgage, Vehicle) and status tracking.
- **Customer Support**: Automated ticket opening, asynchronous manager communication, and seamless human escalation.
- **Mock Data Layer**: Fully functional simulation layer for training and validation without real bank integrations.

---

## 🏗️ Architecture

The project follows a **Multi-Agent System** design:

- **Orchestrator Agent**: The entry point that classifies user intent and routes requests to specialized agents.
- **Specialized Agents**: 
  - `BankingAgent`: Handles daily transactions and account inquiries.
  - `InvestmentAgent`: Manages portfolios and investment recommendations.
  - `CreditAgent`: Conducts loan simulations and debt management.
  - `SupportAgent`: Handles help tickets and office communications.
- **Toolkits**: Modular collections of tools (e.g., `BankingToolkit`, `PIXToolkit`) that provide agents with the necessary capabilities.

---

## 🛠️ Technology Stack

- **Framework**: [Agno](https://agno.com)
- **Backend**: [FastAPI](https://fastapi.tiangolo.com/), [Uvicorn](https://www.uvicorn.org/)
- **Language**: Python 3.12+
- **Database**: SQLite (Local sessions and mock data)
- **Caching**: Redis
- **LLM**: OpenAI / OpenRouter (Gemini)
- **Environment Management**: [uv](https://github.com/astral-sh/uv)
- **Security**: JWT Authentication, HTTPS

---

## 🚀 Getting Started

### Prerequisites

- [uv](https://docs.astral.sh/uv/) installed.
- [Docker](https://www.docker.com/) (optional, for full stack orchestration).
- OpenAI or OpenRouter API Key.

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd bankBot
   ```

2. Setup environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your keys and settings
   ```

3. Install dependencies and run components:

   **For Backend:**
   ```bash
   cd backend
   uv sync
   uv run uvicorn app.main:app --reload
   ```

   **For Agent:**
   ```bash
   cd agent
   uv sync
   uv run uvicorn app.main:app --reload --port 8001
   ```

### Running with Docker Compose

```bash
docker-compose up --build
```

---

## 📁 Project Structure

```text
bankBot/
├── agent/                # Agno Agent service
│   ├── app/
│   │   ├── agents/      # Agent definitions (Orchestrator, etc.)
│   │   ├── api/         # FastAPI routes for chat
│   │   ├── core/        # Configuration and security
│   │   ├── toolkits/    # Agno Toolkits
│   │   └── skills/      # Agent Skills
│   └── ...
├── backend/              # Mock Banking Backend (API)
│   ├── app/
│   │   ├── api/         # Business logic routes
│   │   ├── core/        # Security and settings
│   │   ├── models/      # Data schemas
│   │   └── services/    # Data simulation services
│   └── ...
├── docker-compose.yml    # Full stack orchestration
└── BancoBot_AI_PRD.md    # Product Requirements Document
```

---

## 🧪 Testing

The project uses `pytest` for automated testing.

```bash
uv run pytest
```

---

*FinBank S.A. — Transformando seu atendimento digital.*
