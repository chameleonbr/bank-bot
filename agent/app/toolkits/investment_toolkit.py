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
        """Retorna posição completa da carteira de investimentos."""
        return await self.client.get_portfolio()

    async def get_product_info(self, product_id: str) -> dict:
        """Detalha um produto de investimento específico pelo product_id."""
        return await self.client.get_product_info(product_id)

    async def list_available_products(self, risk_profile: str = "", min_amount: float = 0) -> list:
        """Lista produtos de investimento disponíveis filtrando por perfil e valor mínimo."""
        params = {}
        if risk_profile: params["risk_profile"] = risk_profile
        if min_amount: params["min_amount"] = min_amount
        return await self.client.list_available_products(**params)

    async def simulate_investment(self, product_id: str, amount: float, period_days: int) -> dict:
        """Simula rentabilidade de um investimento com cálculo de IR e rendimento líquido."""
        return await self.client.simulate_investment({"product_id": product_id, "amount": amount, "period_days": period_days})

    async def invest(self, product_id: str, amount: float) -> dict:
        """Executa aplicação em produto de investimento."""
        return await self.client.invest(product_id, amount)

    async def redeem(self, investment_id: str, amount: float = 0) -> dict:
        """Solicita resgate de investimento. Se amount=0, resgata o total."""
        return await self.client.redeem(investment_id, amount or None)

    async def get_investor_profile(self) -> dict:
        """Retorna perfil de investidor: conservador, moderado ou arrojado."""
        return await self.client.get_investor_profile()

    async def get_income_report(self, year: int) -> dict:
        """Gera relatório de rendimentos por ano para declaração de IR."""
        return await self.client.get_income_report(year)
