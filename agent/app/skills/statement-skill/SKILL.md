---
name: statement-skill
description: Organizes and presents account balances and transaction statements in a clear, contextualized way.
---

# Statement Skill

This skill formats and presents financial data in a user-friendly way.

## Balance Display Format

```
💰 Saldo da Conta Corrente: R$ 4.820,50
💵 Conta Poupança: R$ 1.250,00
📊 Total consolidado: R$ 6.070,50
🕐 Atualizado em: 10/03/2026 às 09:17
```

## Statement Display Rules

1. **Group by category** when showing monthly statements (Alimentação, Transporte, Lazer, etc.)
2. **Highlight debits in red context**, credits in green context
3. **Pagination**: show 20 items per page; offer "ver mais" or "enviar por e-mail"
4. **Last debit query**: filter `amount < 0`, order by date desc, limit 5
5. **Monthly summary**: show total entradas, total saídas, and net balance

## Scheduled Operations Display

- Sort chronologically
- Show type icon: PIX 💊, TED 🏦, Pagamento 📄
- For recurring: show "mensal • próxima em {date}"

## Filtering by Category

- Understand natural language: "gastos com alimentação" → category=alimentacao
- Present total for the category + comparison to previous month if available

## Language Rules

- Format all amounts in BRL: `R$ 1.234,56`
- Format dates in PT-BR: `dd/MM/yyyy`
- Use friendly labels: "hoje", "ontem", "há 3 dias" for recent dates
