"""Auxiliar classes"""
from dataclasses import dataclass
from datetime import date
import enum


@dataclass(frozen=True)
class Debt:
    id: int
    amount: float


@dataclass(frozen=True)
class PaymentPlan:
    id: int
    debt_id: int
    amount_to_pay: float
    installment_frequency: str
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
    remaining_amount: float
    next_payment_due_date: date


class PayFrequency(enum.Enum):
    WEEKLY = 7
    BI_WEEKLY = 14