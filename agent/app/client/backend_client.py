"""
Backend HTTP client.
All calls forward the user's JWT automatically — the backend re-validates it
and extracts account_id from the token payload.
"""

import httpx
from app.core.config import settings


class BackendClient:
    def __init__(self, jwt_token: str):
        self._token = jwt_token
        self._base = settings.BACKEND_URL.rstrip("/")
        self._headers = {"Authorization": f"Bearer {jwt_token}"}

    async def _get(self, path: str, params: dict | None = None) -> dict:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(f"{self._base}{path}", headers=self._headers, params=params)
            resp.raise_for_status()
            return resp.json()

    async def _post(self, path: str, body: dict | None = None) -> dict:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(f"{self._base}{path}", headers=self._headers, json=body or {})
            resp.raise_for_status()
            return resp.json()

    async def _put(self, path: str, body: dict) -> dict:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.put(f"{self._base}{path}", headers=self._headers, json=body)
            resp.raise_for_status()
            return resp.json()

    async def _delete(self, path: str) -> None:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.delete(f"{self._base}{path}", headers=self._headers)
            resp.raise_for_status()

    # ── Banking ───────────────────────────────────────────────────────────────
    async def get_balance(self): return await self._get("/banking/balance")
    async def get_account_info(self): return await self._get("/banking/account-info")
    async def get_statement(self, **params): return await self._get("/banking/statement", params)
    async def list_contacts(self, search=None): return await self._get("/banking/contacts", {"search": search} if search else None)
    async def add_contact(self, data: dict): return await self._post("/banking/contacts", data)
    async def remove_contact(self, contact_id: str): return await self._delete(f"/banking/contacts/{contact_id}")
    async def get_scheduled(self, **params): return await self._get("/banking/scheduled", params)
    async def cancel_scheduled(self, schedule_id: str): return await self._delete(f"/banking/scheduled/{schedule_id}")

    # ── PIX ───────────────────────────────────────────────────────────────────
    async def validate_pix_key(self, pix_key: str): return await self._get("/pix/validate", {"pix_key": pix_key})
    async def pix_transfer(self, pix_key: str, amount: float, description: str = ""): return await self._post("/pix/transfer", {"pix_key": pix_key, "amount": amount, "description": description})
    async def pix_schedule(self, data: dict): return await self._post("/pix/schedule", data)
    async def get_pix_keys(self): return await self._get("/pix/keys")
    async def register_pix_key(self, key_type: str, key_value: str = ""): return await self._post("/pix/keys", {"key_type": key_type, "key_value": key_value})
    async def delete_pix_key(self, pix_key_id: str): return await self._delete(f"/pix/keys/{pix_key_id}")
    async def get_pix_limits(self): return await self._get("/pix/limits")
    async def update_pix_limit(self, daytime: float, nighttime: float): return await self._put("/pix/limits", {"new_limit_daytime": daytime, "new_limit_nighttime": nighttime})
    async def get_pix_receipt(self, txn_id: str): return await self._get(f"/pix/receipt/{txn_id}")

    # ── TED ───────────────────────────────────────────────────────────────────
    async def ted_transfer(self, data: dict): return await self._post("/ted/transfer", data)
    async def ted_schedule(self, data: dict): return await self._post("/ted/schedule", data)
    async def validate_ted_dest(self, data: dict): return await self._post("/ted/validate", data)
    async def get_ted_receipt(self, txn_id: str): return await self._get(f"/ted/receipt/{txn_id}")
    async def get_ted_limits(self): return await self._get("/ted/limits")
    async def list_banks(self, search=None): return await self._get("/ted/banks", {"search": search} if search else None)

    # ── Investments ───────────────────────────────────────────────────────────
    async def get_portfolio(self): return await self._get("/investments/portfolio")
    async def get_product_info(self, pid: str): return await self._get(f"/investments/products/{pid}")
    async def list_available_products(self, **params): return await self._get("/investments/products", params)
    async def simulate_investment(self, data: dict): return await self._post("/investments/simulate", data)
    async def invest(self, product_id: str, amount: float): return await self._post("/investments/invest", {"product_id": product_id, "amount": amount})
    async def redeem(self, investment_id: str, amount=None): return await self._post("/investments/redeem", {"investment_id": investment_id, "amount": amount})
    async def get_investor_profile(self): return await self._get("/investments/profile")
    async def get_income_report(self, year: int): return await self._get(f"/investments/income-report/{year}")

    # ── Credit ────────────────────────────────────────────────────────────────
    async def get_credit_limit(self): return await self._get("/credit/limit")
    async def simulate_loan(self, data: dict): return await self._post("/credit/simulate-loan", data)
    async def request_loan(self, data: dict): return await self._post("/credit/request-loan", data)
    async def get_loan_status(self, loan_id: str): return await self._get(f"/credit/loan-status/{loan_id}")
    async def list_active_loans(self): return await self._get("/credit/loans")
    async def get_loan_statement(self, loan_id: str): return await self._get(f"/credit/loans/{loan_id}/statement")
    async def anticipate_installments(self, data: dict): return await self._post("/credit/anticipate", data)
    async def get_credit_score(self): return await self._get("/credit/score")
    async def simulate_financing(self, data: dict): return await self._post("/credit/simulate-financing", data)
    async def list_active_financings(self): return await self._get("/credit/financings")
    async def get_financing_statement(self, fin_id: str): return await self._get(f"/credit/financings/{fin_id}/statement")
    async def get_next_installment(self, fin_id: str): return await self._get(f"/credit/financings/{fin_id}/next-installment")
    async def request_financing(self, data: dict): return await self._post("/credit/financings/request", data)
    async def request_portability(self, fin_id: str, target_bank_code: str): return await self._post(f"/credit/financings/{fin_id}/portability", {"target_bank_code": target_bank_code})

    # ── Support ───────────────────────────────────────────────────────────────
    async def open_ticket(self, data: dict): return await self._post("/support/tickets", data)
    async def get_ticket_status(self, tid: str): return await self._get(f"/support/tickets/{tid}")
    async def list_open_tickets(self): return await self._get("/support/tickets")
    async def schedule_manager_call(self, data: dict): return await self._post("/support/manager/schedule", data)
    async def send_message_to_manager(self, data: dict): return await self._post("/support/manager/message", data)
    async def get_manager_info(self): return await self._get("/support/manager")
    async def escalate_to_human(self, data: dict): return await self._post("/support/escalate", data)
    async def get_faq(self, query: str, category=None): return await self._get("/support/faq", {"query": query, "category": category} if category else {"query": query})
    async def get_branch_info(self): return await self._get("/support/branch")
