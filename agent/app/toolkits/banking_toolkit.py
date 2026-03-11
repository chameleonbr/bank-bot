"""BankingToolkit — tools for account balance, statement, contacts and scheduled operations."""

from agno.tools import Toolkit
from app.client.backend_client import BackendClient


class BankingToolkit(Toolkit):
    def __init__(self, client: BackendClient):
        super().__init__(name="banking_toolkit")
        self.client = client
        self.register(self.get_balance)
        self.register(self.get_statement)
        self.register(self.get_account_info)
        self.register(self.list_contacts)
        self.register(self.add_contact)
        self.register(self.remove_contact)
        self.register(self.get_scheduled)
        self.register(self.cancel_scheduled)

    async def get_balance(self) -> dict:
        """Retorna saldo disponível, bloqueado e total da conta do usuário autenticado."""
        return await self.client.get_balance()

    async def get_statement(self, start_date: str = "", end_date: str = "", category: str = "", limit: int = 20) -> dict:
        """Busca extrato por período com filtros opcionais de categoria."""
        params = {}
        if start_date: params["start_date"] = start_date
        if end_date: params["end_date"] = end_date
        if category: params["category"] = category
        params["limit"] = limit
        return await self.client.get_statement(**params)

    async def get_account_info(self) -> dict:
        """Retorna dados cadastrais e informações da conta."""
        return await self.client.get_account_info()

    async def list_contacts(self, search_term: str = "") -> list:
        """Lista contatos salvos para transferência. Use search_term para filtrar por nome."""
        return await self.client.list_contacts(search=search_term or None)

    async def add_contact(self, name: str, cpf_cnpj: str, bank: str = "", agency: str = "", account_number: str = "", pix_key: str = "") -> dict:
        """Adiciona novo contato à agenda bancária."""
        return await self.client.add_contact({"name": name, "cpf_cnpj": cpf_cnpj, "bank": bank, "agency": agency, "account_number": account_number, "pix_key": pix_key})

    async def remove_contact(self, contact_id: str) -> dict:
        """Remove contato da agenda bancária pelo contact_id."""
        return await self.client.remove_contact(contact_id)

    async def get_scheduled(self, date_from: str = "", date_to: str = "") -> list:
        """Lista transferências e pagamentos agendados."""
        params = {}
        if date_from: params["date_from"] = date_from
        if date_to: params["date_to"] = date_to
        return await self.client.get_scheduled(**params)

    async def cancel_scheduled(self, schedule_id: str) -> dict:
        """Cancela uma operação agendada pelo schedule_id."""
        return await self.client.cancel_scheduled(schedule_id)
