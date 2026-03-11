"""SupportToolkit — tools for support tickets, manager communication and escalation."""

from agno.tools import Toolkit
from app.client.backend_client import BackendClient


class SupportToolkit(Toolkit):
    def __init__(self, client: BackendClient):
        super().__init__(name="support_toolkit")
        self.client = client
        self.register(self.open_ticket)
        self.register(self.get_ticket_status)
        self.register(self.list_open_tickets)
        self.register(self.schedule_manager_call)
        self.register(self.send_message_to_manager)
        self.register(self.get_manager_info)
        self.register(self.escalate_to_human)
        self.register(self.get_faq)
        self.register(self.get_branch_info)

    async def open_ticket(self, category: str, description: str, priority: str = "normal") -> dict:
        """Abre chamado de suporte. priority: low|normal|high|urgent."""
        return await self.client.open_ticket({"category": category, "description": description, "priority": priority})

    async def get_ticket_status(self, ticket_id: str) -> dict:
        """Consulta status de chamado aberto pelo ticket_id."""
        return await self.client.get_ticket_status(ticket_id)

    async def list_open_tickets(self) -> list:
        """Lista todos os chamados abertos do cliente."""
        return await self.client.list_open_tickets()

    async def schedule_manager_call(self, preferred_date: str, preferred_time: str, subject: str) -> dict:
        """Agenda ligação com gerente. preferred_date: YYYY-MM-DD, preferred_time: HH:MM."""
        return await self.client.schedule_manager_call({"preferred_date": preferred_date, "preferred_time": preferred_time, "subject": subject})

    async def send_message_to_manager(self, message: str, category: str = "geral") -> dict:
        """Envia mensagem assíncrona ao gerente. Retorno em até 1 dia útil."""
        return await self.client.send_message_to_manager({"message": message, "category": category})

    async def get_manager_info(self) -> dict:
        """Retorna dados de contato do gerente responsável pela conta."""
        return await self.client.get_manager_info()

    async def escalate_to_human(self, reason: str, priority: str = "normal") -> dict:
        """Escala conversa para atendente humano. Disponível seg–sex, 8h–20h."""
        return await self.client.escalate_to_human({"reason": reason, "priority": priority})

    async def get_faq(self, query: str, category: str = "") -> dict:
        """Busca resposta na base de conhecimento/FAQ."""
        return await self.client.get_faq(query, category or None)

    async def get_branch_info(self) -> dict:
        """Informa agência responsável, endereço e horários."""
        return await self.client.get_branch_info()
