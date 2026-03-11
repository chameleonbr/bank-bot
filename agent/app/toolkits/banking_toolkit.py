"""BankingToolkit — tools for account balance, statement, contacts and scheduled operations."""

from agno.tools import Toolkit
from agno.run import RunContext
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
        self.register(self.generate_statement_pdf)

    async def get_balance(self) -> dict:
        """Returns the available, blocked, and total balance for the authenticated account."""
        return await self.client.get_balance()

    async def get_statement(self, start_date: str = "", end_date: str = "", category: str = "", limit: int = 20) -> dict:
        """Fetches the account statement by period with optional category filters."""
        params = {}
        if start_date: params["start_date"] = start_date
        if end_date: params["end_date"] = end_date
        if category: params["category"] = category
        params["limit"] = limit
        return await self.client.get_statement(**params)

    async def get_account_info(self) -> dict:
        """Returns registration and account details."""
        return await self.client.get_account_info()

    async def list_contacts(self, search_term: str = "") -> list:
        """Lists saved contacts for transfers. Use search_term to filter by name."""
        return await self.client.list_contacts(search=search_term or None)

    async def add_contact(self, name: str, cpf_cnpj: str, bank: str = "", agency: str = "", account_number: str = "", pix_key: str = "") -> dict:
        """Adds a new contact to the banking agenda."""
        return await self.client.add_contact({"name": name, "cpf_cnpj": cpf_cnpj, "bank": bank, "agency": agency, "account_number": account_number, "pix_key": pix_key})

    async def remove_contact(self, contact_id: str) -> dict:
        """Removes a contact from the banking agenda by contact_id."""
        return await self.client.remove_contact(contact_id)

    async def get_scheduled(self, date_from: str = "", date_to: str = "") -> list:
        """Lists scheduled transfers and payments."""
        params = {}
        if date_from: params["date_from"] = date_from
        if date_to: params["date_to"] = date_to
        return await self.client.get_scheduled(**params)

    async def cancel_scheduled(self, schedule_id: str) -> dict:
        """Cancels a scheduled operation by schedule_id."""
        return await self.client.cancel_scheduled(schedule_id)

    async def generate_statement_pdf(self, run_context: RunContext, start_date: str = "", end_date: str = "") -> str:
        """Generates a PDF statement for the period and attaches it to the response."""
        try:
            file_data = await self.client.generate_statement_pdf(start_date, end_date)
            # Add to agent session state so chat API can extract it
            if "files" not in run_context.session_state:
                run_context.session_state["files"] = []
            
            run_context.session_state["files"].append({
                "content_type": file_data.get("content_type", "application/pdf"),
                "content": file_data.get("content"),
                "filename": file_data.get("filename", "statement.pdf")
            })
            return f"Statement PDF for period {start_date} to {end_date} generated successfully."
        except Exception as e:
            return f"Error generating PDF: {str(e)}"
