# BancoBot AI — Walkthrough

## O que foi criado

Dois projetos Python completos em `/mnt/d/Projetos/bankBot/`, mais um `docker-compose.yml` na raiz.

---

## Estrutura Final

```
bankBot/
├── docker-compose.yml          ← backend + agent + redis
├── backend/                    ← FastAPI + SQLite + JWT
│   ├── Dockerfile
│   ├── pyproject.toml          (uv, hatchling, 47 deps)
│   └── app/
│       ├── main.py             ← FastAPI app, seed on startup
│       ├── core/               config · database · security (JWT)
│       ├── models/             10 ORM models (SQLAlchemy)
│       ├── schemas/            7 Pydantic schemas
│       ├── routers/            6 routers (auth, banking, pix, ted, investments, credit+financing, support)
│       └── mock/               data.py + seed.py
└── agent/                      ← Agno + FastAPI + Redis
    ├── Dockerfile
    ├── pyproject.toml          (uv, hatchling, 60 deps)
    └── app/
        ├── main.py             ← FastAPI app
        ├── core/               config · security (JWT verify) · redis_client
        ├── client/             backend_client.py (JWT forwarding)
        ├── agents/             orchestrator.py (Agno Agent)
        ├── toolkits/           7 toolkits (Banking, PIX, TED, Investment, Credit, Loan, Support)
        ├── api/                chat.py (POST /chat)
        └── skills/             10 × SKILL.md folders
```

---

## Mock Data por Usuário

| account_id | Titular | Saldo | Investimentos | Empréstimos | Financiamentos |
|---|---|---|---|---|---|
| ACC001 | Ana Paula Souza | R$ 4.820,50 | CDB + LCI + Tesouro Selic | Pessoal 24x | — |
| ACC002 | Carlos Eduardo Lima | R$ 12.310,00 | CDB + Fundo Multimercado | — | Veículo 48x |
| ACC003 | Fernanda Costa Ltda (PJ) | R$ 87.650,00 | CDB + LCA + Fundo RF | Empresarial 60x | Imóvel 360x |
| ACC004 | Roberto Martins | R$ 2.100,75 | Poupança + Tesouro IPCA+ | Pessoal + Consignado | — |

---

## Rotas do Backend (`localhost:8000/docs`)

| Método | Rota | Descrição |
|---|---|---|
| POST | `/auth/login` | Login com `account_id` + `pin` → JWT |
| POST | `/auth/refresh` | Renovar JWT |
| GET | `/banking/balance` | Saldo da conta |
| GET | `/banking/statement` | Extrato com filtros |
| GET/POST/DELETE | `/banking/contacts` | Agenda de contatos |
| GET/DELETE | `/banking/scheduled` | Operações agendadas |
| POST | `/pix/transfer` | PIX imediato |
| POST | `/pix/schedule` | PIX agendado |
| GET/POST/DELETE | `/pix/keys` | Gerenciar chaves PIX |
| GET/PUT | `/pix/limits` | Limites PIX |
| POST | `/ted/transfer` | TED |
| GET | `/ted/banks` | Lista de bancos |
| GET | `/investments/portfolio` | Carteira de investimentos |
| POST | `/investments/simulate` | Simular investimento |
| POST | `/investments/invest` | Aplicar |
| GET | `/credit/loans` | Empréstimos ativos |
| POST | `/credit/simulate-loan` | Simular empréstimo |
| POST | `/credit/simulate-financing` | Simular financiamento |
| GET | `/credit/financings` | Financiamentos ativos |
| POST | `/support/tickets` | Abrir chamado |
| GET | `/support/faq` | FAQ |
| POST | `/support/escalate` | Escalar para humano |

---

## API do Agent (`localhost:8001/docs`)

| Método | Rota | Descrição |
|---|---|---|
| POST | `/chat` | Enviar mensagem ao BancoBot AI |
| DELETE | `/chat/{session_id}` | Encerrar sessão |

**Fluxo JWT:**
1. Usuário faz `POST /auth/login` no backend → recebe JWT
2. Envia ao agent via `Authorization: Bearer <jwt>`
3. Agent verifica JWT, extrai `account_id`
4. Repassa o mesmo JWT ao backend em cada chamada de tool

---

## Skills (`agent/app/skills/`)

Cada skill é uma pasta com `SKILL.md` seguindo o padrão AgnoSkills:

| Skill | Agente | Responsabilidade |
|---|---|---|
| `intent-classification` | Orchestrator | Mapeia intenção → agente correto |
| `context-retention` | Orchestrator | Mantém contexto entre turnos (Redis, TTL 30min) |
| `transaction-skill` | Banking | Fluxo completo PIX e TED com confirmação |
| `statement-skill` | Banking | Formatação de saldos e extratos em PT-BR |
| `portfolio-skill` | Investment | Apresentação da carteira com educação financeira |
| `investment-recommendation` | Investment | Recomendação por perfil + simulação |
| `loan-simulation` | Credit | Simulação comparativa de empréstimo e financiamento |
| `credit-management` | Credit | Visão consolidada de dívidas e portabilidade |
| `manager-communication` | Support | Agendamento e mensagens ao gerente |
| `escalation-skill` | Support | Transição suave para atendimento humano |

---

## Como executar

**Via docker-compose (recomendado):**
```bash
cd /mnt/d/Projetos/bankBot
cp backend/.env.example backend/.env
cp agent/.env.example agent/.env
# Edite agent/.env com seu OPENAI_API_KEY
docker-compose up --build
```

**Via uv (desenvolvimento):**
```bash
# Backend
cd backend && uv sync && uv run uvicorn app.main:app --reload --port 8000

# Agent (nova aba)
cd agent && uv sync && uv run uvicorn app.main:app --reload --port 8001
```

**Teste rápido:**
```bash
# 1. Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"account_id": "ACC001", "pin": "1234"}'

# 2. Usar o JWT retornado para consultar saldo
curl http://localhost:8000/banking/balance \
  -H "Authorization: Bearer <JWT_DO_PASSO_1>"

# 3. Chat com o agente
curl -X POST http://localhost:8001/chat \
  -H "Authorization: Bearer <JWT_DO_PASSO_1>" \
  -H "Content-Type: application/json" \
  -d '{"message": "Qual é o meu saldo?"}'
```

---

## Validação

- ✅ `uv sync` executado com sucesso no backend (47 pacotes)
- ✅ `uv sync` executado com sucesso no agent (60 pacotes)
- ✅ FAQ syntax bug corrigido em `mock/data.py`
- ✅ Import limpo de `get_current_user` em `auth.py`
- ✅ Hatchling flat-layout configurado em ambos `pyproject.toml`
