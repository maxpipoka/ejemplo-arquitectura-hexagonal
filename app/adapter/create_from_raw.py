from typing import List, Dict
from app.domain.auxiliar_classes import Debt, PaymentPlan, Payment


def create_debts_from_raw(raw_debts: List[Dict]) -> List[Debt]:
    