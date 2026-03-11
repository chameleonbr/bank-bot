# 🏦 BancoBot AI
## Product Requirements Document
**Intelligent Banking Chatbot with Agno Framework**

| Field | Value |
|---|---|
| Version | 1.0 |
| Date | March / 2025 |
| Status | Draft — For Review |
| Framework | Agno (agno.com) |
| Classification | Confidential |

---

# 1. Product Overview

## 1.1 Executive Summary

BancoBot AI is a banking virtual assistant developed for the fictional bank **FinBank S.A.**, aimed at offering customers a complete, secure, and efficient digital service experience via chat. The system is built on the **Agno Framework (agno.com)**, leveraging its AI agent architecture with support for tools, toolkits, and agent skills.

The chatbot centralizes everyday banking operations, reducing the need for human attendance for routine demands and offering 24/7 availability.

## 1.2 Business Objectives

- Reduce call center volume for routine operations by up to **60%**
- Offer service available **24 hours a day, 7 days a week**
- Increase NPS for digital operations (target: > 75)
- Decrease average resolution time from 8 min to **< 2 min**
- Increase adoption of investment and credit products via digital channels

## 1.3 Target Audience

| Segment | Profile | Primary Need |
|---|---|---|
| Individual (PF) | 18–35 years, digitally active | Agility in transactions (PIX, statement) |
| Individual (PF) | 36–60 years, long-time customer | Support and clarification of doubts |
| Legal Entity (PJ) | MEI and PME | Loans, TEDs, and reports |
| Legal Entity (PJ) | Large companies | Investments and priority service |

---

# 2. Technical Architecture — Agno Framework

## 2.1 Architecture Overview

BancoBot AI is structured as a **multi-agent system** using the Agno Framework, where each functional domain is handled by a specialized agent, orchestrated by a central agent (Orchestrator Agent). All communication between agents is asynchronous and driven by structured messages.

**Main Components:**

- **Orchestrator Agent** — Central agent that interprets user intent and delegates to the correct specialized agent
- **Domain Agents** — Specialized agents by domain: Banking, Investments, Credit, Support
- **Toolkits** — Collections of tools grouped by functional domain (e.g., BankingToolkit, PIXToolkit)
- **Agent Skills** — Declarative abilities registered in each agent to guide behaviors
- **Memory Store** — Session context and interaction history persisted for continuity
- **Mock Data Layer** — Simulated data layer for validation without real systems

## 2.2 Processing Flow

1. Customer sends a message in the channel (mobile app, internet banking, or WhatsApp)
2. Orchestrator Agent receives the message and executes intent analysis (Intent Classification Skill)
3. Orchestrator delegates the task to the corresponding Domain Agent via Agno message routing
4. Domain Agent activates necessary tools from the registered Toolkit
5. Tools access the Mock Data Layer and return structured data
6. Domain Agent composes the response using formatting and personalization Agent Skills
7. Response is delivered to the customer with context, clarity, and suggested actions

## 2.3 Agent Structure

| Agent | Responsibility | Registered Toolkits | Active Skills |
|---|---|---|---|
| `OrchestratorAgent` | Routing and intent classification | RouterToolkit | IntentSkill, ContextSkill |
| `BankingAgent` | Transactions, statements, balance, contacts | BankingToolkit, PIXToolkit, TEDToolkit | TransactionSkill, StatementSkill |
| `InvestmentAgent` | Investments and portfolio | InvestmentToolkit | PortfolioSkill, RecommendationSkill |
| `CreditAgent` | Loans and financing | CreditToolkit, LoanToolkit | CreditSkill, SimulationSkill |
| `SupportAgent` | Manager, doubts, escalation | SupportToolkit | EscalationSkill, FAQSkill |

---

# 3. Toolkits and Tools

The Agno Framework organizes tools into **Toolkits** — cohesive groups of Tools that share context and configuration. Below are defined all Toolkits and their corresponding Tools for BancoBot AI.

## 3.1 BankingToolkit

Central toolkit for checking account and savings operations.

| Tool Name | Description | Key Parameters |
|---|---|---|
| `get_balance` | Returns available, blocked, and total account balance | `account_id`, `account_type` |
| `get_statement` | Fetches statement by period with filters | `account_id`, `start_date`, `end_date`, `category`, `limit` |
| `get_account_info` | Returns registration data and account information | `account_id` |
| `list_contacts` | Lists saved contacts for transfer | `account_id`, `search_term` |
| `add_contact` | Adds a new contact to the banking agenda | `name`, `cpf_cnpj`, `bank`, `agency`, `account` |
| `remove_contact` | Removes a contact from the banking agenda | `account_id`, `contact_id` |
| `get_scheduled` | Lists scheduled transfers and payments | `account_id`, `date_from`, `date_to` |
| `cancel_scheduled` | Cancels a scheduled operation | `account_id`, `schedule_id` |

## 3.2 PIXToolkit

Toolkit dedicated to PIX operations — instant payments regulated by the Central Bank of Brazil.

| Tool Name | Description | Key Parameters |
|---|---|---|
| `pix_transfer` | Executes immediate PIX transfer | `origin_account`, `pix_key`, `amount`, `description` |
| `pix_schedule` | Schedules a PIX for a future date/time | `origin_account`, `pix_key`, `amount`, `schedule_datetime` |
| `get_pix_keys` | Lists PIX keys registered in the account | `account_id` |
| `register_pix_key` | Registers a new PIX key (CPF, CNPJ, email, mobile, random) | `account_id`, `key_type`, `key_value` |
| `delete_pix_key` | Removes a registered PIX key | `account_id`, `pix_key_id` |
| `validate_pix_key` | Validates and returns recipient data by PIX key | `pix_key` |
| `get_pix_limits` | Returns PIX transfer limits (day and night) | `account_id` |
| `update_pix_limit` | Requests a change to PIX limit (subject to grace period) | `account_id`, `new_limit_daytime`, `new_limit_nighttime` |
| `get_pix_receipt` | Generates a PIX transaction receipt in structured format | `transaction_id` |

## 3.3 TEDToolkit

Toolkit for TED (Transferência Eletrônica Disponível) transfers between different financial institutions.

| Tool Name | Description | Key Parameters |
|---|---|---|
| `ted_transfer` | Executes TED to an account in another bank | `origin_account`, `bank_code`, `agency`, `account`, `cpf_cnpj`, `amount` |
| `ted_schedule` | Schedules TED for a future business day | `origin_account`, `dest_data`, `amount`, `schedule_date` |
| `validate_ted_dest` | Validates recipient banking data for TED | `bank_code`, `agency`, `account`, `cpf_cnpj` |
| `get_ted_receipt` | Generates a TED receipt in structured format | `transaction_id` |
| `get_ted_limits` | Returns TED limits per period | `account_id` |
| `list_banks` | Lists available banks with ISPB code | `search_term` |

## 3.4 InvestmentToolkit

Toolkit for visualization and management of the investment portfolio.

| Tool Name | Description | Key Parameters |
|---|---|---|
| `get_portfolio` | Returns full position of the investment portfolio | `account_id` |
| `get_product_info` | Details an investment product (CDB, LCI, etc.) | `product_id` |
| `list_available_products` | Lists investment products available for the profile | `account_id`, `risk_profile`, `min_amount` |
| `simulate_investment` | Simulates investment profitability | `product_id`, `amount`, `period_days` |
| `invest` | Executes application in an investment product | `account_id`, `product_id`, `amount` |
| `redeem` | Requests investment redemption (total or partial) | `account_id`, `investment_id`, `amount` |
| `get_investor_profile` | Returns investor profile (conservative/moderate/aggressive) | `account_id` |
| `get_income_report` | Generates income report per period | `account_id`, `year` |

## 3.5 CreditToolkit

Toolkit for personal credit, payroll-deducted loans, and borrowings.

| Tool Name | Description | Key Parameters |
|---|---|---|
| `get_credit_limit` | Returns available and utilized credit limit | `account_id` |
| `simulate_loan` | Simulates personal loan (installments, interest, CET) | `account_id`, `amount`, `num_installments`, `loan_type` |
| `request_loan` | Initiates a personal loan request | `account_id`, `amount`, `num_installments`, `purpose` |
| `get_loan_status` | Checks status of an ongoing request | `account_id`, `loan_request_id` |
| `list_active_loans` | Lists active loans with outstanding balance | `account_id` |
| `get_loan_statement` | Payment history for a loan | `loan_id` |
| `anticipate_installments` | Simulates and requests early installment payment | `loan_id`, `num_installments_to_anticipate` |
| `get_credit_score` | Returns internal credit score of the customer | `account_id` |

## 3.6 LoanToolkit (Financing)

Specific toolkit for long-term financing: real estate, vehicles, and rural credit.

| Tool Name | Description | Key Parameters |
|---|---|---|
| `simulate_financing` | Simulates financing with SAC, Price, or Mixed tables | `amount`, `entry_value`, `period_months`, `modality`, `system` |
| `list_financing_lines` | Lists available financing lines | `modality` |
| `request_financing` | Initiates financing application process | `account_id`, `modality`, `property_value`, `entry_value`, `period_months` |
| `get_financing_status` | Tracks the financing process stage | `account_id`, `financing_id` |
| `list_active_financings` | Lists customer's active financings | `account_id` |
| `get_financing_statement` | Detailed statement for an active financing | `financing_id` |
| `get_next_installment` | Informs about the date and value of the next installment | `financing_id` |
| `request_portability` | Initiates a financing portability request | `financing_id`, `target_bank_code` |

## 3.7 SupportToolkit

Toolkit for customer support, escalation, and communication with managers.

| Tool Name | Description | Key Parameters |
|---|---|---|
| `open_ticket` | Opens a categorized support ticket | `account_id`, `category`, `description`, `priority` |
| `get_ticket_status` | Consults the status of an open ticket | `ticket_id` |
| `list_open_tickets` | Lists all open tickets for the customer | `account_id` |
| `schedule_manager_call` | Schedules a call with the relationship manager | `account_id`, `preferred_date`, `preferred_time`, `subject` |
| `send_message_to_manager` | Sends an asynchronous message to the manager | `account_id`, `message`, `category` |
| `get_manager_info` | Returns contact details of the responsible manager | `account_id` |
| `escalate_to_human` | Escalates conversation to a human agent in real-time | `session_id`, `reason`, `priority` |
| `get_faq` | Searches answer in knowledge base/FAQ | `query`, `category` |
| `get_branch_info` | Provides information about the agency and its hours | `account_id` |

---

# 4. Agent Skills

Agent Skills in the Agno Framework are **declarative capabilities** registered in agents that define behaviors, business rules, and interaction flows. Each skill is activated contextually based on the situation detected by the agent.

## 4.1 OrchestratorAgent Skills

### `IntentClassificationSkill`

Responsible for identifying user intent and mapping to the correct agent and toolkit.

**Usage Scenarios:**

- **Scenario 1 — Direct PIX:** User writes _"I want to make a PIX of 200 reais"_ → classifies as `PIX_TRANSFER`, delegates to `BankingAgent`
- **Scenario 2 — Filtered Balance Inquiry:** User writes _"how much do I have in savings?"_ → classifies as `BALANCE_INQUIRY`, filters `account_type=savings`
- **Scenario 3 — Ambiguous Intent:** Message _"I want to invest"_ → activates `ClarificationSkill` to collect value and term before delegating
- **Scenario 4 — Support Request:** User mentions _"manager"_ or _"complaint"_ → prioritizes `SupportAgent` with `is_complaint=true` flag
- **Scenario 5 — Out of Scope:** Non-banking message → activates `OutOfScopeSkill` and redirects politely

---

### `ContextRetentionSkill`

Maintains conversation context between turns to prevent the user from having to repeat information.

**Usage Scenarios:**

- **Scenario 1 — Account Continuity:** User asks for balance, then says _"transfer 500 to João"_ → skill uses account identified in previous turn
- **Scenario 2 — Parameter Preservation:** Ongoing loan simulation → skill preserves amount and term entered during the confirmation stage
- **Scenario 3 — Session Resumption:** User abandons flow and returns in 5 min → skill restores state if session is still active (TTL: 30 min)
- **Scenario 4 — Multiple Accounts:** Customer with checking and savings accounts → skill requests confirmation and saves preference during the session

---

## 4.2 BankingAgent Skills

### `TransactionSkill`

Manages the full flow of PIX and TED transactions, including validation, confirmation, and receipt issuance.

**Usage Scenarios:**

- **Simple PIX Scenario:** Customer provides PIX key and amount → skill validates key (`validate_pix_key`) → displays recipient name and amount → requests confirmation → executes `pix_transfer` → displays receipt
- **Scheduled PIX Scenario:** Customer wants to pay a bill tomorrow → skill collects date/time → calls `pix_schedule` → confirms scheduling with reference ID
- **TED Scenario:** Customer provides agency, account, and bank → skill calls `validate_ted_dest` → confirms data → executes `ted_transfer`
- **Limit Exceeded Scenario:** Amount exceeds night limit (10 PM – 6 AM) → skill informs current limit → offers options: schedule for daytime hours, request limit increase, or split the amount
- **Favorite Contact Scenario:** _"Send 150 reais to Maria"_ → skill searches in `list_contacts` → confirms identity → confirms transfer
- **Invalid Key Scenario:** Non-existent PIX key → skill explains the error and requests a new key without restarting the flow

---

### `StatementSkill`

Organizes and presents statements and balances in a contextualized and readable manner.

**Usage Scenarios:**

- **Balance Scenario:** _"What's my balance?"_ → skill calls `get_balance` → presents highlighted available balance, separate blocked balance, and update date/time
- **Today's Statement Scenario:** _"My statement for today"_ → skill calls `get_statement` with `start_date` and `end_date = today` → groups by category and displays summary
- **Filtered by Category Scenario:** _"Food expenses this month"_ → skill filters `category=food` and formats with total spending and variance compared to the previous month
- **Last Debit Scenario:** _"What was debited yesterday?"_ → skill fetches statement from D-1 and lists outgoing transactions in chronological order
- **Long Statement Scenario:** _"Show me the full statement for the last 30 days"_ → skill paginates results (20 at a time) and offers to continue or send via email
- **Scheduled Operations Scenario:** _"Do I have anything scheduled this week?"_ → skill calls `get_scheduled` and lists chronologically with amounts and destinations

---

## 4.3 InvestmentAgent Skills

### `PortfolioSkill`

Presents and explains the customer's investment portfolio clearly and educationally.

**Usage Scenarios:**

- **Summary Portfolio Scenario:** _"How are my investments doing?"_ → skill calls `get_portfolio` → displays total invested, monthly return, and accumulated profitability by category (Fixed Income, Treasury, Funds)
- **Specific Product Scenario:** _"How's my CDB?"_ → skill filters by type in the portfolio and details maturity, contracted rate, and current value with return
- **Redemption Scenario:** _"I want to redeem my Tesouro Direto"_ → skill checks product liquidity → informs credit term (D+1) → confirms with customer → calls `redeem`
- **Income Report Scenario:** _"I need the income report"_ → skill calls `get_income_report` → generates summary by product type, period, and tax withheld

---

### `InvestmentRecommendationSkill`

Recommends investment products based on the profile and objectives declared by the customer.

**Usage Scenarios:**

- **New Investor Scenario:** _"I want to start investing"_ → skill calls `get_investor_profile` → if profile not defined, starts a quick questionnaire (3 questions about term, risk, and goal) → recommends suitable products
- **By Amount and Term Scenario:** _"I have R$500 to invest for 6 months"_ → skill filters `list_available_products` by `min_amount` and term → presents top 3 options with net yield simulation
- **Simulation Scenario:** _"How much does R$1,000 in CDB yield for 1 year?"_ → skill calls `simulate_investment` → presents gross result, estimated Income Tax (IR), and final net value
- **Application Scenario:** Customer confirms investment → skill calls `invest` → confirms application, updates available balance in the response, and informs maturity date

---

## 4.4 CreditAgent Skills

### `LoanSimulationSkill`

Conducts loan and financing simulations transparently and comparatively.

**Usage Scenarios:**

- **Personal Loan Scenario:** _"I want to simulate a loan of R$5,000"_ → skill collects term → calls `simulate_loan` → presents installment value, monthly rate, annual rate, and CET (Total Effective Cost)
- **Term Comparison Scenario:** After the first simulation, skill proactively offers comparison with 12, 18, and 24 installments in a summary table
- **Real Estate Financing Scenario:** _"I want to finance an apartment for R$300,000"_ → skill collects entry and term → calls `simulate_financing` with SAC and Price systems → presents side-by-side comparison
- **Vehicle Financing Scenario:** Similar flow to real estate with specific parameters (asset value, minimum 20% entry, up to 60 months)
- **Early Payment Scenario:** _"Can I pay installments early?"_ → skill calls `anticipate_installments` → shows applied discount and new outstanding balance
- **Low Score Scenario:** Score below minimum for the product → skill informs the situation, suggests smaller amount or shorter term, and guides on credit portability

---

### `CreditManagementSkill`

Manages tracking of active credits, maturities, and portability.

**Usage Scenarios:**

- **Debt Overview Scenario:** _"How much do I owe the bank?"_ → skill aggregates `list_active_loans` + `list_active_financings` → presents consolidated total debt, next maturity, and early payment option with discount
- **Next Installment Scenario:** _"When is my next installment due?"_ → skill calls `get_next_installment` → informs date, amount, and automatic debit account
- **Request Tracking Scenario:** _"How is my loan application doing?"_ → skill calls `get_loan_status` → informs current stage (analysis, approval, contracting) and estimated response time
- **Portability Scenario:** _"I have financing at another bank, can I bring it over?"_ → skill initiates `request_portability` → explains the process, necessary documents, and estimated analysis time

---

## 4.5 SupportAgent Skills

### `ManagerCommunicationSkill`

Facilitates communication between the customer and the designated relationship manager.

**Usage Scenarios:**

- **Consulting the Manager Scenario:** _"I want to talk to my manager"_ → skill calls `get_manager_info` → presents name, phone, and email → offers three options: send message now, schedule a call, or continue via chatbot
- **Scheduling a Call Scenario:** Customer chooses to call → skill collects preferred date and time → calls `schedule_manager_call` → confirms scheduling and informs that a reminder will be sent
- **Asynchronous Message Scenario:** _"Send a message to my manager about limit increase"_ → skill automatically categorizes (`category=credit`) → calls `send_message_to_manager` → confirms sending with a return time of up to 1 business day
- **Urgency Scenario:** Indue blockage situation or critical problem → skill detects urgency through semantic analysis → elevates scheduling priority or initiates `EscalationSkill` flow

---

### `EscalationSkill`

Manages a smooth transition to human service when the chatbot cannot resolve the demand.

**Usage Scenarios:**

- **Dissatisfaction Detected Scenario:** User expresses frustration after 2+ attempts without resolution → skill detects negative sentiment → offers immediate escalation to a human agent with context summary
- **High Complexity Scenario:** Request not mapped in any toolkit → skill registers the case via `open_ticket` and informs return in up to 2 business hours
- **Explicit Request Scenario:** _"I want to talk to an agent"_ → skill checks availability and waiting queue → estimates time → transfers via `escalate_to_human` with full session history
- **Outside Hours Scenario:** Escalation requested outside human service hours (8 AM – 8 PM on business days) → skill informs available hours → offers: schedule callback, leave message for manager, or open a high-priority ticket
- **Post-Escalation Scenario:** After resolution by a human agent, skill records the service and sends a satisfaction survey (NPS)

---

# 5. Feature Specification

## 5.1 Transfer Module

| Feature | Details |
|---|---|
| **PIX — Immediate Transfer** | Transfer via PIX key (CPF, CNPJ, email, mobile, or random key). Recipient validation before confirmation. Differentiated limit for nighttime hours (10 PM – 6 AM: max R$1,000). Receipt generated automatically. |
| **PIX — Scheduled** | PIX scheduling for future date and time. Recurrence possibility (weekly/monthly). Push notification 1 hour before execution. Cancellation available until D-0 at 11:59 PM. |
| **TED — Electronic Transfer** | Transfer to any Brazilian bank via ISPB code. Processing on business days in up to 30 minutes. Configurable daily limit. Validation of banking data before confirmation. |
| **Contact Management** | Integrated favorites agenda. Search by name, CPF, or nickname. Adding and removing contacts. Direct transfer from agenda without re-typing data. |
| **PIX Keys** | Registration, consultation, and exclusion of PIX keys. Types: CPF, CNPJ, email, mobile, and random key. Maximum of 5 keys per PF account and 20 per PJ. |

## 5.2 Balance and Statement Module

- Real-time balance: checking, savings, and salary accounts
- Full statement with filters by period (7, 15, 30, 90 days or custom)
- Filter by spending category (food, transport, leisure, health, etc.)
- Monthly summary with total income, expenses, and net balance
- Consultation of scheduled and pending operations
- Search for a specific entry by value or establishment

## 5.3 Investments Module

| Product | Mock Characteristics |
|---|---|
| **CDB (CDI)** | Rates between 90% and 115% of CDI. Term from 30 to 1,800 days. Daily liquidity or at maturity. Regressive Income Tax (22.5% to 15%). |
| **LCI / LCA** | Income Tax exempt for PF. Minimum term of 90 days. Rate between 85% and 100% of equivalent CDI. |
| **Tesouro Direto** | Tesouro Selic, IPCA+, and Prefixado. Daily liquidity (D+1 credit). Available from R$30.00. |
| **Investment Funds** | Fixed Income, Multimarket, and Stocks. Different risk profiles. Redemption in D+0 to D+30 as per regulations. |
| **Savings (Poupança)** | Automatic yield on birthday date. Income Tax exempt. Immediate liquidity. |

## 5.4 Credit and Financing Module

- **Personal Loan:** up to R$50,000, 6 to 60 installments, rate starting at 1.99% p.m.
- **Payday Loan** (simulated for public servants): rate starting at 1.14% p.m.
- **Mortgage Financing:** up to 35 years, up to 80% of property value, SAC and Price tables
- **Vehicle Financing:** up to 60 months, rate starting at 0.99% p.m.
- Early payment of installments with proportional discount
- Credit portability from other institutions
- Internal credit score consultation

## 5.5 Support and Service Module

- Communication with relationship manager: asynchronous message and call scheduling
- Opening and tracking of support tickets with defined SLA
- FAQ base with semantic search for frequent doubts
- Escalation to human agent with estimated queue time
- Agency information consultation (address, phone, hours)

---

# 6. Mock Data Layer

For validation of the chatbot without integration with real systems, all data layer is simulated. Mock data is generated deterministically based on `account_id`, ensuring consistency between calls in the same session.

## 6.1 Mock Accounts Available for Testing

| account_id | Holder | Profile | Checking Balance |
|---|---|---|---|
| `ACC001` | Ana Paula Souza | PF / Conservative | R$ 4,820.50 |
| `ACC002` | Carlos Eduardo Lima | PF / Moderate | R$ 12,310.00 |
| `ACC003` | Fernanda Costa Ltda | PJ / Business | R$ 87,650.00 |
| `ACC004` | Roberto Martins | PF / Aggressive | R$ 2,100.75 |

## 6.2 Mock Data Behaviors

- **Balance:** varies deterministically according to `account_id` and session timestamp
- **Statement:** generated with 30–90 fictitious entries per month, with realistic categories
- **PIX:** simulates latency of 800ms–1,500ms; 95% success rate, 5% controlled random failure
- **TED:** simulates operation window 6 AM – 5 PM on business days; outside hours returns error
- **Investments:** yields calculated with fictitious CDI of 10.5% p.a.
- **Credit Score:** ACC001 = 720 | ACC002 = 650 | ACC003 = 810 | ACC004 = 580

---

# 7. Non-Functional Requirements

| Category | Requirement | Target / SLA |
|---|---|---|
| **Performance** | Chatbot response time | < 2 seconds for 95% of messages |
| **Availability** | System uptime | 99.9% (max 8.7h unavailability/year) |
| **Security** | Session authentication | JWT with 30 min expiration + biometrics for transactions |
| **Security** | Data encryption | TLS 1.3 in transit; AES-256 at rest |
| **Accessibility** | Screen readers | Compatible with WCAG 2.1 level AA |
| **Scalability** | Simultaneous sessions | Support for 10,000 simultaneous users |
| **Compliance** | LGPD | Sensitive data masked; consent recorded |
| **Compliance** | Central Bank | Compliance with BCB Resolution No. 96/2021 (PIX) |

---

# 8. Development Roadmap

| Phase | Period | Scope |
|---|---|---|
| **Phase 1 — MVP** | Months 1–2 | Setup Agno Framework + OrchestratorAgent + BankingAgent (balance, statement, simple PIX) + basic Mock Data Layer |
| **Phase 2 — Core Banking** | Months 3–4 | TEDToolkit, contact management, PIX keys, SupportAgent, ManagerCommunicationSkill, EscalationSkill |
| **Phase 3 — Credit** | Months 5–6 | CreditAgent, LoanToolkit, loan and financing simulations, CreditManagementSkill |
| **Phase 4 — Investments** | Months 7–8 | InvestmentAgent, InvestmentToolkit, investor profile, recommendations, income report |
| **Phase 5 — Refinement** | Months 9–10 | Skill optimization, personalization by segment, A/B testing, conversation analytics |

---

*BancoBot AI — PRD v1.0 | FinBank S.A. | Confidential Document*
