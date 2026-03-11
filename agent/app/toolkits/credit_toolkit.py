"""CreditToolkit — tools for loans, credit limit and score."""

from agno.tools import Toolkit
from agno.run import RunContext
from app.client.backend_client import BackendClient


class CreditToolkit(Toolkit):
    def __init__(self, client: BackendClient):
        super().__init__(name="credit_toolkit")
        self.client = client
        self.register(self.get_credit_limit)
        self.register(self.simulate_loan)
        self.register(self.request_loan)
        self.register(self.get_loan_status)
        self.register(self.list_active_loans)
        self.register(self.get_loan_statement)
        self.register(self.anticipate_installments)
        self.register(self.get_credit_score)

    async def get_credit_limit(self) -> dict:
        """Retorna limite de crédito disponível e utilizado."""
        return await self.client.get_credit_limit()

    async def simulate_loan(self, amount: float, num_installments: int, loan_type: str = "pessoal") -> dict:
        """Simula empréstimo: parcelas, taxa mensal, taxa anual e CET."""
        return await self.client.simulate_loan({"amount": amount, "num_installments": num_installments, "loan_type": loan_type})

    async def request_loan(self, run_context: RunContext, amount: float, num_installments: int, loan_type: str = "pessoal", purpose: str = "") -> str:
        """
        Inicia solicitação de empréstimo.
        Se a operação já estiver confirmada no pending_operation, ela é executada.
        Caso contrário, salva os dados na sessão e pede confirmação ao usuário.
        """
        state = run_context.session_state
        pending = state.get("pending_operation")

        if pending and pending.get("type") == "loan_request" and pending.get("status") == "confirmed":
            result = await self.client.request_loan({
                "amount": pending.get("amount"),
                "num_installments": pending.get("num_installments"),
                "loan_type": pending.get("loan_type"),
                "purpose": pending.get("purpose")
            })
            state["pending_operation"] = None
            return f"Empréstimo solicitado com sucesso: {result}"

        state["pending_operation"] = {
            "type": "loan_request",
            "amount": amount,
            "num_installments": num_installments,
            "loan_type": loan_type,
            "purpose": purpose,
            "status": "pending_confirmation"
        }
        return (f"Solicitação de empréstimo {loan_type} preparada. Valor: R$ {amount:.2f} em {num_installments} parcelas. "
                f"Por favor, peça ao usuário para confirmar a solicitação.")

    async def get_loan_status(self, loan_id: str) -> dict:
        """Verifica status de solicitação de empréstimo em andamento."""
        return await self.client.get_loan_status(loan_id)

    async def list_active_loans(self) -> list:
        """Lista empréstimos ativos com saldo devedor."""
        return await self.client.list_active_loans()

    async def get_loan_statement(self, loan_id: str) -> dict:
        """Histórico de pagamentos de um empréstimo."""
        return await self.client.get_loan_statement(loan_id)

    async def anticipate_installments(self, loan_id: str, num_installments_to_anticipate: int) -> dict:
        """Simula e solicita antecipação de parcelas com desconto."""
        return await self.client.anticipate_installments({"loan_id": loan_id, "num_installments_to_anticipate": num_installments_to_anticipate})

    async def get_credit_score(self) -> dict:
        """Retorna score de crédito interno do cliente."""
        return await self.client.get_credit_score()
