# 🏦 BancoBot AI
## Product Requirements Document
**Chatbot Bancário Inteligente com Agno Framework**

| Campo | Valor |
|---|---|
| Versão | 1.0 |
| Data | Março / 2025 |
| Status | Draft — Para Revisão |
| Framework | Agno (agno.com) |
| Classificação | Confidencial |

---

# 1. Visão Geral do Produto

## 1.1 Resumo Executivo

O BancoBot AI é um assistente virtual bancário desenvolvido para o banco fictício **FinBank S.A.**, com o objetivo de oferecer aos clientes uma experiência de atendimento digital completa, segura e eficiente via chat. O sistema será construído sobre o **Agno Framework (agno.com)**, aproveitando sua arquitetura de agentes de IA com suporte a tools, toolkits e agent skills.

O chatbot centraliza as principais operações bancárias do dia a dia, reduzindo a necessidade de atendimento humano para demandas rotineiras e oferecendo disponibilidade 24/7.

## 1.2 Objetivos de Negócio

- Reduzir em até **60%** o volume de chamadas no call center para operações rotineiras
- Oferecer atendimento disponível **24 horas por dia, 7 dias por semana**
- Aumentar o índice de satisfação NPS para operações digitais (meta: > 75)
- Diminuir o tempo médio de resolução de demandas bancárias de 8 min para **< 2 min**
- Aumentar a adoção de produtos de investimento e crédito via canal digital

## 1.3 Público-Alvo

| Segmento | Perfil | Necessidade Principal |
|---|---|---|
| Pessoa Física | 18–35 anos, digitalmente ativo | Agilidade em transações (PIX, extrato) |
| Pessoa Física | 36–60 anos, cliente de longa data | Suporte e esclarecimento de dúvidas |
| Pessoa Jurídica | MEI e PME | Financiamentos, TEDs e relatórios |
| Pessoa Jurídica | Grandes empresas | Investimentos e atendimento prioritário |

---

# 2. Arquitetura Técnica — Agno Framework

## 2.1 Visão Geral da Arquitetura

O BancoBot AI é estruturado como um **sistema multi-agente** utilizando o Agno Framework, onde cada domínio funcional é tratado por um agente especializado, orquestrado por um agente central (Orchestrator Agent). Toda comunicação entre agentes é assíncrona e orientada por mensagens estruturadas.

**Componentes Principais:**

- **Orchestrator Agent** — Agente central que interpreta a intenção do usuário e delega ao agente especializado correto
- **Domain Agents** — Agentes especializados por domínio: Banking, Investments, Credit, Support
- **Toolkits** — Coleções de tools agrupadas por domínio funcional (ex: BankingToolkit, PIXToolkit)
- **Agent Skills** — Habilidades declarativas registradas em cada agente para guiar comportamentos
- **Memory Store** — Contexto de sessão e histórico de interações persistido para continuidade
- **Mock Data Layer** — Camada de dados simulados para validação sem sistemas reais

## 2.2 Fluxo de Processamento

1. Cliente envia mensagem no canal (app mobile, internet banking ou WhatsApp)
2. Orchestrator Agent recebe a mensagem e executa análise de intenção (Intent Classification Skill)
3. Orchestrator delega a tarefa ao Domain Agent correspondente via Agno message routing
4. Domain Agent ativa as tools necessárias do Toolkit registrado
5. Tools acessam a Mock Data Layer e retornam dados estruturados
6. Domain Agent compõe a resposta utilizando as Agent Skills de formatação e personalização
7. Resposta é entregue ao cliente com contexto, clareza e ações sugeridas

## 2.3 Estrutura de Agentes

| Agente | Responsabilidade | Toolkits Registrados | Skills Ativas |
|---|---|---|---|
| `OrchestratorAgent` | Roteamento e intent classification | RouterToolkit | IntentSkill, ContextSkill |
| `BankingAgent` | Transações, extrato, saldo, contatos | BankingToolkit, PIXToolkit, TEDToolkit | TransactionSkill, StatementSkill |
| `InvestmentAgent` | Investimentos e carteira | InvestmentToolkit | PortfolioSkill, RecommendationSkill |
| `CreditAgent` | Empréstimos e financiamentos | CreditToolkit, LoanToolkit | CreditSkill, SimulationSkill |
| `SupportAgent` | Gerente, dúvidas, escalação | SupportToolkit | EscalationSkill, FAQSkill |

---

# 3. Toolkits e Tools

O Agno Framework organiza ferramentas em **Toolkits** — grupos coesos de Tools que compartilham contexto e configuração. Abaixo estão definidos todos os Toolkits e suas Tools correspondentes para o BancoBot AI.

## 3.1 BankingToolkit

Toolkit central para operações de conta corrente e poupança.

| Nome da Tool | Descrição | Parâmetros Principais |
|---|---|---|
| `get_balance` | Retorna saldo disponível, bloqueado e total da conta | `account_id`, `account_type` |
| `get_statement` | Busca extrato por período com filtros | `account_id`, `start_date`, `end_date`, `category`, `limit` |
| `get_account_info` | Retorna dados cadastrais e informações da conta | `account_id` |
| `list_contacts` | Lista contatos salvos para transferência | `account_id`, `search_term` |
| `add_contact` | Adiciona novo contato à agenda bancária | `name`, `cpf_cnpj`, `bank`, `agency`, `account` |
| `remove_contact` | Remove contato da agenda bancária | `account_id`, `contact_id` |
| `get_scheduled` | Lista transferências e pagamentos agendados | `account_id`, `date_from`, `date_to` |
| `cancel_scheduled` | Cancela uma operação agendada | `account_id`, `schedule_id` |

## 3.2 PIXToolkit

Toolkit dedicado às operações PIX — pagamentos instantâneos regulamentados pelo Banco Central do Brasil.

| Nome da Tool | Descrição | Parâmetros Principais |
|---|---|---|
| `pix_transfer` | Executa transferência PIX imediata | `origin_account`, `pix_key`, `amount`, `description` |
| `pix_schedule` | Agenda um PIX para data/hora futura | `origin_account`, `pix_key`, `amount`, `schedule_datetime` |
| `get_pix_keys` | Lista chaves PIX registradas na conta | `account_id` |
| `register_pix_key` | Registra nova chave PIX (CPF, CNPJ, email, celular, aleatória) | `account_id`, `key_type`, `key_value` |
| `delete_pix_key` | Remove chave PIX registrada | `account_id`, `pix_key_id` |
| `validate_pix_key` | Valida e retorna dados do recebedor pela chave PIX | `pix_key` |
| `get_pix_limits` | Retorna limites de transferência PIX (diurno e noturno) | `account_id` |
| `update_pix_limit` | Solicita alteração de limite PIX (sujeito a carência) | `account_id`, `new_limit_daytime`, `new_limit_nighttime` |
| `get_pix_receipt` | Gera comprovante de transação PIX em formato estruturado | `transaction_id` |

## 3.3 TEDToolkit

Toolkit para transferências TED (Transferência Eletrônica Disponível) entre diferentes instituições financeiras.

| Nome da Tool | Descrição | Parâmetros Principais |
|---|---|---|
| `ted_transfer` | Executa TED para conta em outro banco | `origin_account`, `bank_code`, `agency`, `account`, `cpf_cnpj`, `amount` |
| `ted_schedule` | Agenda TED para dia útil futuro | `origin_account`, `dest_data`, `amount`, `schedule_date` |
| `validate_ted_dest` | Valida dados bancários do destinatário TED | `bank_code`, `agency`, `account`, `cpf_cnpj` |
| `get_ted_receipt` | Gera comprovante de TED em formato estruturado | `transaction_id` |
| `get_ted_limits` | Retorna limites de TED por período | `account_id` |
| `list_banks` | Lista bancos disponíveis com código ISPB | `search_term` |

## 3.4 InvestmentToolkit

Toolkit para visualização e gestão da carteira de investimentos.

| Nome da Tool | Descrição | Parâmetros Principais |
|---|---|---|
| `get_portfolio` | Retorna posição completa da carteira de investimentos | `account_id` |
| `get_product_info` | Detalha um produto de investimento (CDB, LCI, etc.) | `product_id` |
| `list_available_products` | Lista produtos de investimento disponíveis para o perfil | `account_id`, `risk_profile`, `min_amount` |
| `simulate_investment` | Simula rentabilidade de um investimento | `product_id`, `amount`, `period_days` |
| `invest` | Executa aplicação em produto de investimento | `account_id`, `product_id`, `amount` |
| `redeem` | Solicita resgate de investimento (total ou parcial) | `account_id`, `investment_id`, `amount` |
| `get_investor_profile` | Retorna perfil de investidor (conservador/moderado/arrojado) | `account_id` |
| `get_income_report` | Gera relatório de rendimentos por período | `account_id`, `year` |

## 3.5 CreditToolkit

Toolkit para produtos de crédito pessoal, consignado e empréstimos.

| Nome da Tool | Descrição | Parâmetros Principais |
|---|---|---|
| `get_credit_limit` | Retorna limite de crédito disponível e utilizado | `account_id` |
| `simulate_loan` | Simula empréstimo pessoal (parcelas, juros, CET) | `account_id`, `amount`, `num_installments`, `loan_type` |
| `request_loan` | Inicia solicitação de empréstimo pessoal | `account_id`, `amount`, `num_installments`, `purpose` |
| `get_loan_status` | Verifica status de solicitação em andamento | `account_id`, `loan_request_id` |
| `list_active_loans` | Lista empréstimos ativos com saldo devedor | `account_id` |
| `get_loan_statement` | Histórico de pagamentos de um empréstimo | `loan_id` |
| `anticipate_installments` | Simula e solicita antecipação de parcelas | `loan_id`, `num_installments_to_anticipate` |
| `get_credit_score` | Retorna score de crédito interno do cliente | `account_id` |

## 3.6 LoanToolkit (Financiamentos)

Toolkit específico para financiamentos de longo prazo: imóvel, veículo e crédito rural.

| Nome da Tool | Descrição | Parâmetros Principais |
|---|---|---|
| `simulate_financing` | Simula financiamento com tabelas SAC, Price ou Misto | `amount`, `entry_value`, `period_months`, `modality`, `system` |
| `list_financing_lines` | Lista linhas de financiamento disponíveis | `modality` |
| `request_financing` | Inicia processo de solicitação de financiamento | `account_id`, `modality`, `property_value`, `entry_value`, `period_months` |
| `get_financing_status` | Acompanha estágio do processo de financiamento | `account_id`, `financing_id` |
| `list_active_financings` | Lista financiamentos ativos do cliente | `account_id` |
| `get_financing_statement` | Extrato detalhado de financiamento ativo | `financing_id` |
| `get_next_installment` | Informa data e valor da próxima parcela | `financing_id` |
| `request_portability` | Inicia pedido de portabilidade de financiamento | `financing_id`, `target_bank_code` |

## 3.7 SupportToolkit

Toolkit para suporte ao cliente, escalonamento e comunicação com gerentes.

| Nome da Tool | Descrição | Parâmetros Principais |
|---|---|---|
| `open_ticket` | Abre chamado de suporte categorizado | `account_id`, `category`, `description`, `priority` |
| `get_ticket_status` | Consulta status de chamado aberto | `ticket_id` |
| `list_open_tickets` | Lista todos os chamados abertos do cliente | `account_id` |
| `schedule_manager_call` | Agenda ligação com gerente de relacionamento | `account_id`, `preferred_date`, `preferred_time`, `subject` |
| `send_message_to_manager` | Envia mensagem assíncrona ao gerente | `account_id`, `message`, `category` |
| `get_manager_info` | Retorna dados de contato do gerente responsável | `account_id` |
| `escalate_to_human` | Escala conversa para atendente humano em tempo real | `session_id`, `reason`, `priority` |
| `get_faq` | Busca resposta em base de conhecimento/FAQ | `query`, `category` |
| `get_branch_info` | Informa agência responsável e horários | `account_id` |

---

# 4. Agent Skills

As Agent Skills no Agno Framework são **capacidades declarativas** registradas nos agentes que definem comportamentos, regras de negócio e fluxos de interação. Cada skill é ativada contextualmente conforme a situação detectada pelo agente.

## 4.1 Skills do OrchestratorAgent

### `IntentClassificationSkill`

Responsável por identificar a intenção do usuário e mapear para o agente e toolkit corretos.

**Cenários de Uso:**

- **Cenário 1 — PIX direto:** Usuário escreve _"quero fazer um pix de 200 reais"_ → classifica como `PIX_TRANSFER`, delega ao `BankingAgent`
- **Cenário 2 — Consulta de saldo filtrado:** Usuário escreve _"quanto tenho na poupança?"_ → classifica como `BALANCE_INQUIRY`, filtra `account_type=savings`
- **Cenário 3 — Intenção ambígua:** Mensagem _"quero investir"_ → ativa `ClarificationSkill` para coletar valor e prazo antes de delegar
- **Cenário 4 — Solicitação de suporte:** Usuário menciona _"gerente"_ ou _"reclamação"_ → prioriza `SupportAgent` com flag `is_complaint=true`
- **Cenário 5 — Fora do escopo:** Mensagem não bancária → ativa `OutOfScopeSkill` e redireciona educadamente

---

### `ContextRetentionSkill`

Mantém o contexto da conversa entre turnos para evitar que o usuário precise repetir informações.

**Cenários de Uso:**

- **Cenário 1 — Continuidade de conta:** Usuário pergunta saldo, depois diz _"pode transferir 500 para o João"_ → skill usa a conta identificada no turno anterior
- **Cenário 2 — Preservação de parâmetros:** Simulação de empréstimo em andamento → skill preserva valor e prazo digitados durante a etapa de confirmação
- **Cenário 3 — Retomada de sessão:** Usuário abandona fluxo e retorna em 5 min → skill restaura estado se sessão ainda ativa (TTL: 30 min)
- **Cenário 4 — Múltiplas contas:** Cliente com conta corrente e poupança → skill solicita confirmação e salva preferência durante a sessão

---

## 4.2 Skills do BankingAgent

### `TransactionSkill`

Gerencia o fluxo completo de transações PIX e TED, incluindo validação, confirmação e emissão de comprovante.

**Cenários de Uso:**

- **Cenário PIX Simples:** Cliente informa chave PIX e valor → skill valida chave (`validate_pix_key`) → exibe nome do recebedor e valor → solicita confirmação → executa `pix_transfer` → exibe comprovante
- **Cenário PIX Agendado:** Cliente quer pagar conta amanhã → skill coleta data/hora → chama `pix_schedule` → confirma agendamento com ID de referência
- **Cenário TED:** Cliente informa agência, conta e banco → skill chama `validate_ted_dest` → confirma dados → executa `ted_transfer`
- **Cenário de Limite Excedido:** Valor supera limite noturno (22h–6h) → skill informa limite vigente → oferece opções: agendar para horário diurno, solicitar aumento de limite ou fracionar o valor
- **Cenário de Contato Favorito:** _"Manda 150 reais pra Maria"_ → skill busca em `list_contacts` → confirma identidade → confirma transferência
- **Cenário de Chave Inválida:** Chave PIX inexistente → skill explica o erro e solicita nova chave sem reiniciar o fluxo

---

### `StatementSkill`

Organiza e apresenta extratos e saldos de forma contextualizada e legível.

**Cenários de Uso:**

- **Cenário Saldo:** _"Qual meu saldo?"_ → skill chama `get_balance` → apresenta saldo disponível destacado, saldo bloqueado em separado e data/hora de atualização
- **Cenário Extrato do Dia:** _"Meu extrato de hoje"_ → skill chama `get_statement` com `start_date` e `end_date = hoje` → agrupa por categoria e exibe resumo
- **Cenário Filtrado por Categoria:** _"Gastos com alimentação este mês"_ → skill filtra `category=food` e formata com total de gastos e variação em relação ao mês anterior
- **Cenário Último Débito:** _"O que foi debitado ontem?"_ → skill busca extrato de D-1 e lista transações de saída em ordem cronológica
- **Cenário Extrato Longo:** _"Me mostra o extrato completo dos últimos 30 dias"_ → skill pagina os resultados (20 por vez) e oferece continuar ou enviar por e-mail
- **Cenário Agendamentos:** _"Tenho algo agendado essa semana?"_ → skill chama `get_scheduled` e lista cronologicamente com valores e destinos

---

## 4.3 Skills do InvestmentAgent

### `PortfolioSkill`

Apresenta e explica a carteira de investimentos do cliente de forma clara e educativa.

**Cenários de Uso:**

- **Cenário Carteira Resumida:** _"Como estão meus investimentos?"_ → skill chama `get_portfolio` → exibe total aplicado, rendimento do mês e rentabilidade acumulada por categoria (Renda Fixa, Tesouro, Fundos)
- **Cenário Produto Específico:** _"Como está meu CDB?"_ → skill filtra por tipo no portfólio e detalha vencimento, taxa contratada e valor atual com rendimento
- **Cenário Resgate:** _"Quero resgatar meu Tesouro Direto"_ → skill verifica liquidez do produto → informa prazo de crédito (D+1) → confirma com cliente → chama `redeem`
- **Cenário Relatório de IR:** _"Preciso do informe de rendimentos"_ → skill chama `get_income_report` → gera sumário por tipo de produto, período e imposto retido

---

### `InvestmentRecommendationSkill`

Recomenda produtos de investimento com base no perfil e objetivos declarados pelo cliente.

**Cenários de Uso:**

- **Cenário Novo Investidor:** _"Quero começar a investir"_ → skill chama `get_investor_profile` → se perfil não definido, inicia questionário rápido (3 perguntas sobre prazo, risco e objetivo) → recomenda produtos adequados
- **Cenário por Valor e Prazo:** _"Tenho R$500 para investir por 6 meses"_ → skill filtra `list_available_products` por `min_amount` e período → apresenta top 3 opções com simulação de rendimento líquido
- **Cenário Simulação:** _"Quanto rende R$1.000 em CDB por 1 ano?"_ → skill chama `simulate_investment` → apresenta resultado bruto, IR estimado e valor líquido final
- **Cenário Aplicação:** Cliente confirma investimento → skill chama `invest` → confirma aplicação, atualiza saldo disponível na resposta e informa data de vencimento

---

## 4.4 Skills do CreditAgent

### `LoanSimulationSkill`

Conduz simulações de empréstimo e financiamento de forma transparente e comparativa.

**Cenários de Uso:**

- **Cenário Empréstimo Pessoal:** _"Quero simular um empréstimo de R$5.000"_ → skill coleta prazo → chama `simulate_loan` → apresenta valor da parcela, taxa mensal, taxa anual e CET (Custo Efetivo Total)
- **Cenário Comparação de Prazos:** Após a primeira simulação, skill proativamente oferece comparativo com 12, 18 e 24 parcelas em uma tabela resumida
- **Cenário Financiamento de Imóvel:** _"Quero financiar um apartamento de R$300.000"_ → skill coleta entrada e prazo → chama `simulate_financing` com sistemas SAC e Price → apresenta comparativo lado a lado
- **Cenário Financiamento de Veículo:** Fluxo similar ao imóvel com parâmetros específicos (valor do bem, entrada mínima de 20%, até 60 meses)
- **Cenário Antecipação:** _"Posso antecipar parcelas?"_ → skill chama `anticipate_installments` → mostra desconto aplicado e novo saldo devedor
- **Cenário Score Baixo:** Score abaixo do mínimo para o produto → skill informa a situação, sugere valor menor ou prazo mais curto, e orienta sobre portabilidade de crédito

---

### `CreditManagementSkill`

Gerencia o acompanhamento de créditos ativos, vencimentos e portabilidade.

**Cenários de Uso:**

- **Cenário Visão Geral de Dívidas:** _"Quanto devo ao banco?"_ → skill agrega `list_active_loans` + `list_active_financings` → apresenta total de dívida consolidado, próximo vencimento e opção de antecipação com desconto
- **Cenário Próxima Parcela:** _"Quando vence minha próxima parcela?"_ → skill chama `get_next_installment` → informa data, valor e conta de débito automático
- **Cenário Acompanhamento de Solicitação:** _"Como está meu pedido de empréstimo?"_ → skill chama `get_loan_status` → informa etapa atual (análise, aprovação, contratação) e prazo estimado de resposta
- **Cenário Portabilidade:** _"Tenho um financiamento em outro banco, posso trazer?"_ → skill inicia `request_portability` → explica o processo, documentos necessários e prazo estimado de análise

---

## 4.5 Skills do SupportAgent

### `ManagerCommunicationSkill`

Facilita a comunicação entre o cliente e o gerente de relacionamento designado.

**Cenários de Uso:**

- **Cenário Consulta ao Gerente:** _"Quero falar com meu gerente"_ → skill chama `get_manager_info` → apresenta nome, telefone e e-mail → oferece três opções: enviar mensagem agora, agendar ligação ou continuar pelo chatbot
- **Cenário Agendamento de Ligação:** Cliente opta por ligar → skill coleta data e horário preferenciais → chama `schedule_manager_call` → confirma agendamento e informa que um lembrete será enviado
- **Cenário Mensagem Assíncrona:** _"Manda uma mensagem pro meu gerente sobre aumento de limite"_ → skill categoriza automaticamente (`category=credit`) → chama `send_message_to_manager` → confirma envio com prazo de retorno de até 1 dia útil
- **Cenário Urgência:** Situação de bloqueio indevido ou problema crítico → skill detecta urgência pela análise semântica → eleva a prioridade do agendamento ou inicia fluxo de `EscalationSkill`

---

### `EscalationSkill`

Gerencia a transição suave para atendimento humano quando o chatbot não consegue resolver a demanda.

**Cenários de Uso:**

- **Cenário Insatisfação Detectada:** Usuário expressa frustração após 2+ tentativas sem resolução → skill detecta sentimento negativo → oferece escalação imediata para atendente humano com resumo do contexto
- **Cenário de Alta Complexidade:** Solicitação não mapeada em nenhum toolkit → skill registra o caso via `open_ticket` e informa retorno em até 2 horas úteis
- **Cenário Solicitação Explícita:** _"Quero falar com um atendente"_ → skill verifica disponibilidade e fila de espera → estima tempo → transfere via `escalate_to_human` com histórico completo da sessão
- **Cenário Fora do Horário:** Escalação solicitada fora do horário de atendimento humano → skill informa horário disponível (8h–20h em dias úteis) → oferece: agendar callback, deixar mensagem para o gerente ou abrir ticket com alta prioridade
- **Cenário Pós-Escalação:** Após resolução pelo atendente humano, skill registra o atendimento e envia pesquisa de satisfação (NPS)

---

# 5. Especificação de Funcionalidades

## 5.1 Módulo de Transferências

| Funcionalidade | Detalhamento |
|---|---|
| **PIX — Transferência Imediata** | Transferência via chave PIX (CPF, CNPJ, e-mail, celular ou chave aleatória). Validação do recebedor antes da confirmação. Limite diferenciado para horário noturno (22h–6h: máx. R$1.000). Comprovante gerado automaticamente. |
| **PIX — Agendado** | Agendamento de PIX para data e hora futura. Possibilidade de recorrência (semanal/mensal). Notificação push 1 hora antes da execução. Cancelamento disponível até D-0 às 23h59. |
| **TED — Transferência Eletrônica** | Transferência para qualquer banco brasileiro via código ISPB. Processamento em dias úteis em até 30 minutos. Limite diário configurável. Validação dos dados bancários antes da confirmação. |
| **Gestão de Contatos** | Agenda de favoritos integrada. Busca por nome, CPF ou apelido. Adição e remoção de contatos. Transferência direta a partir da agenda sem redigitar dados. |
| **Chaves PIX** | Registro, consulta e exclusão de chaves PIX. Tipos: CPF, CNPJ, e-mail, celular e chave aleatória. Máximo de 5 chaves por conta PF e 20 por PJ. |

## 5.2 Módulo de Saldo e Extrato

- Saldo em tempo real: conta corrente, poupança e conta salário
- Extrato completo com filtros por período (7, 15, 30, 90 dias ou personalizado)
- Filtro por categoria de gasto (alimentação, transporte, lazer, saúde, etc.)
- Resumo mensal com total de entradas, saídas e saldo líquido
- Consulta de operações agendadas e pendentes
- Pesquisa de lançamento específico por valor ou estabelecimento

## 5.3 Módulo de Investimentos

| Produto | Características no Mock |
|---|---|
| **CDB (CDI)** | Taxas entre 90% e 115% do CDI. Prazo de 30 a 1.800 dias. Liquidez diária ou no vencimento. IR regressivo (22,5% a 15%). |
| **LCI / LCA** | Isento de IR para PF. Prazo mínimo de 90 dias. Taxa entre 85% e 100% do CDI equivalente. |
| **Tesouro Direto** | Tesouro Selic, IPCA+ e Prefixado. Liquidez diária (crédito D+1). Disponível a partir de R$30,00. |
| **Fundos de Investimento** | Renda Fixa, Multimercado e Ações. Diferentes perfis de risco. Resgate em D+0 a D+30 conforme regulamento. |
| **Poupança** | Rendimento automático na data de aniversário. Isento de IR. Liquidez imediata. |

## 5.4 Módulo de Crédito e Financiamentos

- **Empréstimo Pessoal:** até R$50.000, de 6 a 60 parcelas, taxa a partir de 1,99% a.m.
- **Crédito Consignado** (simulado para servidores públicos): taxa a partir de 1,14% a.m.
- **Financiamento Imobiliário:** até 35 anos, até 80% do valor do imóvel, tabelas SAC e Price
- **Financiamento de Veículos:** até 60 meses, taxa a partir de 0,99% a.m.
- Antecipação de parcelas com desconto proporcional
- Portabilidade de crédito de outras instituições
- Consulta de score de crédito interno

## 5.5 Módulo de Suporte e Atendimento

- Comunicação com gerente de relacionamento: mensagem assíncrona e agendamento de ligação
- Abertura e acompanhamento de tickets de suporte com SLA definido
- Base de FAQ com busca semântica para dúvidas frequentes
- Escalação para atendente humano com estimativa de tempo de fila
- Consulta de dados da agência responsável (endereço, telefone, horário)

---

# 6. Mock Data Layer

Para validação do chatbot sem integração com sistemas reais, toda a camada de dados é simulada. Os dados mock são gerados deterministicamente com base no `account_id`, garantindo consistência entre chamadas na mesma sessão.

## 6.1 Contas Mock Disponíveis para Testes

| account_id | Titular | Perfil | Saldo Corrente |
|---|---|---|---|
| `ACC001` | Ana Paula Souza | PF / Conservador | R$ 4.820,50 |
| `ACC002` | Carlos Eduardo Lima | PF / Moderado | R$ 12.310,00 |
| `ACC003` | Fernanda Costa Ltda | PJ / Empresarial | R$ 87.650,00 |
| `ACC004` | Roberto Martins | PF / Arrojado | R$ 2.100,75 |

## 6.2 Comportamentos dos Dados Mock

- **Saldo:** varia de forma determinística conforme `account_id` e timestamp da sessão
- **Extrato:** gerado com 30–90 lançamentos fictícios por mês, com categorias realistas
- **PIX:** simula latência de 800ms–1.500ms; taxa de sucesso de 95%, 5% de falha aleatória controlada
- **TED:** simula janela de operação 6h–17h em dias úteis; fora do horário retorna erro com orientação
- **Investimentos:** rentabilidade calculada com CDI fictício de 10,5% a.a.
- **Score de Crédito:** ACC001 = 720 | ACC002 = 650 | ACC003 = 810 | ACC004 = 580

---

# 7. Requisitos Não Funcionais

| Categoria | Requisito | Meta / SLA |
|---|---|---|
| **Performance** | Tempo de resposta do chatbot | < 2 segundos para 95% das mensagens |
| **Disponibilidade** | Uptime do sistema | 99,9% (máx. 8,7h de indisponibilidade/ano) |
| **Segurança** | Autenticação de sessão | JWT com expiração de 30 min + biometria para transações |
| **Segurança** | Criptografia de dados | TLS 1.3 em trânsito; AES-256 em repouso |
| **Acessibilidade** | Leitores de tela | Compatível com WCAG 2.1 nível AA |
| **Escalabilidade** | Sessões simultâneas | Suporte a 10.000 usuários simultâneos |
| **Conformidade** | LGPD | Dados sensíveis mascarados; consentimento registrado |
| **Conformidade** | Banco Central | Conformidade com Resolução BCB nº 96/2021 (PIX) |

---

# 8. Roadmap de Desenvolvimento

| Fase | Período | Escopo |
|---|---|---|
| **Fase 1 — MVP** | Meses 1–2 | Setup Agno Framework + OrchestratorAgent + BankingAgent (saldo, extrato, PIX simples) + Mock Data Layer básica |
| **Fase 2 — Core Banking** | Meses 3–4 | TEDToolkit, gestão de contatos, chaves PIX, SupportAgent, ManagerCommunicationSkill, EscalationSkill |
| **Fase 3 — Crédito** | Meses 5–6 | CreditAgent, LoanToolkit, simulações de empréstimo e financiamento, CreditManagementSkill |
| **Fase 4 — Investimentos** | Meses 7–8 | InvestmentAgent, InvestmentToolkit, perfil de investidor, recomendações, relatório de IR |
| **Fase 5 — Refinamento** | Meses 9–10 | Otimização de skills, personalização por segmento, A/B testing de fluxos, analytics de conversação |

---

*BancoBot AI — PRD v1.0 | FinBank S.A. | Documento Confidencial*
