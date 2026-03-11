---
name: investment-recommendation
description: Recommends investment products based on the client's profile, available amount and declared objectives.
---

# Investment Recommendation Skill

This skill guides clients to the best investment products based on their profile and goals.

## Discovery Flow (New Investor)

1. Call `get_investor_profile`
2. If profile not defined, run mini-questionnaire (3 questions):
   - "Você precisaria do dinheiro antes de 1 ano?" (liquidity)
   - "Como você se sente se perder 10% temporariamente?" (risk tolerance)
   - "Qual seu objetivo: reserva de emergência, aposentadoria ou crescimento?" (goal)
3. Map answers to profile: conservador / moderado / arrojado
4. Call `list_available_products` with the identified profile

## Recommendation Display

Present top 3 options:
```
🥇 CDB FinBank 100% CDI — Rendimento estimado: R$ 52,50 em 180 dias
   Liquidez diária • IR sobre rendimentos • A partir de R$ 1.000

🥈 LCI FinBank 88% CDI — Rendimento estimado: R$ 44,10 em 180 dias
   No vencimento • Isento de IR • A partir de R$ 3.000

🥉 Tesouro Selic 2027 — Rendimento estimado: R$ 49,80 em 180 dias
   Liquidez diária • Disponível a partir de R$ 30
```

## Simulation Before Investing

- Always call `simulate_investment` before presenting numbers
- Show: valor bruto, IR estimado, rendimento líquido, valor final
- Proactively compare 2-3 periods (ex: 180, 365 e 720 dias)

## Execution Flow (After Client Confirms)

1. Confirm: "Confirma aplicação de **R$ {amount}** em **{product_name}**?"
2. Call `invest`
3. Confirm success, show updated balance, inform maturity date
