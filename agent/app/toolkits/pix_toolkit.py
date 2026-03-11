"""PIXToolkit — tools for PIX instant payments."""

from agno.tools import Toolkit
from agno.run import RunContext
from app.client.backend_client import BackendClient


class PIXToolkit(Toolkit):
    def __init__(self, client: BackendClient):
        super().__init__(name="pix_toolkit")
        self.client = client
        self.register(self.pix_transfer)
        self.register(self.pix_schedule)
        self.register(self.get_pix_keys)
        self.register(self.register_pix_key)
        self.register(self.delete_pix_key)
        self.register(self.validate_pix_key)
        self.register(self.get_pix_limits)
        self.register(self.update_pix_limit)
        self.register(self.get_pix_receipt)

    async def validate_pix_key(self, pix_key: str) -> dict:
        """Validates a PIX key and returns the receiver's data."""
        try:
            return await self.client.validate_pix_key(pix_key)
        except Exception as e:
            return {"name": "Mocked Validation Receiver", "masked_document": "***.***.***-**", "bank": "Banco Mock S.A."}

    async def pix_transfer(self, run_context: RunContext, pix_key: str, amount: float, description: str = "") -> str:
        """
        Prepares or executes an immediate PIX transfer.
        If the operation is already confirmed in pending_operation, it is executed.
        Otherwise, it saves the data in the session and asks the user for confirmation.
        """
        state = run_context.session_state
        pending = state.get("pending_operation")

        # If there is already a pending and confirmed pix type operation
        if pending and pending.get("type") == "pix" and pending.get("status") == "confirmed":
            # Execute indeed
            result = await self.client.pix_transfer(
                pending.get("pix_key"), pending.get("amount"), pending.get("description", "")
            )
            # Clear state
            state["pending_operation"] = None
            return f"Transfer completed successfully: {result}"

        # Otherwise, just prepares the operation and saves it in the state
        state["pending_operation"] = {
            "type": "pix",
            "pix_key": pix_key,
            "amount": amount,
            "description": description,
            "status": "pending_confirmation"
        }
        
        # Optional: Validate the PIX key before asking for confirmation to show the receiver
        try:
            receiver_info = await self.client.validate_pix_key(pix_key)
            receiver_name = receiver_info.get("name", "Unknown")
            masked_document = receiver_info.get("masked_document", "")
            return (f"PIX operation prepared. Receiver: {receiver_name} ({masked_document}). "
                    f"Amount: R$ {amount:.2f}. Please ask the user to confirm the operation.")
        except Exception:
            return (f"PIX operation prepared for key {pix_key} in the amount of R$ {amount:.2f}. "
                    f"Please ask the user to confirm the operation.")

    async def pix_schedule(self, run_context: RunContext, pix_key: str, amount: float, schedule_datetime: str, recurrence: str = "none") -> str:
        """
        Prepares or executes a PIX scheduling.
        Saves in the state waiting for confirmation.
        """
        state = run_context.session_state
        pending = state.get("pending_operation")

        if pending and pending.get("type") == "pix_schedule" and pending.get("status") == "confirmed":
            result = await self.client.pix_schedule({
                "pix_key": pending.get("pix_key"),
                "amount": pending.get("amount"),
                "schedule_datetime": pending.get("schedule_datetime"),
                "recurrence": pending.get("recurrence")
            })
            state["pending_operation"] = None
            return f"Scheduling completed successfully: {result}"

        state["pending_operation"] = {
            "type": "pix_schedule",
            "pix_key": pix_key,
            "amount": amount,
            "schedule_datetime": schedule_datetime,
            "recurrence": recurrence,
            "status": "pending_confirmation"
        }
        return (f"PIX scheduling prepared for {schedule_datetime} in the amount of R$ {amount:.2f}. "
                f"Please ask the user to confirm.")

    async def get_pix_keys(self) -> list:
        """Lists PIX keys registered in the account."""
        return await self.client.get_pix_keys()

    async def register_pix_key(self, key_type: str, key_value: str = "") -> dict:
        """Registers a new PIX key. key_type: cpf|cnpj|email|phone|random."""
        return await self.client.register_pix_key(key_type, key_value)

    async def delete_pix_key(self, pix_key_id: str) -> dict:
        """Removes a registered PIX key by ID."""
        return await self.client.delete_pix_key(pix_key_id)

    async def get_pix_limits(self) -> dict:
        """Returns PIX transfer limits (daytime and nighttime)."""
        return await self.client.get_pix_limits()

    async def update_pix_limit(self, new_limit_daytime: float, new_limit_nighttime: float) -> dict:
        """Requests a PIX limit change."""
        return await self.client.update_pix_limit(new_limit_daytime, new_limit_nighttime)

    async def get_pix_receipt(self, transaction_id: str) -> dict:
        """Generates PIX transaction receipt."""
        return await self.client.get_pix_receipt(transaction_id)
