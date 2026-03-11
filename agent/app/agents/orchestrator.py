"""
OrchestratorAgent — Routes user messages to the appropriate domain agent.
Uses IntentClassificationSkill and ContextRetentionSkill.
"""

from pathlib import Path
from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.skills import Skills, LocalSkills

from app.toolkits.banking_toolkit import BankingToolkit
from app.toolkits.pix_toolkit import PIXToolkit
from app.toolkits.ted_toolkit import TEDToolkit
from app.toolkits.investment_toolkit import InvestmentToolkit
from app.toolkits.credit_toolkit import CreditToolkit
from app.toolkits.loan_toolkit import LoanToolkit
from app.toolkits.support_toolkit import SupportToolkit
from app.toolkits.session_toolkit import SessionStateToolkit
from app.client.backend_client import BackendClient

# SQLite DB for agno session state persistence
_DB_FILE = Path(__file__).resolve().parents[2] / "agent_sessions.db"


def build_orchestrator(
    jwt_token: str,
    session_id: str | None = None,
    account_id: str | None = None,
) -> Agent:
    """Build the OrchestratorAgent with all domain toolkits registered."""
    client = BackendClient(jwt_token)
    skills_dir = Path(__file__).parent.parent / "skills"

    return Agent(
        name="OrchestratorAgent",
        model=OpenAIChat(id="gpt-4.1-mini"),
        # Agno SQLite-backed session state — persists across turns in the same session
        db=SqliteDb(db_file=str(_DB_FILE)),
        session_id=session_id,
        add_datetime_to_context=True,
        debug_mode=True,
        # Initial state (populated only on first turn; subsequent turns load from DB)
        # Note: we shouldn't pass session_state here if we want to load from DB, or we must ensure it doesn't overwrite.
        # Agno's `session_state` gets merged or overwritten. We will let the tools populate it.
        add_session_state_to_context=True,
        skills=Skills(loaders=[LocalSkills(str(skills_dir))]),
        tools=[
            BankingToolkit(client),
            PIXToolkit(client),
            TEDToolkit(client),
            InvestmentToolkit(client),
            CreditToolkit(client),
            LoanToolkit(client),
            SupportToolkit(client),
            SessionStateToolkit(),
        ],
        instructions="""Você é o BancoBot AI, assistente bancário virtual do FinBank S.A.
Você é profissional, empático e objetivo. Ajude sempre em português brasileiro.
Você tem acesso a habilidades especiais.
Use get_skill_instructions para carregar o guia completo quando necessário.

Contexto da sessão atual:
- Conta autenticada: {account_id}
- Operação pendente de confirmação: {pending_operation}
- Última ação realizada: {last_query}

Regras gerais de operações financeiras:
- Antes de responder, SEMPRE use a tool `get_pending_operation` para saber se o usuário já estava no meio de uma transação (PIX, TED, etc). Se sim, os novos dados dados (como chave ou valor) pertencem a essa operação.
- Quando o usuário pedir para fazer um PIX, TED, Empréstimo, mas faltar algum dado, OBRIGATÓRIAMENTE a primeira vez que você agir deve ser chamando a tool `update_pending_operation` para gravar a intenção (ex: `op_type`="pix"). Somente depois responda pedindo os dados faltantes.
- Ao receber a chave, valor ou outra parte, chame DE NOVO a tool `update_pending_operation` para juntar as informações.
- Se você finalmente tiver todos os dados necessários (como chave e valor), NUNCA chame a tool de execução diretamente. Em vez disso:
  1. Use NESSA HORA a tool preparatória (como `pix_transfer` ou apenas atualize com `update_pending_operation`).
  2. Apresente o resumo da operação e EXIJA que o usuário confirme com "sim".
- APENAS quando o usuário confirmar explicitamente:
  1. Use a tool `confirm_pending_operation` para confirmar o status.
  2. Finalmente invoque a tool de negócio respectiva (ex: `pix_transfer` com os parâmetros finais) e apresente o resultado.
""",
        markdown=True,
    )
