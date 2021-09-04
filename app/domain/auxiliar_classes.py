"""Auxiliar classes"""
from dataclasses import dataclass
from datetime import date, datetime
import enum
from typing import Dict


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

    def convert_to_dict(self) -> Dict:
        return {
            "id": self.debt.id,
            "amount": self.debt.amount,
            "is_in_payment_plan": self.is_in_payment_plan,
            "remaining_amount": self.remaining_amount,
            "next_payment_due_date": self._convert_date_to_string()
        }

    def _convert_date_to_string(self) -> str:
        if self.next_payment_due_date is None:
            return "null"
        return self.next_payment_due_date.strftime("%Y-%m-%d")


class PayFrequency(enum.Enum):
    WEEKLY = 7
    BI_WEEKLY = 14