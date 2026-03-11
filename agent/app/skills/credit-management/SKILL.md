---
name: credit-management
description: Manages tracking of active credit products, upcoming installments and portability requests.
---

# Credit Management Skill

This skill presents a complete view of the client's active debt and helps them manage it.

## Consolidated Debt View

1. Call `list_active_loans` and `list_active_financings` in parallel
2. Present:
```
📋 Suas Dívidas Consolidadas
━━━━━━━━━━━━━━━━━━━━━━━━━━━
Empréstimo Pessoal    Saldo: R$ 5.240,00   Próx. parcela: 01/04
Consignado            Saldo: R$ 4.010,00   Próx. parcela: 01/04
━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total devido:         R$ 9.250,00
```
3. Offer: "Deseja ver detalhes, antecipar alguma parcela ou verificar desconto de antecipação?"

## Loan Status Tracking

- When user asks about a loan request: call `get_loan_status`
- Map statuses to friendly language:
  - `analysis` → "Em análise — nossa equipe está avaliando seu perfil"
  - `pending_approval` → "Aguardando aprovação final"
  - `active` → "Contrato ativo"

## Portability Flow

1. User asks about bringing financing from another bank
2. Call `request_portability` with the target financing and source bank
3. Explain: "A portabilidade pode reduzir sua taxa. O processo leva até 5 dias úteis e não tem custo."
4. List documents typically required: contrato do financiamento original, extrato atualizado
