"""LoanToolkit — tools for long-term financing (imovel, veiculo, rural)."""

from agno.tools import Toolkit
from app.client.backend_client import BackendClient


class LoanToolkit(Toolkit):
    def __init__(self, client: BackendClient):
        super().__init__(name="loan_toolkit")
        self.client = client
        self.register(self.simulate_financing)
        self.register(self.list_active_financings)
        self.register(self.request_financing)
        self.register(self.get_financing_statement)
        self.register(self.get_next_installment)
        self.register(self.request_portability)

    async def simulate_financing(self, amount: float, entry_value: float, period_months: int, modality: str, system: str = "SAC") -> dict:
        """Simulates financing with SAC, PRICE, or MIXED tables. modality: real_estate|vehicle|rural."""
        return await self.client.simulate_financing({"amount": amount, "entry_value": entry_value, "period_months": period_months, "modality": modality, "system": system})

    async def list_active_financings(self) -> list:
        """Lists the client's active financings."""
        return await self.client.list_active_financings()

    async def request_financing(self, amount: float, entry_value: float, period_months: int, modality: str, system: str = "SAC") -> dict:
        """Initiates the financing request process."""
        return await self.client.request_financing({"amount": amount, "entry_value": entry_value, "period_months": period_months, "modality": modality, "system": system})

    async def get_financing_statement(self, financing_id: str) -> dict:
        """Detailed statement of active financing."""
        return await self.client.get_financing_statement(financing_id)

    async def get_next_installment(self, financing_id: str) -> dict:
        """Informs the date and amount of the next financing installment."""
        return await self.client.get_next_installment(financing_id)

    async def request_portability(self, financing_id: str, target_bank_code: str) -> dict:
        """Initiates financing portability request to another bank."""
        return await self.client.request_portability(financing_id, target_bank_code)
