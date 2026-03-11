---
name: manager-communication
description: Facilitates communication between the client and their designated relationship manager.
---

# Manager Communication Skill

This skill handles all interactions between the client and their relationship manager.

## Manager Info Display

When user asks to contact manager → call `get_manager_info`, then present:
```
👤 Seu Gerente de Relacionamento
Nome:    Marcos Oliveira
Fone:    (11) 3456-7890
E-mail:  marcos.oliveira@finbank.com.br

O que você prefere?
1️⃣  Enviar uma mensagem agora
2️⃣  Agendar uma ligação
3️⃣  Continuar pelo chatbot
```

## Async Message Flow

1. Collect `message` and auto-detect `category` from content
   - Keywords: limit/crédito → "credit" | investimento → "investment" | outros → "geral"
2. Call `send_message_to_manager`
3. Confirm: "Mensagem enviada. Seu gerente responderá em até **1 dia útil**."

## Schedule Call Flow

1. Ask: preferred date (YYYY-MM-DD) and time (HH:MM), and subject
2. Call `schedule_manager_call`
3. Confirm with formatted response:
   - "📅 Ligação agendada com **{manager_name}** em **{date}** às **{time}**"
   - "Assunto: {subject}"
   - "Você receberá um lembrete por e-mail."

## Urgency Detection

Signals of urgency: "bloqueio indevido", "fraude", "urgente", "emergência"
→ Automatically elevate priority in any ticket or message
→ Mention our 24h central: 0800 700 1234
