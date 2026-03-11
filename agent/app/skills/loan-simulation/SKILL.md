---
name: loan-simulation
description: Conducts transparent and comparative loan and financing simulations.
---

# Loan Simulation Skill

This skill guides clients through credit and financing simulations in a clear and comparative way.

## Personal Loan Simulation Flow

1. Collect: desired amount + number of installments (or ask if not given)
2. Call `simulate_loan` with `loan_type=pessoal`
3. Present:
```
💳 Simulação de Empréstimo Pessoal
Valor solicitado:    R$ 5.000,00
Parcelas:            12x de R$ 462,00
Taxa mensal:         1,99% a.m.
Taxa anual:          26,74% a.a.
CET:                 2,03% a.m.
Total a pagar:       R$ 5.544,00
```
4. Proactively offer comparison table for 12, 18 and 24 installments

## Financing Simulation Flow

1. Collect: asset value, entry value, period in months, modality (imovel/veiculo/rural)
2. Call `simulate_financing` for both SAC and PRICE systems
3. Show side-by-side comparison:
   - First installment, last installment, total amount paid
4. Recommend SAC for those paying off faster; PRICE for stable monthly budget

## Anticipation Flow

1. Call `list_active_loans` → let user pick the loan
2. Collect number of installments to anticipate
3. Call `anticipate_installments` → show discount and new balance
4. Ask: "Deseja confirmar a antecipação de {n} parcelas com desconto de R$ {discount}?"

## Score Warning

If score < 620 (Baixo):
- Inform honestly: "No momento, seu score não está adequado para este produto"
- Suggest: smaller amount, shorter term, or credit building tips
- Never leave client without a constructive next step
