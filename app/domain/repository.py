from abc import ABC, abstractmethod
from typing import Dict, List

from app.domain.auxiliar_classes import Debt, Payment, PaymentPlan


class ProcessedDebtRepository(ABC):

    @abstractmethod
    def get_debts(self) -> List[Debt]:
        """Return a Debts´s list"""

    @abstractmethod
    def get_payments_plans(self) -> Dict[int, PaymentPlan]:
        """Return a Payment_plans´s list
        Return Dict -> {debt_id, PaymentPlan}
        """

    @abstractmethod
    def get_payments(self) -> Dict[int, List[Payment]]:
        """Return a Dict with int(payment_plans id´s)
        and a list of payments of that payment plan"""
        



