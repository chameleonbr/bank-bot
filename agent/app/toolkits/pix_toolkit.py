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
        """Valida uma chave PIX e retorna os dados do recebedor."""
        try:
            return await self.client.validate_pix_key(pix_key)
        except Exception as e:
            return {"name": "Destinatário Validação Mockada", "masked_document": "***.***.***-**", "bank": "Banco Mock S.A."}

    async def pix_transfer(self, run_context: RunContext, pix_key: str, amount: float, description: str = "") -> str:
        """
        Prepara ou executa uma transferência PIX imediata.
        Se a operação já estiver confirmada no pending_operation, ela é executada.
        Caso contrário, salva os dados na sessão e pede confirmação ao usuário.
        """
        state = run_context.session_state
        pending = state.get("pending_operation")

        # Se já existe uma operação do tipo pix pendente e confirmada
        if pending and pending.get("type") == "pix" and pending.get("status") == "confirmed":
            # Executa de fato
            result = await self.client.pix_transfer(
                pending.get("pix_key"), pending.get("amount"), pending.get("description", "")
            )
            # Limpa estado
            state["pending_operation"] = None
            return f"Transferência realizada com sucesso: {result}"

        # Caso contrário, apenas prepara a operação e salva no estado
        state["pending_operation"] = {
            "type": "pix",
            "pix_key": pix_key,
            "amount": amount,
            "description": description,
            "status": "pending_confirmation"
        }
        
        # Opcional: Validar a chave PIX antes de pedir confirmação para mostrar o recebedor
        try:
            receiver_info = await self.client.validate_pix_key(pix_key)
            receiver_name = receiver_info.get("name", "Desconhecido")
            masked_document = receiver_info.get("masked_document", "")
            return (f"Operação PIX preparada. Recebedor: {receiver_name} ({masked_document}). "
                    f"Valor: R$ {amount:.2f}. Por favor, peça ao usuário para confirmar a operação.")
        except Exception:
            return (f"Operação PIX preparada para a chave {pix_key} no valor de R$ {amount:.2f}. "
                    f"Por favor, peça ao usuário para confirmar a operação.")

    async def pix_schedule(self, run_context: RunContext, pix_key: str, amount: float, schedule_datetime: str, recurrence: str = "none") -> str:
        """
        Prepara ou executa um agendamento de PIX.
        Salva no estado aguardando confirmação.
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
            return f"Agendamento realizado com sucesso: {result}"

        state["pending_operation"] = {
            "type": "pix_schedule",
            "pix_key": pix_key,
            "amount": amount,
            "schedule_datetime": schedule_datetime,
            "recurrence": recurrence,
            "status": "pending_confirmation"
        }
        return (f"Agendamento de PIX preparado para {schedule_datetime} no valor de R$ {amount:.2f}. "
                f"Por favor, peça ao usuário para confirmar.")

    async def get_pix_keys(self) -> list:
        """Lista chaves PIX registradas na conta."""
        return await self.client.get_pix_keys()

    async def register_pix_key(self, key_type: str, key_value: str = "") -> dict:
        """Registra nova chave PIX. key_type: cpf|cnpj|email|phone|random."""
        return await self.client.register_pix_key(key_type, key_value)

    async def delete_pix_key(self, pix_key_id: str) -> dict:
        """Remove chave PIX registrada pelo ID."""
        return await self.client.delete_pix_key(pix_key_id)

    async def get_pix_limits(self) -> dict:
        """Retorna os limites de transferência PIX (diurno e noturno)."""
        return await self.client.get_pix_limits()

    async def update_pix_limit(self, new_limit_daytime: float, new_limit_nighttime: float) -> dict:
        """Solicita alteração de limite PIX."""
        return await self.client.update_pix_limit(new_limit_daytime, new_limit_nighttime)

    async def get_pix_receipt(self, transaction_id: str) -> dict:
        """Gera comprovante de transação PIX."""
        return await self.client.get_pix_receipt(transaction_id)
