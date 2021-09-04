from datetime import date, datetime
from typing import List, Dict
from app.domain.auxiliar_classes import Debt, PaymentPlan, Payment


def create_debts_from_raw(raw_debts: List[Dict]) -> List[Debt]:
    # [{"amount": float, "id": int},{"amount": float, "id": int}]
    return [
        Debt(id=int(raw_debt["id"]), amount=float(raw_debt["amount"])) for raw_debt in raw_debts
    ]

def create_payment_plans_from_raw(raw_payment_plans: List[Dict]) -> Dict[int, PaymentPlan]:
    payment_plans_b = {}
    for payment_plan in raw_payment_plans:
        payment_plans_b[int(payment_plan["debt_id"])] = PaymentPlan(
            id=int(payment_plan["id"]),
            debt_id=int(payment_plan["debt_id"]),
            amount_to_pay=float(payment_plan["amount_to_pay"]),
            installment_frequency=payment_plan["installment_frequency"],
            installment_amount=float(payment_plan["installment_amount"]),
            start_date=datetime.strptime(payment_plan['start_date'], '%Y-%m-%d').date()
        )
    return payment_plans_b

def create_payments_from_raw(raw_payments: List[Dict]) -> Dict[int, List[Payment]]:
    payments = {}
    for payment_raw in raw_payments:
        key = int(payment_raw["payment_plan_id"])
        if key in payments:
            continue
        payments[key] = [
            Payment(
                payment_plan_id=int(x["payment_plan_id"]),
                amount=float(x["amount"]),
                date=datetime.strptime(x['date'], '%Y-%m-%d').date(),
            ) for x in raw_payments if int(x["payment_plan_id"]) == key
        ]
    return payments


