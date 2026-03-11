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
        """Valida dados bancários do destinatário TED antes da transferência."""
        return await self.client.validate_ted_dest({"bank_code": bank_code, "agency": agency, "account_number": account_number, "cpf_cnpj": cpf_cnpj})

    async def ted_transfer(self, run_context: RunContext, bank_code: str, agency: str, account_number: str, cpf_cnpj: str, amount: float) -> str:
        """
        Prepara ou executa uma TED imediata.
        Se a operação já estiver confirmada no pending_operation, ela é executada.
        Caso contrário, salva os dados na sessão e pede confirmação ao usuário.
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
            return f"TED realizada com sucesso. Comprovante/Detalhes: {result}"

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
            receiver_name = val_result.get("name", "Desconhecido")
            return (f"Operação TED preparada para {receiver_name} (Banco {bank_code}, Ag {agency}, CC {account_number}). "
                    f"Valor: R$ {amount:.2f}. Por favor, peça ao usuário para confirmar a operação.")
        except Exception:
            return (f"Operação TED preparada no valor de R$ {amount:.2f}. "
                    f"Por favor, peça ao usuário para confirmar a operação.")

    async def ted_schedule(self, run_context: RunContext, bank_code: str, agency: str, account_number: str, cpf_cnpj: str, amount: float, schedule_date: str) -> str:
        """
        Prepara ou executa agendamento de TED.
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
            return f"Agendamento de TED realizado com sucesso: {result}"

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
        return (f"Agendamento de TED preparado para o dia {schedule_date} no valor de R$ {amount:.2f}. "
                f"Por favor, peça ao usuário para confirmar de forma clara.")

    async def get_ted_receipt(self, transaction_id: str) -> dict:
        """Gera comprovante de TED."""
        return await self.client.get_ted_receipt(transaction_id)

    async def get_ted_limits(self) -> dict:
        """Retorna limites de TED por período."""
        return await self.client.get_ted_limits()

    async def list_banks(self, search_term: str = "") -> list:
        """Lista bancos disponíveis com código ISPB. Use search_term para filtrar."""
        return await self.client.list_banks(search=search_term or None)
