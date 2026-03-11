import uuid
from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.account import Account
from app.models.investment import Investment
from app.mock.data import AVAILABLE_PRODUCTS
from app.schemas.investment import (
    InvestmentOut, PortfolioResponse, ProductOut,
    SimulateInvestmentRequest, SimulateInvestmentResponse,
    InvestRequest, RedeemRequest, InvestorProfileOut, IncomeReportOut,
)

router = APIRouter(prefix="/investments", tags=["investments"])

CDI_AA = 0.105  # 10.5% a.a. fictício
IR_BRACKETS = [(180, 0.225), (360, 0.20), (720, 0.175), (float("inf"), 0.15)]

_PROFILE_DESCRIPTIONS = {
    "conservador": "Prefere segurança e previsibilidade, aceita rentabilidades menores para preservar capital.",
    "moderado": "Equilibra segurança e rentabilidade, aceita riscos controlados em busca de maior retorno.",
    "arrojado": "Busca máxima rentabilidade, aceita volatilidade e riscos mais elevados.",
}


def _get_account(account_id: str, db: Session) -> Account:
    acc = db.get(Account, account_id)
    if not acc:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    return acc


def _calculate_ir(period_days: int, gross: float) -> float:
    rate = next(r for days, r in IR_BRACKETS if period_days <= days)
    return round(gross * rate, 2)


def _simulate(amount: float, period_days: float, rate_str: str) -> tuple[float, float]:
    """Returns (gross_return, final_value)."""
    if "CDI" in rate_str:
        pct = float(rate_str.replace("% CDI", "").replace("%CDI", "").strip()) / 100
        eff_aa = pct * CDI_AA
    elif "Selic" in rate_str or "selic" in rate_str:
        eff_aa = CDI_AA * 0.7
    elif "IPCA" in rate_str:
        eff_aa = 0.059 + 0.045  # IPCA 4.5% + taxa
    else:
        eff_aa = CDI_AA
    gross = round(amount * ((1 + eff_aa) ** (period_days / 365) - 1), 2)
    return gross, round(amount + gross, 2)


@router.get("/portfolio", response_model=PortfolioResponse)
def get_portfolio(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    _get_account(current_user["account_id"], db)
    investments = db.query(Investment).filter(
        Investment.account_id == current_user["account_id"],
        Investment.status == "active",
    ).all()
    items = []
    for inv in investments:
        profit = round(inv.current_value - inv.amount_invested, 2)
        profit_pct = round((profit / inv.amount_invested) * 100, 2) if inv.amount_invested else 0
        items.append(InvestmentOut(
            **{c.name: getattr(inv, c.name) for c in inv.__table__.columns},
            profit=profit, profit_percent=profit_pct,
        ))
    total_invested = sum(i.amount_invested for i in investments)
    total_current = sum(i.current_value for i in investments)
    profit = round(total_current - total_invested, 2)
    profit_pct = round((profit / total_invested) * 100, 2) if total_invested else 0
    return PortfolioResponse(
        account_id=current_user["account_id"],
        total_invested=total_invested, total_current=total_current,
        total_profit=profit, total_profit_percent=profit_pct, investments=items,
    )


@router.get("/products", response_model=list[ProductOut])
def list_available_products(
    risk_profile: Optional[str] = Query(None),
    min_amount: Optional[float] = Query(None),
    _: dict = Depends(get_current_user),
):
    products = AVAILABLE_PRODUCTS
    if risk_profile:
        products = [p for p in products if p["risk_profile"] == risk_profile]
    if min_amount is not None:
        products = [p for p in products if p["min_amount"] <= min_amount]
    return [ProductOut(**p) for p in products]


@router.get("/products/{product_id}", response_model=ProductOut)
def get_product_info(product_id: str, _: dict = Depends(get_current_user)):
    prod = next((p for p in AVAILABLE_PRODUCTS if p["id"] == product_id), None)
    if not prod:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return ProductOut(**prod)


@router.post("/simulate", response_model=SimulateInvestmentResponse)
def simulate_investment(payload: SimulateInvestmentRequest, _: dict = Depends(get_current_user)):
    prod = next((p for p in AVAILABLE_PRODUCTS if p["id"] == payload.product_id), None)
    if not prod:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    gross, final = _simulate(payload.amount, payload.period_days, prod["rate"])
    ir = _calculate_ir(payload.period_days, gross) if not prod["is_ir_exempt"] else 0.0
    net = round(gross - ir, 2)
    return SimulateInvestmentResponse(
        product_name=prod["name"], amount=payload.amount,
        period_days=payload.period_days, gross_return=gross,
        ir_estimate=ir, net_return=net, final_value=round(payload.amount + net, 2),
    )


@router.post("/invest", status_code=201)
def invest(
    payload: InvestRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    acc = _get_account(current_user["account_id"], db)
    prod = next((p for p in AVAILABLE_PRODUCTS if p["id"] == payload.product_id), None)
    if not prod:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    if acc.balance_checking < payload.amount:
        raise HTTPException(status_code=422, detail="Saldo insuficiente")
    acc.balance_checking -= payload.amount
    inv = Investment(
        id=f"INV{uuid.uuid4().hex[:6].upper()}",
        account_id=acc.id, product_type=prod["product_type"],
        product_name=prod["name"], amount_invested=payload.amount,
        current_value=payload.amount, rate=prod["rate"],
        start_date=datetime.now(timezone.utc),
        maturity_date=None, liquidity=prod["liquidity"], status="active",
    )
    db.add(inv)
    db.commit()
    return {"investment_id": inv.id, "status": "active", "message": f"Aplicação de R$ {payload.amount:.2f} em {prod['name']} realizada com sucesso!"}


@router.post("/redeem")
def redeem(
    payload: RedeemRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    inv = db.query(Investment).filter(
        Investment.id == payload.investment_id,
        Investment.account_id == current_user["account_id"],
        Investment.status == "active",
    ).first()
    if not inv:
        raise HTTPException(status_code=404, detail="Investimento não encontrado")
    amount = payload.amount or inv.current_value
    if amount > inv.current_value:
        raise HTTPException(status_code=422, detail="Valor de resgate superior ao disponível")
    acc = _get_account(current_user["account_id"], db)
    acc.balance_checking += amount
    inv.current_value -= amount
    if inv.current_value <= 0:
        inv.status = "redeemed"
    db.commit()
    return {"status": "success", "amount_credited": amount, "message": f"Resgate de R$ {amount:.2f} creditado na conta corrente."}


@router.get("/profile", response_model=InvestorProfileOut)
def get_investor_profile(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    acc = _get_account(current_user["account_id"], db)
    return InvestorProfileOut(
        account_id=acc.id, profile=acc.investor_profile,
        description=_PROFILE_DESCRIPTIONS.get(acc.investor_profile, ""),
    )


@router.get("/income-report/{year}", response_model=IncomeReportOut)
def get_income_report(year: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    investments = db.query(Investment).filter(Investment.account_id == current_user["account_id"]).all()
    products = []
    total_gross = total_ir = 0.0
    for inv in investments:
        gross = round(inv.current_value - inv.amount_invested, 2)
        ir = _calculate_ir(365, gross) if gross > 0 and inv.product_type not in ("LCI", "LCA", "POUPANCA") else 0
        net = round(gross - ir, 2)
        products.append({"product": inv.product_name, "type": inv.product_type, "gross": gross, "ir": ir, "net": net})
        total_gross += gross
        total_ir += ir
    return IncomeReportOut(
        year=year, account_id=current_user["account_id"],
        products=products, total_gross=round(total_gross, 2),
        total_ir=round(total_ir, 2), total_net=round(total_gross - total_ir, 2),
    )
