---
name: context-retention
description: Maintains conversation context between turns so users don't need to repeat information. Session TTL is 30 minutes.
---

# Context Retention Skill

This skill preserves relevant information from previous turns of the conversation to provide a seamless banking experience.

## What to Retain

- **account_type** — if user specified "corrente" or "poupança", remember it for the session
- **last_pix_key** — the PIX key validated in the current flow
- **last_amount** — the last mentioned amount
- **last_contact** — the last contact referenced by the user
- **active_loan_id** / **active_financing_id** — the loan or financing under discussion
- **current_flow** — the multi-step flow in progress (e.g., `pix_confirmation`, `loan_simulation`)

## Retention Rules

1. **Carry forward** — if user says "agora manda mais 300" after a PIX flow, reuse the last pix_key.
2. **Ask before assuming** — if user has multiple accounts (corrente + poupança), always confirm which one.
3. **Context expiry** — after 30 minutes of inactivity (Redis TTL), clear session and greet freshly.
4. **Explicit override** — if user provides new values (different key, different amount), always use the latest.
5. **Flow abandonment** — if user switches topic mid-flow, save partial state; offer to resume if user returns within TTL.

## Multi-turn Example

```
Turn 1: User → "Qual meu saldo?"
         Agent saves: account_id, last_balance_check
Turn 2: User → "Me manda o extrato dessa conta"
         Agent reuses: account_id from Turn 1 (no need to ask again)
Turn 3: User → "Pode transferir 500 pro João?"
         Agent reuses: account_id; resolves "João" from contacts list
```
