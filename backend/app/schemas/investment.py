from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class InvestmentOut(BaseModel):
    id: str
    product_type: str
    product_name: str
    amount_invested: float
    current_value: float
    profit: float
    profit_percent: float
    rate: str
    start_date: datetime
    maturity_date: Optional[datetime]
    liquidity: str
    status: str

    model_config = {"from_attributes": True}


class PortfolioResponse(BaseModel):
    account_id: str
    total_invested: float
    total_current: float
    total_profit: float
    total_profit_percent: float
    investments: List[InvestmentOut]


class ProductOut(BaseModel):
    id: str
    product_type: str
    name: str
    rate: str
    min_amount: float
    period_days: int
    liquidity: str
    risk_profile: str
    is_ir_exempt: bool


class SimulateInvestmentRequest(BaseModel):
    product_id: str
    amount: float
    period_days: int


class SimulateInvestmentResponse(BaseModel):
    product_name: str
    amount: float
    period_days: int
    gross_return: float
    ir_estimate: float
    net_return: float
    final_value: float


class InvestRequest(BaseModel):
    product_id: str
    amount: float


class RedeemRequest(BaseModel):
    investment_id: str
    amount: Optional[float] = None  # None = total


class InvestorProfileOut(BaseModel):
    account_id: str
    profile: str
    description: str


class IncomeReportOut(BaseModel):
    year: int
    account_id: str
    products: List[dict]
    total_gross: float
    total_ir: float
    total_net: float
