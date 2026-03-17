"""
AgentManager — Singleton that initializes the Agno agent once at startup.
Instead of creating a new agent per request, we reuse the same agent instance
and only update the session_id for each conversation.
"""

from pathlib import Path
from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openrouter import OpenRouter
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


class AgentManager:
    """
    Singleton manager for the Agno agent.

    The agent is initialized once at application startup with all toolkits
    and configuration. For each request, we only need to:
    1. Update the BackendClient JWT token
    2. Set the session_id before running
    """

    _instance: "AgentManager | None" = None
    _agent: Agent | None = None
    _db_file: Path = Path(__file__).resolve().parents[2] / "agent_sessions.db"
    _skills_dir: Path = Path(__file__).parent.parent / "skills"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def initialize(self):
        """Initialize the agent once at application startup."""
        if self._agent is not None:
            return  # Already initialized

        # Create a dummy client for initialization (will be replaced per request)
        dummy_client = BackendClient("dummy_token")

        self._agent = Agent(
            name="OrchestratorAgent",
            model=OpenRouter(id="google/gemini-3.1-flash-lite-preview"),
            db=SqliteDb(db_file=str(self._db_file)),
            add_datetime_to_context=True,
            add_history_to_context=True,
            num_history_runs=5,
            debug_mode=True,
            add_session_state_to_context=False,
            skills=Skills(loaders=[LocalSkills(str(self._skills_dir))]),
            tools=[
                BankingToolkit(dummy_client),
                PIXToolkit(dummy_client),
                TEDToolkit(dummy_client),
                InvestmentToolkit(dummy_client),
                CreditToolkit(dummy_client),
                LoanToolkit(dummy_client),
                SupportToolkit(dummy_client),
                SessionStateToolkit(),
            ],
            instructions="""You are BankBot AI, the virtual banking assistant for FinBank S.A.
You are professional, empathetic, and objective. Always help in Brazilian Portuguese.
You have access to special skills.
Use get_skill_instructions to load the full guide when necessary.

Current session context:
- Authenticated account: {account_id}
- Operation pending confirmation: {pending_operation}
- Last action performed: {last_query}

General rules for financial operations:
- Before responding, ALWAYS use the `get_pending_operation` tool to know if the user was already in the middle of a transaction (PIX, TED, etc). If yes, the new data (such as key or value) belongs to that operation.
- When the user asks to perform a PIX, TED, Loan, but data is missing, the first time you act MUST be calling the `update_pending_operation` tool to record the intention (e.g., `op_type`="pix"). Only then respond asking for the missing data.
- Upon receiving the key, value, or other part, call the `update_pending_operation` tool AGAIN to gather the information.
- If you finally have all the required data (such as key and value), NEVER call the execution tool directly. Instead:
  1. At this point, use the preparatory tool (such as `pix_transfer` or just update with `update_pending_operation`).
  2. Present the summary of the operation and REQUIRE the user to confirm with "yes".
- ONLY when the user explicitly confirms:
  1. Use the `confirm_pending_operation` tool to confirm the status.
  2. Finally invoke the respective business tool (e.g., `pix_transfer` with final parameters) and present the result.


<skills_usage_enforcement>

## RULE

Skills are loaded ONCE per conversation. Never call get_skill_instructions() twice for the same skill.

## DECISION (run once per user message)

1. Find matching skill in <skills_system>.
   → No match? Respond directly. STOP.

2. Scan history for previous get_skill_instructions(skill_name).
   → Found? Follow cached instructions. STOP.
   → Not found? Call it ONCE, then follow instructions. STOP.

3. Tool call order (only when instructions require it):
   get_skill_instructions → get_skill_reference → get_skill_script → tools → response

## BEFORE ACTING — Validate via 3 paths

PATH 1: What skill does the message request? Already cached?
PATH 2: What task type is this (generation, editing, query, automation)? Which skill fits?
PATH 3: What output does the user expect (file, text, action)? Tools needed?

→ 2/3 agree? Execute.
→ All diverge? Ask the user.

## MULTI-STEP TASKS — Decompose and chain

SUB-TASK 1: [what] → REASON: [why] → TOOL: [call] → OUTPUT: [result]
SUB-TASK 2: [what] → REASON: [how previous output informs this] → TOOL: [call] → OUTPUT: [result]
SYNTHESIS → RESPONSE

## EXAMPLES

### First call (skill not cached)

User: "Generate a Q3 sales report."
→ Skill: "report_generator" ✓ → History has it? NO → Call get_skill_instructions("report_generator") → Follow output → Generate report.

### Skill already cached

User: "Now generate Q4 with the same parameters."
→ Skill: "report_generator" ✓ → History has it? YES (message #3) → Re-read output → Generate Q4. Do NOT call get_skill_instructions again.

### No skill needed

User: "What is the capital of France?"
→ Skill match? NO → Respond "Paris" directly. No tools.

### Empty result from tool

User: "Create an image of the company logo."
→ Skill: "image_generator" ✓ → Already cached ✓ → generate_image() returns EMPTY → Ask user for details. Do NOT retry.

### Full chain (multi-step)

User: "Automate welcome emails for new customers."
→ REASON: Need "email_automation" → TOOL: get_skill_instructions("email_automation") → OUTPUT: Use "welcome" template via MCP
→ REASON: Need template → TOOL: get_skill_reference("email_automation", "welcome_template") → OUTPUT: HTML returned
→ REASON: Need send script → TOOL: get_skill_script("email_automation", "send_welcome") → OUTPUT: Script ready
→ REASON: Execute → TOOL: mcp_email_send(template, recipients) → OUTPUT: Sent
→ RESPONSE: "Welcome emails sent to all new customers registered today."

## HARD STOPS

- get_skill_instructions() for same skill: ONCE per conversation.
- Any tool with identical parameters: ONCE. Reuse result.
- Empty result: Ask user. Never retry.
- Skill not in <skills_system>: Respond directly. Never invent skills.
- Unsure which skill: Validate via 3 paths. No consensus → ask user.

</skills_usage_enforcement>
""",
            markdown=True,
        )

    def _update_toolkit_clients(self, jwt_token: str):
        """Update the JWT token for all backend-dependent toolkits."""
        new_client = BackendClient(jwt_token)

        # Update client for all toolkits that depend on BackendClient
        for tool in self._agent.tools:
            if hasattr(tool, 'client') and isinstance(tool.client, BackendClient):
                tool.client = new_client

    async def run(
        self,
        message: str,
        jwt_token: str,
        session_id: str,
        account_id: str | None = None,
    ):
        """
        Run the agent with a new message.

        This method:
        1. Updates the BackendClient JWT token for all toolkits
        2. Sets the session_id for this conversation
        3. Runs the agent with the message

        Args:
            message: User's message
            jwt_token: JWT token for backend authentication
            session_id: Session ID for conversation state
            account_id: Optional account ID for context

        Returns:
            Agent response
        """
        if self._agent is None:
            raise RuntimeError("Agent not initialized. Call initialize() first.")

        # Update JWT token for all backend toolkits
        self._update_toolkit_clients(jwt_token)

        # Set session_id for this run (Agno will load state from DB)
        self._agent.session_id = session_id

        # Run the agent
        response = await self._agent.arun(message)

        return response


# Global singleton instance
agent_manager = AgentManager()
