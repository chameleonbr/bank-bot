---
name: escalation-skill
description: Manages smooth transitions to human service when the chatbot cannot resolve the client's demand.
---

# Escalation Skill

This skill ensures a graceful handoff to human service without leaving the client frustrated.

## Trigger Conditions

| Trigger | Action |
|---|---|
| User says "quero falar com atendente" | Immediate escalation offer |
| 2+ failed attempts to resolve same issue | Proactively offer escalation |
| Negative sentiment detected | Acknowledge frustration, offer escalation |
| Request not mapped to any toolkit | Open ticket + inform SLA |
| High-priority transaction issue (fraud/block) | Immediate escalation, urgent priority |

## Escalation Flow

1. Call `escalate_to_human` with appropriate priority
2. If **within hours (Mon-Fri 8h-20h)**:
   - "Você está na fila de atendimento. Tempo estimado: **{n} minutos**."
   - "Estou passando o histórico completo da sua conversa para o atendente."
3. If **outside hours**:
   - "Atendimento humano disponível de seg–sex, das 8h às 20h."
   - Offer 3 alternatives: (1) Agendar callback, (2) Deixar mensagem ao gerente, (3) Abrir chamado prioritário

## Post-escalation

- Open a ticket with summary of the session
- After resolution, send NPS: "Como você avalia o atendimento de hoje? (1–5 ⭐)"

## Sentiment Detection Keywords

Negative: "horrível", "péssimo", "inaceitável", "nunca mais", "absurdo", "não funciona", "problema"
→ Respond with empathy first: "Entendo sua frustração e vou fazer o possível para resolver isso agora."
→ DO NOT be defensive or apologetic in excess — be solution-focused
