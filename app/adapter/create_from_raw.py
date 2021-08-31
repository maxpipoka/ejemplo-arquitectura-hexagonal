from datetime import date, datetime
from typing import List, Dict
from app.domain.auxiliar_classes import Debt, PaymentPlan, Payment


def create_debts_from_raw(raw_debts: List[Dict]) -> List[Debt]:
    # [{"amount": float, "id": int},{"amount": float, "id": int}]
    return [
        Debt(id=raw_debt["id"], amount=raw_debt["amount"]) for raw_debt in raw_debts
    ]

def create_payment_plans_from_raw(raw_payment_plans: List[Dict]) -> Dict[int, PaymentPlan]:
    payment_plans_b = {}
    for payment_plan in raw_payment_plans:
        payment_plans_b[payment_plan["debt_id"]] = PaymentPlan(
            id=payment_plan["id"],
            debt_id=payment_plan["debt_id"],
            amount_to_pay=payment_plan["amount_to_pay"],
            installment_frequency=payment_plan["installment_frequency"],
            installment_amount=payment_plan["installment_amount"],
            start_date=datetime.strptime(payment_plan['start_date'], '%Y-%m-%d').date()
        )
    return payment_plans_b

def create_payments_from_raw(raw_payments: List[Dict]) -> Dict[int, List[Payment]]:
    payments = {}
    for payment_raw in raw_payments:
        if payment_raw["payment_plan_id"] in payments:
            continue
        payments[payment_raw["payment_plan_id"]] = [
            Payment(
                payment_plan_id=x["payment_plan_id"],
                amount=x["amount"],
                date=datetime.strptime(x['date'], '%Y-%m-%d').date(),
            ) for x in raw_payments if x["payment_plan_id"] == payment_raw["payment_plan_id"]
        ]
    return payments


