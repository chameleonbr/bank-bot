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
        """Returns the available and utilized credit limit."""
        return await self.client.get_credit_limit()

    async def simulate_loan(self, amount: float, num_installments: int, loan_type: str = "personal") -> dict:
        """Simulates a loan: installments, monthly rate, annual rate, and total effective cost (CET)."""
        return await self.client.simulate_loan({"amount": amount, "num_installments": num_installments, "loan_type": loan_type})

    async def request_loan(self, run_context: RunContext, amount: float, num_installments: int, loan_type: str = "personal", purpose: str = "") -> str:
        """
        Initiates a loan request.
        If the operation is already confirmed in pending_operation, it is executed.
        Otherwise, it saves the data in the session and asks the user for confirmation.
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
            return f"Loan requested successfully: {result}"

        state["pending_operation"] = {
            "type": "loan_request",
            "amount": amount,
            "num_installments": num_installments,
            "loan_type": loan_type,
            "purpose": purpose,
            "status": "pending_confirmation"
        }
        return (f"{loan_type.capitalize()} loan request prepared. Amount: R$ {amount:.2f} in {num_installments} installments. "
                f"Please ask the user to confirm the request.")

    async def get_loan_status(self, loan_id: str) -> dict:
        """Checks the status of an ongoing loan request."""
        return await self.client.get_loan_status(loan_id)

    async def list_active_loans(self) -> list:
        """Lists active loans with outstanding balance."""
        return await self.client.list_active_loans()

    async def get_loan_statement(self, loan_id: str) -> dict:
        """Payment history of a loan."""
        return await self.client.get_loan_statement(loan_id)

    async def anticipate_installments(self, loan_id: str, num_installments_to_anticipate: int) -> dict:
        """Simulates and requests installment anticipation with a discount."""
        return await self.client.anticipate_installments({"loan_id": loan_id, "num_installments_to_anticipate": num_installments_to_anticipate})

    async def get_credit_score(self) -> dict:
        """Returns the client's internal credit score."""
        return await self.client.get_credit_score()
