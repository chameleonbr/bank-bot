"""
Mock data definitions for the BancoBot AI backend.
All data is deterministic and consistent per account_id, as per the PRD.
"""

from datetime import datetime, timezone

# ── Accounts ────────────────────────────────────────────────────────────────

MOCK_ACCOUNTS = [
    {
        "id": "ACC001",
        "holder_name": "Ana Paula Souza",
        "cpf_cnpj": "123.456.789-01",
        "account_type": "PF",
        "investor_profile": "conservador",
        "credit_score": 720.0,
        "balance_checking": 4820.50,
        "balance_savings": 1250.00,
        "balance_salary": 0.0,
        "manager_name": "Marcos Oliveira",
        "manager_phone": "(11) 3456-7890",
        "manager_email": "marcos.oliveira@finbank.com.br",
        "branch_name": "Agência Paulista",
        "branch_address": "Av. Paulista, 1000 - Bela Vista, São Paulo - SP",
        "branch_phone": "(11) 3456-7800",
    },
    {
        "id": "ACC002",
        "holder_name": "Carlos Eduardo Lima",
        "cpf_cnpj": "234.567.890-12",
        "account_type": "PF",
        "investor_profile": "moderado",
        "credit_score": 650.0,
        "balance_checking": 12310.00,
        "balance_savings": 3400.00,
        "balance_salary": 0.0,
        "manager_name": "Fernanda Rocha",
        "manager_phone": "(11) 3456-7891",
        "manager_email": "fernanda.rocha@finbank.com.br",
        "branch_name": "Agência Moema",
        "branch_address": "Rua das Flores, 450 - Moema, São Paulo - SP",
        "branch_phone": "(11) 3456-7810",
    },
    {
        "id": "ACC003",
        "holder_name": "Fernanda Costa Ltda",
        "cpf_cnpj": "12.345.678/0001-90",
        "account_type": "PJ",
        "investor_profile": "arrojado",
        "credit_score": 810.0,
        "balance_checking": 87650.00,
        "balance_savings": 0.0,
        "balance_salary": 0.0,
        "manager_name": "Ricardo Mendes",
        "manager_phone": "(11) 3456-7892",
        "manager_email": "ricardo.mendes@finbank.com.br",
        "branch_name": "Agência Empresarial Centro",
        "branch_address": "Rua XV de Novembro, 200 - Centro, São Paulo - SP",
        "branch_phone": "(11) 3456-7820",
    },
    {
        "id": "ACC004",
        "holder_name": "Roberto Martins",
        "cpf_cnpj": "345.678.901-23",
        "account_type": "PF",
        "investor_profile": "arrojado",
        "credit_score": 580.0,
        "balance_checking": 2100.75,
        "balance_savings": 350.00,
        "balance_salary": 1800.00,
        "manager_name": "Patrícia Alves",
        "manager_phone": "(11) 3456-7893",
        "manager_email": "patricia.alves@finbank.com.br",
        "branch_name": "Agência Santo André",
        "branch_address": "Av. industrial, 600 - Santo André - SP",
        "branch_phone": "(11) 3456-7830",
    },
]

# ── Users (PIN default = 1234, hashed at seed time) ─────────────────────────

MOCK_USERS = [
    {"id": "USR001", "account_id": "ACC001", "pin": "1234"},
    {"id": "USR002", "account_id": "ACC002", "pin": "1234"},
    {"id": "USR003", "account_id": "ACC003", "pin": "1234"},
    {"id": "USR004", "account_id": "ACC004", "pin": "1234"},
]

# ── PIX Keys ─────────────────────────────────────────────────────────────────

MOCK_PIX_KEYS = [
    # ACC001 - Ana: CPF + email
    {"id": "PIX001", "account_id": "ACC001", "key_type": "cpf",   "key_value": "123.456.789-01", "status": "active"},
    {"id": "PIX002", "account_id": "ACC001", "key_type": "email",  "key_value": "ana.souza@email.com", "status": "active"},
    # ACC002 - Carlos: phone + random
    {"id": "PIX003", "account_id": "ACC002", "key_type": "phone",  "key_value": "+5511999998888", "status": "active"},
    {"id": "PIX004", "account_id": "ACC002", "key_type": "random", "key_value": "a1b2c3d4-e5f6-7890-abcd-ef1234567890", "status": "active"},
    # ACC003 - Fernanda (PJ): CNPJ + email
    {"id": "PIX005", "account_id": "ACC003", "key_type": "cnpj",  "key_value": "12.345.678/0001-90", "status": "active"},
    {"id": "PIX006", "account_id": "ACC003", "key_type": "email", "key_value": "financeiro@fernandacosta.com.br", "status": "active"},
    # ACC004 - Roberto: CPF + phone
    {"id": "PIX007", "account_id": "ACC004", "key_type": "cpf",   "key_value": "345.678.901-23", "status": "active"},
    {"id": "PIX008", "account_id": "ACC004", "key_type": "phone", "key_value": "+5511988887777", "status": "active"},
]

MOCK_PIX_LIMITS = [
    {"account_id": "ACC001", "limit_daytime": 5000.0,   "limit_nighttime": 1000.0},
    {"account_id": "ACC002", "limit_daytime": 10000.0,  "limit_nighttime": 1000.0},
    {"account_id": "ACC003", "limit_daytime": 100000.0, "limit_nighttime": 10000.0},
    {"account_id": "ACC004", "limit_daytime": 3000.0,   "limit_nighttime": 500.0},
]

# ── Contacts ─────────────────────────────────────────────────────────────────

MOCK_CONTACTS = [
    # ACC001
    {"id": "CON001", "account_id": "ACC001", "name": "João Silva",       "cpf_cnpj": "111.222.333-44", "bank": "Nubank",  "bank_code": "260", "agency": "0001", "account_number": "1234567-8",  "pix_key": "joao.silva@email.com",    "alias": "João"},
    {"id": "CON002", "account_id": "ACC001", "name": "Maria Fernandes",  "cpf_cnpj": "222.333.444-55", "bank": "Itaú",    "bank_code": "341", "agency": "1234", "account_number": "9876543-2",  "pix_key": "+5511977776666",           "alias": "Maria"},
    # ACC002
    {"id": "CON003", "account_id": "ACC002", "name": "Pedro Santos",     "cpf_cnpj": "333.444.555-66", "bank": "Bradesco","bank_code": "237", "agency": "5678", "account_number": "5432109-8",  "pix_key": "pedro.santos@email.com",  "alias": "Pedro"},
    {"id": "CON004", "account_id": "ACC002", "name": "Luciana Pereira",  "cpf_cnpj": "444.555.666-77", "bank": "Caixa",   "bank_code": "104", "agency": "9012", "account_number": "0123456-7",  "pix_key": "+5511966665555",           "alias": "Lu"},
    # ACC003
    {"id": "CON005", "account_id": "ACC003", "name": "Fornecedor Alpha", "cpf_cnpj": "98.765.432/0001-10", "bank": "BB",  "bank_code": "001", "agency": "3456", "account_number": "7890123-4",  "pix_key": "financeiro@alpha.com.br", "alias": "Alpha"},
    # ACC004
    {"id": "CON006", "account_id": "ACC004", "name": "Carla Rodrigues",  "cpf_cnpj": "555.666.777-88", "bank": "Inter",   "bank_code": "077", "agency": "0001", "account_number": "3456789-0",  "pix_key": "+5511955554444",           "alias": "Carla"},
]

# ── Investments ───────────────────────────────────────────────────────────────
# CDI fictício: 10.5% a.a.

MOCK_INVESTMENTS = [
    # ACC001 - Conservador: CDB + LCI + Tesouro Selic
    {"id": "INV001", "account_id": "ACC001", "product_type": "CDB",     "product_name": "CDB FinBank 90% CDI",  "amount_invested": 5000.00,  "current_value": 5243.75,  "rate": "90% CDI",   "start_date": "2024-09-01", "maturity_date": "2025-09-01", "liquidity": "no_vencimento", "status": "active"},
    {"id": "INV002", "account_id": "ACC001", "product_type": "LCI",     "product_name": "LCI FinBank 88% CDI",  "amount_invested": 3000.00,  "current_value": 3118.50,  "rate": "88% CDI",   "start_date": "2024-10-15", "maturity_date": "2025-04-15", "liquidity": "no_vencimento", "status": "active"},
    {"id": "INV003", "account_id": "ACC001", "product_type": "TESOURO", "product_name": "Tesouro Selic 2027",   "amount_invested": 1500.00,  "current_value": 1573.80,  "rate": "Selic+0%",  "start_date": "2024-07-10", "maturity_date": "2027-03-01", "liquidity": "diaria",        "status": "active"},
    # ACC002 - Moderado: CDB 110% CDI + Fundo Multimercado
    {"id": "INV004", "account_id": "ACC002", "product_type": "CDB",     "product_name": "CDB FinBank 110% CDI", "amount_invested": 20000.00, "current_value": 21450.00, "rate": "110% CDI",  "start_date": "2024-06-01", "maturity_date": "2025-06-01", "liquidity": "no_vencimento", "status": "active"},
    {"id": "INV005", "account_id": "ACC002", "product_type": "FUNDO",   "product_name": "Fundo Multimercado FinBank Plus", "amount_invested": 10000.00, "current_value": 10830.00, "rate": "CDI +2%",  "start_date": "2024-08-01", "maturity_date": None,         "liquidity": "D+30",          "status": "active"},
    # ACC003 - Arrojado: CDB 115% CDI + LCA + Fundo RF
    {"id": "INV006", "account_id": "ACC003", "product_type": "CDB",     "product_name": "CDB FinBank PRO 115% CDI", "amount_invested": 100000.00, "current_value": 107250.00, "rate": "115% CDI", "start_date": "2024-01-15", "maturity_date": "2026-01-15", "liquidity": "no_vencimento", "status": "active"},
    {"id": "INV007", "account_id": "ACC003", "product_type": "LCA",     "product_name": "LCA Agro FinBank 95% CDI","amount_invested": 50000.00, "current_value": 52375.00, "rate": "95% CDI",  "start_date": "2024-04-01", "maturity_date": "2025-04-01", "liquidity": "no_vencimento", "status": "active"},
    {"id": "INV008", "account_id": "ACC003", "product_type": "FUNDO",   "product_name": "Fundo Renda Fixa FinBank", "amount_invested": 30000.00, "current_value": 31200.00, "rate": "CDI+0.5%","start_date": "2024-05-20", "maturity_date": None,         "liquidity": "D+1",           "status": "active"},
    # ACC004 - Arrojado: Poupança + Tesouro IPCA+
    {"id": "INV009", "account_id": "ACC004", "product_type": "POUPANCA","product_name": "Poupança FinBank",      "amount_invested": 800.00,   "current_value": 828.40,   "rate": "70% Selic", "start_date": "2024-05-01", "maturity_date": None,         "liquidity": "diaria",        "status": "active"},
    {"id": "INV010", "account_id": "ACC004", "product_type": "TESOURO", "product_name": "Tesouro IPCA+ 2029",   "amount_invested": 2000.00,  "current_value": 2155.00,  "rate": "IPCA+5.9%","start_date": "2024-03-01", "maturity_date": "2029-05-15", "liquidity": "diaria",        "status": "active"},
]

# ── Loans ─────────────────────────────────────────────────────────────────────

MOCK_LOANS = [
    # ACC001 - Empréstimo Pessoal R$ 8.000 / 24x
    {
        "id": "LOA001", "account_id": "ACC001", "loan_type": "pessoal",
        "requested_amount": 8000.00, "outstanding_balance": 5240.00,
        "installment_amount": 391.80, "num_installments": 24, "paid_installments": 10,
        "monthly_rate": 0.0219, "start_date": "2024-04-01", "next_due_date": "2026-04-01",
        "status": "active",
    },
    # ACC003 - Crédito Empresarial R$ 200.000 / 60x
    {
        "id": "LOA002", "account_id": "ACC003", "loan_type": "empresarial",
        "requested_amount": 200000.00, "outstanding_balance": 164350.00,
        "installment_amount": 4520.00, "num_installments": 60, "paid_installments": 8,
        "monthly_rate": 0.0149, "start_date": "2024-07-01", "next_due_date": "2026-04-01",
        "status": "active",
    },
    # ACC004 - Empréstimo Pessoal R$ 3.000 / 12x
    {
        "id": "LOA003", "account_id": "ACC004", "loan_type": "pessoal",
        "requested_amount": 3000.00, "outstanding_balance": 1820.00,
        "installment_amount": 282.50, "num_installments": 12, "paid_installments": 5,
        "monthly_rate": 0.0249, "start_date": "2024-10-01", "next_due_date": "2026-04-01",
        "status": "active",
    },
    # ACC004 - Consignado R$ 5.000 / 36x
    {
        "id": "LOA004", "account_id": "ACC004", "loan_type": "consignado",
        "requested_amount": 5000.00, "outstanding_balance": 4010.00,
        "installment_amount": 163.90, "num_installments": 36, "paid_installments": 6,
        "monthly_rate": 0.0114, "start_date": "2024-09-01", "next_due_date": "2026-04-01",
        "status": "active",
    },
]

# ── Financings ────────────────────────────────────────────────────────────────

MOCK_FINANCINGS = [
    # ACC002 - Financiamento Veículo R$ 45.000 / 48x
    {
        "id": "FIN001", "account_id": "ACC002", "modality": "veiculo",
        "asset_value": 60000.00, "financed_amount": 45000.00, "entry_value": 15000.00,
        "outstanding_balance": 37250.00, "installment_amount": 1075.40,
        "num_installments": 48, "paid_installments": 7, "amortization_system": "PRICE",
        "monthly_rate": 0.0099, "start_date": "2024-08-01", "next_due_date": "2026-04-01",
        "status": "active",
    },
    # ACC003 - Financiamento Imóvel R$ 800.000 / 360x
    {
        "id": "FIN002", "account_id": "ACC003", "modality": "imovel",
        "asset_value": 1000000.00, "financed_amount": 800000.00, "entry_value": 200000.00,
        "outstanding_balance": 785000.00, "installment_amount": 6850.00,
        "num_installments": 360, "paid_installments": 3, "amortization_system": "SAC",
        "monthly_rate": 0.0075, "start_date": "2025-01-01", "next_due_date": "2026-04-01",
        "status": "active",
    },
]

# ── Scheduled Operations ──────────────────────────────────────────────────────

MOCK_SCHEDULED = [
    {"id": "SCH001", "account_id": "ACC001", "type": "pix",     "amount": 250.00,  "destination_name": "João Silva",       "destination_key": "joao.silva@email.com", "schedule_datetime": "2026-03-15 10:00:00", "recurrence": "monthly",  "status": "scheduled"},
    {"id": "SCH002", "account_id": "ACC001", "type": "payment", "amount": 380.00,  "destination_name": "Condomínio Alvorada", "destination_key": "",                  "schedule_datetime": "2026-03-20 08:00:00", "recurrence": "monthly",  "status": "scheduled"},
    {"id": "SCH003", "account_id": "ACC002", "type": "ted",     "amount": 1500.00, "destination_name": "Pedro Santos",     "destination_key": "",                    "schedule_datetime": "2026-03-12 14:00:00", "recurrence": "none",     "status": "scheduled"},
    {"id": "SCH004", "account_id": "ACC003", "type": "pix",     "amount": 8000.00, "destination_name": "Fornecedor Alpha", "destination_key": "financeiro@alpha.com.br", "schedule_datetime": "2026-03-11 09:00:00", "recurrence": "none", "status": "scheduled"},
]

# ── Support Tickets ───────────────────────────────────────────────────────────

MOCK_TICKETS = [
    {"id": "TIC001", "account_id": "ACC001", "category": "transferencia", "description": "PIX duplicado no dia 05/03",        "priority": "high",   "status": "in_progress", "created_at": "2026-03-05 10:30:00", "updated_at": "2026-03-06 09:00:00", "resolution": ""},
    {"id": "TIC002", "account_id": "ACC002", "category": "outros",         "description": "Atualização de dados cadastrais",  "priority": "normal", "status": "open",         "created_at": "2026-03-08 15:00:00", "updated_at": "2026-03-08 15:00:00", "resolution": ""},
    {"id": "TIC003", "account_id": "ACC003", "category": "credito",        "description": "Reavaliação de limite empresarial", "priority": "normal", "status": "resolved",     "created_at": "2026-02-20 11:00:00", "updated_at": "2026-02-28 16:00:00", "resolution": "Limite ajustado conforme análise cadastral."},
]

# ── Transactions (recent history) ─────────────────────────────────────────────

MOCK_TRANSACTIONS = [
    # ACC001
    {"id": "TRX001", "account_id": "ACC001", "date": "2026-03-09 14:32:00", "description": "PIX enviado - João Silva",          "amount": -200.00,  "category": "transferencia", "type": "pix",    "counterpart_name": "João Silva",       "counterpart_key": "joao.silva@email.com", "receipt_id": "RCP001", "status": "completed"},
    {"id": "TRX002", "account_id": "ACC001", "date": "2026-03-09 09:15:00", "description": "Supermercado Extra",                "amount": -187.40,  "category": "alimentacao",   "type": "debit",  "counterpart_name": "Supermercado Extra", "counterpart_key": "",                    "receipt_id": "",       "status": "completed"},
    {"id": "TRX003", "account_id": "ACC001", "date": "2026-03-08 18:00:00", "description": "Salário FinCorp",                   "amount": 5200.00,  "category": "salario",       "type": "credit", "counterpart_name": "FinCorp S.A.",      "counterpart_key": "",                    "receipt_id": "",       "status": "completed"},
    {"id": "TRX004", "account_id": "ACC001", "date": "2026-03-07 12:45:00", "description": "iFood",                             "amount": -45.90,   "category": "alimentacao",   "type": "debit",  "counterpart_name": "iFood",            "counterpart_key": "",                    "receipt_id": "",       "status": "completed"},
    {"id": "TRX005", "account_id": "ACC001", "date": "2026-03-05 10:00:00", "description": "PIX enviado (duplicado) - Maria",   "amount": -350.00,  "category": "transferencia", "type": "pix",    "counterpart_name": "Maria Fernandes",   "counterpart_key": "+5511977776666",      "receipt_id": "RCP002", "status": "completed"},
    {"id": "TRX006", "account_id": "ACC001", "date": "2026-03-04 16:20:00", "description": "Farmácia São Paulo",                "amount": -62.30,   "category": "saude",         "type": "debit",  "counterpart_name": "Farmácia São Paulo","counterpart_key": "",                    "receipt_id": "",       "status": "completed"},
    {"id": "TRX007", "account_id": "ACC001", "date": "2026-03-03 11:00:00", "description": "Conta de luz",                      "amount": -145.00,  "category": "moradia",       "type": "payment","counterpart_name": "Enel SP",           "counterpart_key": "",                    "receipt_id": "",       "status": "completed"},
    {"id": "TRX008", "account_id": "ACC001", "date": "2026-03-01 08:00:00", "description": "Transporte - Uber",                 "amount": -22.50,   "category": "transporte",    "type": "debit",  "counterpart_name": "Uber",             "counterpart_key": "",                    "receipt_id": "",       "status": "completed"},
    # ACC002
    {"id": "TRX009", "account_id": "ACC002", "date": "2026-03-09 16:00:00", "description": "TED enviado - Pedro Santos",        "amount": -1500.00, "category": "transferencia", "type": "ted",    "counterpart_name": "Pedro Santos",     "counterpart_key": "",                    "receipt_id": "RCP003", "status": "completed"},
    {"id": "TRX010", "account_id": "ACC002", "date": "2026-03-08 20:00:00", "description": "Restaurante Fogo de Chão",          "amount": -280.00,  "category": "alimentacao",   "type": "debit",  "counterpart_name": "Fogo de Chão",     "counterpart_key": "",                    "receipt_id": "",       "status": "completed"},
    {"id": "TRX011", "account_id": "ACC002", "date": "2026-03-07 09:00:00", "description": "Salário TechStart",                 "amount": 8500.00,  "category": "salario",       "type": "credit", "counterpart_name": "TechStart Ltda",   "counterpart_key": "",                    "receipt_id": "",       "status": "completed"},
    {"id": "TRX012", "account_id": "ACC002", "date": "2026-03-06 14:30:00", "description": "Amazon BR",                         "amount": -319.90,  "category": "compras",       "type": "debit",  "counterpart_name": "Amazon",           "counterpart_key": "",                    "receipt_id": "",       "status": "completed"},
    # ACC003
    {"id": "TRX013", "account_id": "ACC003", "date": "2026-03-09 10:00:00", "description": "Recebimento cliente Beta",          "amount": 25000.00, "category": "receita",       "type": "ted",    "counterpart_name": "Beta Corp",        "counterpart_key": "",                    "receipt_id": "RCP004", "status": "completed"},
    {"id": "TRX014", "account_id": "ACC003", "date": "2026-03-08 11:00:00", "description": "Pagamento fornecedor Alpha",        "amount": -8000.00, "category": "fornecedor",    "type": "pix",    "counterpart_name": "Fornecedor Alpha", "counterpart_key": "financeiro@alpha.com.br", "receipt_id": "RCP005", "status": "completed"},
    {"id": "TRX015", "account_id": "ACC003", "date": "2026-03-05 09:00:00", "description": "Folha de pagamento colaboradores",  "amount": -32000.00,"category": "salario",       "type": "ted",    "counterpart_name": "Múltiplos",        "counterpart_key": "",                    "receipt_id": "",       "status": "completed"},
    # ACC004
    {"id": "TRX016", "account_id": "ACC004", "date": "2026-03-09 12:00:00", "description": "PIX recebido - Carla Rodrigues",   "amount": 500.00,   "category": "transferencia", "type": "pix",    "counterpart_name": "Carla Rodrigues",  "counterpart_key": "+5511955554444",      "receipt_id": "RCP006", "status": "completed"},
    {"id": "TRX017", "account_id": "ACC004", "date": "2026-03-08 18:30:00", "description": "Supermercado Dia",                  "amount": -98.60,   "category": "alimentacao",   "type": "debit",  "counterpart_name": "Supermercado Dia", "counterpart_key": "",                    "receipt_id": "",       "status": "completed"},
    {"id": "TRX018", "account_id": "ACC004", "date": "2026-03-05 08:00:00", "description": "Salário LogCom",                    "amount": 3200.00,  "category": "salario",       "type": "credit", "counterpart_name": "LogCom S.A.",      "counterpart_key": "",                    "receipt_id": "",       "status": "completed"},
    {"id": "TRX019", "account_id": "ACC004", "date": "2026-03-04 19:00:00", "description": "Netflix",                           "amount": -44.90,   "category": "lazer",         "type": "debit",  "counterpart_name": "Netflix",          "counterpart_key": "",                    "receipt_id": "",       "status": "completed"},
    {"id": "TRX020", "account_id": "ACC004", "date": "2026-03-01 07:30:00", "description": "Gasolina Shell",                    "amount": -210.00,  "category": "transporte",    "type": "debit",  "counterpart_name": "Shell",            "counterpart_key": "",                    "receipt_id": "",       "status": "completed"},
]

# ── FAQ Knowledge Base ────────────────────────────────────────────────────────

FAQ_DATA = [
    {"category": "pix",        "query_keywords": ["pix", "chave", "transferência instantânea"], "answer": "O PIX está disponível 24h/dia, 7 dias por semana. Você pode transferir usando chaves CPF, CNPJ, e-mail, celular ou chave aleatória. O limite noturno (22h–6h) é de R$ 1.000 por padrão."},
    {"category": "ted",        "query_keywords": ["ted", "transferência bancária"],             "answer": "A TED é processada em dias úteis no horário de 6h às 17h, com crédito em até 30 minutos. Para TED agendada fora do horário, o envio ocorre no próximo dia útil."},
    {"category": "extrato",    "query_keywords": ["extrato", "lançamento", "movimentação"],     "answer": "Você pode consultar o extrato dos últimos 90 dias. Filtre por período, categoria ou valor. Para extratos mais antigos, solicite ao gerente ou abra um chamado."},
    {"category": "investimento","query_keywords": ["investimento", "CDB", "rendimento"],        "answer": "Nossos produtos de investimento incluem CDB, LCI, LCA, Tesouro Direto e Fundos. Cada produto tem características de prazo, liquidez e risco diferentes. Consulte seu perfil de investidor para recomendações personalizadas."},
    {"category": "emprestimo", "query_keywords": ["empréstimo", "crédito", "parcela"],          "answer": "Oferecemos empréstimo pessoal (a partir de 1,99% a.m.), consignado (a partir de 1,14% a.m.) e crédito empresarial. Simule pelo chat antes de solicitar."},
    {"category": "gerente",    "query_keywords": ["gerente", "falar", "atendimento"],            "answer": "Seu gerente de relacionamento está disponível por mensagem (retorno em 1 dia útil) ou por ligação agendada em horários previamente combinados."},
    {"category": "seguranca",  "query_keywords": ["senha", "bloqueio", "fraude", "segurança"],  "answer": "Em caso de suspeita de fraude, bloqueie sua conta imediatamente pelo app ou ligue para nossa central 24h: 0800 700 1234. Nunca compartilhe sua senha ou token com ninguém."},
]

# ── Available Investment Products ─────────────────────────────────────────────

AVAILABLE_PRODUCTS = [
    {"id": "PROD001", "product_type": "CDB",     "name": "CDB FinBank 90% CDI",        "rate": "90% CDI",   "min_amount": 500.0,   "period_days": 365,  "liquidity": "no_vencimento", "risk_profile": "conservador", "is_ir_exempt": False},
    {"id": "PROD002", "product_type": "CDB",     "name": "CDB FinBank 100% CDI",       "rate": "100% CDI",  "min_amount": 1000.0,  "period_days": 180,  "liquidity": "diaria",        "risk_profile": "conservador", "is_ir_exempt": False},
    {"id": "PROD003", "product_type": "CDB",     "name": "CDB FinBank PRO 110% CDI",   "rate": "110% CDI",  "min_amount": 5000.0,  "period_days": 365,  "liquidity": "no_vencimento", "risk_profile": "moderado",    "is_ir_exempt": False},
    {"id": "PROD004", "product_type": "CDB",     "name": "CDB FinBank PRO 115% CDI",   "rate": "115% CDI",  "min_amount": 10000.0, "period_days": 720,  "liquidity": "no_vencimento", "risk_profile": "arrojado",    "is_ir_exempt": False},
    {"id": "PROD005", "product_type": "LCI",     "name": "LCI FinBank 85% CDI",        "rate": "85% CDI",   "min_amount": 1000.0,  "period_days": 90,   "liquidity": "no_vencimento", "risk_profile": "conservador", "is_ir_exempt": True},
    {"id": "PROD006", "product_type": "LCI",     "name": "LCI FinBank 88% CDI",        "rate": "88% CDI",   "min_amount": 3000.0,  "period_days": 180,  "liquidity": "no_vencimento", "risk_profile": "conservador", "is_ir_exempt": True},
    {"id": "PROD007", "product_type": "LCA",     "name": "LCA Agro FinBank 95% CDI",   "rate": "95% CDI",   "min_amount": 5000.0,  "period_days": 365,  "liquidity": "no_vencimento", "risk_profile": "moderado",    "is_ir_exempt": True},
    {"id": "PROD008", "product_type": "TESOURO", "name": "Tesouro Selic 2027",          "rate": "Selic+0%",  "min_amount": 30.0,    "period_days": 365,  "liquidity": "diaria",        "risk_profile": "conservador", "is_ir_exempt": False},
    {"id": "PROD009", "product_type": "TESOURO", "name": "Tesouro IPCA+ 2029",          "rate": "IPCA+5.9%", "min_amount": 30.0,    "period_days": 1095, "liquidity": "diaria",        "risk_profile": "moderado",    "is_ir_exempt": False},
    {"id": "PROD010", "product_type": "FUNDO",   "name": "Fundo Renda Fixa FinBank",   "rate": "CDI+0.5%",  "min_amount": 100.0,   "period_days": 1,    "liquidity": "D+1",           "risk_profile": "conservador", "is_ir_exempt": False},
    {"id": "PROD011", "product_type": "FUNDO",   "name": "Fundo Multimercado FinBank Plus","rate": "CDI+2%", "min_amount": 1000.0,  "period_days": 30,   "liquidity": "D+30",          "risk_profile": "moderado",    "is_ir_exempt": False},
    {"id": "PROD012", "product_type": "FUNDO",   "name": "Fundo Ações FinBank",        "rate": "IBOV",      "min_amount": 500.0,   "period_days": 1,    "liquidity": "D+3",           "risk_profile": "arrojado",    "is_ir_exempt": False},
]

# ── Banks (partial list for TED) ──────────────────────────────────────────────

MOCK_BANKS = [
    {"code": "001", "ispb": "00000000", "name": "Banco do Brasil S.A.",                 "short_name": "BB"},
    {"code": "033", "ispb": "90400888", "name": "Banco Santander Brasil S.A.",          "short_name": "Santander"},
    {"code": "077", "ispb": "00416968", "name": "Banco Inter S.A.",                     "short_name": "Inter"},
    {"code": "104", "ispb": "00360305", "name": "Caixa Econômica Federal",              "short_name": "Caixa"},
    {"code": "237", "ispb": "60746948", "name": "Banco Bradesco S.A.",                  "short_name": "Bradesco"},
    {"code": "260", "ispb": "18236120", "name": "Nu Pagamentos S.A.",                   "short_name": "Nubank"},
    {"code": "341", "ispb": "60701190", "name": "Itaú Unibanco S.A.",                   "short_name": "Itaú"},
    {"code": "422", "ispb": "58160789", "name": "Banco Safra S.A.",                     "short_name": "Safra"},
    {"code": "623", "ispb": "92894922", "name": "Banco PAN S.A.",                       "short_name": "PAN"},
    {"code": "735", "ispb": "00000208", "name": "Banco Neon S.A.",                      "short_name": "Neon"},
    {"code": "756", "ispb": "02038232", "name": "Banco Cooperativo do Brasil S.A.",     "short_name": "Sicoob"},
]
