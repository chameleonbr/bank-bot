---
name: transaction-skill
description: Manages the complete flow for PIX and TED transactions including validation, confirmation, and receipt.
---

# Transaction Skill

This skill governs all money movement flows: PIX, TED, and scheduled transfers.

## PIX Simple Transfer Flow

1. User provides a PIX key → call `validate_pix_key`
2. Display: recipient name, CPF/CNPJ (masked), bank name
3. Ask: "Confirma o envio de **R$ {amount}** para **{name}**?"
4. On confirmation → call `pix_transfer`
5. Display: compact receipt (transaction ID, timestamp, amount)

## PIX Scheduled Flow

1. Collect: PIX key, amount, target date/time, recurrence option
2. Call `pix_schedule`
3. Confirm: "PIX de R$ {amount} agendado para {date} às {time}"

## TED Flow

1. Collect: bank (offer to call `list_banks` if unknown), agency, account number, CPF/CNPJ
2. Call `validate_ted_dest` → display holder name
3. Confirm amount and recipient
4. Call `ted_transfer`
5. Inform: TED é processada em até 30 minutos

## Limit Handling Rules

- **Nighttime limit** (22h–6h): if amount > nighttime limit, inform limit → offer: schedule for daytime, request limit increase, or split
- **Insufficient balance**: show current balance, suggest lower amount
- **Invalid PIX key**: apologize, ask for a new key — do NOT restart the entire flow

## Contact-based Transfer

- If user says "manda 300 pra Maria" → call `list_contacts` with search="Maria"
- If single match: confirm identity → proceed
- If multiple matches: list options, ask user to confirm which one

## Always

- Never execute a transfer without explicit user confirmation
- Show a formatted receipt after every successful transaction
