"""Auxiliar classes"""
from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Debt:
    id: int
    amount: float


@dataclass(frozen=True)
class PaymentPlan:
    id: int
    debt_id: int
    amount_to_pay: float
    installment_frecuency: str
    installment_amount: float
    start_date: date


@dataclass(frozen=True)
class Payment:
    payment_plan_id: int
    amount: float
    date: date


@dataclass(frozen=True)
class DebtProcessed:
    debt: Debt 
    is_in_payment_plan: bool