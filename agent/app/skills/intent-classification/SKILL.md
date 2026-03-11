---
name: intent-classification
description: Identifies user intent and maps it to the correct agent and toolkit for the BancoBot AI banking assistant.
---

# Intent Classification Skill

This skill is responsible for identifying what the user wants and routing the request to the correct domain agent.

## Intent Categories

| Intent | Keywords / Signals | Target Agent |
|---|---|---|
| `BALANCE_INQUIRY` | saldo, quanto tenho, conta | BankingAgent |
| `STATEMENT` | extrato, lançamento, movimentação, histórico | BankingAgent |
| `PIX_TRANSFER` | pix, transferir, mandar dinheiro, chave | BankingAgent |
| `TED_TRANSFER` | TED, transferência bancária, outro banco | BankingAgent |
| `CONTACTS` | contatos, favoritos, agenda | BankingAgent |
| `SCHEDULED` | agendado, agendar, recorrente | BankingAgent |
| `PORTFOLIO` | investimento, carteira, CDB, rendimento | InvestmentAgent |
| `SIMULATE_INVESTMENT` | simular, quanto rende, aplicar | InvestmentAgent |
| `LOAN` | empréstimo, crédito, parcelas | CreditAgent |
| `FINANCING` | financiamento, imóvel, veículo, SAC, PRICE | CreditAgent |
| `CREDIT_SCORE` | score, pontuação, crédito disponível | CreditAgent |
| `SUPPORT_TICKET` | problema, reclamação, chamado, suporte | SupportAgent |
| `MANAGER` | gerente, falar com alguém, atendimento | SupportAgent |
| `ESCALATE` | atendente, humano, quero sair | SupportAgent |
| `FAQ` | como funciona, o que é, dúvida | SupportAgent |
| `OUT_OF_SCOPE` | qualquer assunto não bancário | OrchestratorAgent |

## Classification Rules

1. **Prioritize explicit keywords** over context — a clear "fazer um pix" beats ambiguous context.
2. **Ambiguity → Clarify first** — if intent score < 0.7, ask one focused clarifying question before delegating.
3. **Complaint signals** — words like "problema", "errado", "frustrado", "inaceitável" → always route to SupportAgent with `is_complaint=True`.
4. **Out-of-scope** — respond politely: "Como assistente bancário do FinBank, só posso ajudar com serviços financeiros. Posso te ajudar com saldo, transferências, investimentos ou crédito?"
5. **Multiple intents** — address the primary intent first, acknowledge secondary intent at the end.

## Examples

- "Quero fazer um pix de 200 reais para o João" → `PIX_TRANSFER` → BankingAgent
- "Quanto está rendendo meu CDB?" → `PORTFOLIO` → InvestmentAgent  
- "Quero falar com meu gerente" → `MANAGER` → SupportAgent
- "Me dê uma receita de bolo" → `OUT_OF_SCOPE`
