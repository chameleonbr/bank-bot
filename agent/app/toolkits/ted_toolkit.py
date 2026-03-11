"""TEDToolkit — tools for TED bank transfers."""

from agno.tools import Toolkit
from agno.run import RunContext
from app.client.backend_client import BackendClient


class TEDToolkit(Toolkit):
    def __init__(self, client: BackendClient):
        super().__init__(name="ted_toolkit")
        self.client = client
        self.register(self.ted_transfer)
        self.register(self.ted_schedule)
        self.register(self.validate_ted_dest)
        self.register(self.get_ted_receipt)
        self.register(self.get_ted_limits)
        self.register(self.list_banks)

    async def validate_ted_dest(self, bank_code: str, agency: str, account_number: str, cpf_cnpj: str) -> dict:
        """Validates recipient's bank details before the TED transfer."""
        return await self.client.validate_ted_dest({"bank_code": bank_code, "agency": agency, "account_number": account_number, "cpf_cnpj": cpf_cnpj})

    async def ted_transfer(self, run_context: RunContext, bank_code: str, agency: str, account_number: str, cpf_cnpj: str, amount: float) -> str:
        """
        Prepares or executes an immediate TED transfer.
        If the operation is already confirmed in pending_operation, it is executed.
        Otherwise, it saves the data in the session and asks the user for confirmation.
        """
        state = run_context.session_state
        pending = state.get("pending_operation")

        if pending and pending.get("type") == "ted" and pending.get("status") == "confirmed":
            result = await self.client.ted_transfer({
                "bank_code": pending.get("bank_code"),
                "agency": pending.get("agency"),
                "account_number": pending.get("account_number"),
                "cpf_cnpj": pending.get("cpf_cnpj"),
                "amount": pending.get("amount")
            })
            state["pending_operation"] = None
            return f"TED performed successfully. Receipt/Details: {result}"

        state["pending_operation"] = {
            "type": "ted",
            "bank_code": bank_code,
            "agency": agency,
            "account_number": account_number,
            "cpf_cnpj": cpf_cnpj,
            "amount": amount,
            "status": "pending_confirmation"
        }

        try:
            val_result = await self.client.validate_ted_dest({
                "bank_code": bank_code, "agency": agency, "account_number": account_number, "cpf_cnpj": cpf_cnpj
            })
            receiver_name = val_result.get("name", "Unknown")
            return (f"TED operation prepared for {receiver_name} (Bank {bank_code}, Ag {agency}, CC {account_number}). "
                    f"Amount: R$ {amount:.2f}. Please ask the user to confirm the operation.")
        except Exception:
            return (f"TED operation prepared in the amount of R$ {amount:.2f}. "
                    f"Please ask the user to confirm the operation.")

    async def ted_schedule(self, run_context: RunContext, bank_code: str, agency: str, account_number: str, cpf_cnpj: str, amount: float, schedule_date: str) -> str:
        """
        Prepares or executes TED scheduling.
        """
        state = run_context.session_state
        pending = state.get("pending_operation")

        if pending and pending.get("type") == "ted_schedule" and pending.get("status") == "confirmed":
            result = await self.client.ted_schedule({
                "bank_code": pending.get("bank_code"),
                "agency": pending.get("agency"),
                "account_number": pending.get("account_number"),
                "cpf_cnpj": pending.get("cpf_cnpj"),
                "amount": pending.get("amount"),
                "schedule_date": pending.get("schedule_date")
            })
            state["pending_operation"] = None
            return f"TED scheduling performed successfully: {result}"

        state["pending_operation"] = {
            "type": "ted_schedule",
            "bank_code": bank_code,
            "agency": agency,
            "account_number": account_number,
            "cpf_cnpj": cpf_cnpj,
            "amount": amount,
            "schedule_date": schedule_date,
            "status": "pending_confirmation"
        }
        return (f"TED scheduling prepared for {schedule_date} in the amount of R$ {amount:.2f}. "
                f"Please ask the user to confirm clearly.")

    async def get_ted_receipt(self, transaction_id: str) -> dict:
        """Generates TED receipt."""
        return await self.client.get_ted_receipt(transaction_id)

    async def get_ted_limits(self) -> dict:
        """Returns TED limits per period."""
        return await self.client.get_ted_limits()

    async def list_banks(self, search_term: str = "") -> list:
        """Lists available banks with ISPB code. Use search_term to filter."""
        return await self.client.list_banks(search=search_term or None)
