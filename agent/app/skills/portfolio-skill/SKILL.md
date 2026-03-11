---
name: portfolio-skill
description: Presents and explains the client's investment portfolio clearly and educatively.
---

# Portfolio Skill

This skill presents the client's investment portfolio in a friendly, educational way.

## Portfolio Summary Format

```
📈 Sua Carteira de Investimentos
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total investido:  R$ 9.500,00
Valor atual:      R$ 9.936,05
Rendimento:      +R$ 436,05 (+4,59%)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CDB FinBank 90% CDI     R$ 5.243,75 ▲ +4,87%
LCI FinBank 88% CDI     R$ 3.118,50 ▲ +3,95%
Tesouro Selic 2027      R$ 1.573,80 ▲ +4,92%
```

## Redemption Flow

1. User requests redemption → check `liquidity` field
2. **Liquid products** (diaria, D+1): inform settlement date → confirm → call `redeem`
3. **Non-liquid products**: inform that redemption is only at maturity → offer alternatives
4. Always show: amount to redeem, settlement date, IR deduction (if applicable)

## IR Report Format

For declaração de IR, present a clean table:
- Product name | Gross return | IR | Net return
- Total line at the bottom
- Remind: LCI, LCA, Poupança are IR-exempt for individuals

## Educational Tone

- Explain jargon simply: "CDI é a taxa básica dos financiamentos entre bancos"
- Don't use jargon without explanation on first mention
- Celebrate milestones: "Seu investimento rendeu mais de R$ 400 este ano! 🎉"
