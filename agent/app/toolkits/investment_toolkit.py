"""InvestmentToolkit — tools for portfolio and investment operations."""

from agno.tools import Toolkit
from app.client.backend_client import BackendClient


class InvestmentToolkit(Toolkit):
    def __init__(self, client: BackendClient):
        super().__init__(name="investment_toolkit")
        self.client = client
        self.register(self.get_portfolio)
        self.register(self.get_product_info)
        self.register(self.list_available_products)
        self.register(self.simulate_investment)
        self.register(self.invest)
        self.register(self.redeem)
        self.register(self.get_investor_profile)
        self.register(self.get_income_report)

    async def get_portfolio(self) -> dict:
        """Returns the full position of the investment portfolio."""
        return await self.client.get_portfolio()

    async def get_product_info(self, product_id: str) -> dict:
        """Details a specific investment product by product_id."""
        return await self.client.get_product_info(product_id)

    async def list_available_products(self, risk_profile: str = "", min_amount: float = 0) -> list:
        """Lists available investment products filtering by profile and minimum amount."""
        params = {}
        if risk_profile: params["risk_profile"] = risk_profile
        if min_amount: params["min_amount"] = min_amount
        return await self.client.list_available_products(**params)

    async def simulate_investment(self, product_id: str, amount: float, period_days: int) -> dict:
        """Simulates the profitability of an investment with calculation of income tax and net return."""
        return await self.client.simulate_investment({"product_id": product_id, "amount": amount, "period_days": period_days})

    async def invest(self, product_id: str, amount: float) -> dict:
        """Executes an investment in a specific product."""
        return await self.client.invest(product_id, amount)

    async def redeem(self, investment_id: str, amount: float = 0) -> dict:
        """Requests investment redemption. If amount=0, redeems the total."""
        return await self.client.redeem(investment_id, amount or None)

    async def get_investor_profile(self) -> dict:
        """Returns investor profile: conservative, moderate, or aggressive."""
        return await self.client.get_investor_profile()

    async def get_income_report(self, year: int) -> dict:
        """Generates income report by year for tax declaration."""
        return await self.client.get_income_report(year)
