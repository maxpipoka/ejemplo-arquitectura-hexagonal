from typing import Dict, List
from app.domain.auxiliar_classes import DebtProcessed, Payment, PaymentPlan
from app.domain.repository import ProcessedDebtRepository


class ProcessDebtsService:

    def __init__(self, repository: ProcessedDebtRepository) -> None:
        self._repository = repository


    def analize_debt(self) -> List[DebtProcessed]:
        debts_processeds = []
        debts = self._repository.get_debts()
        payment_plans = self._repository.get_payments_plans()
        payments = self._repository.get_payments()

        for actualdebt in debts:
            is_in_payment_plan = self._is_in_payment_plan(actualdebt.id, payment_plans, payments)
            processed_debt = DebtProcessed(
                debt=actualdebt,
                is_in_payment_plan=is_in_payment_plan
            )
            debts_processeds.append(processed_debt)

        return debts_processeds


    def _is_in_payment_plan(
        self, 
        actualdebt_id: int, 
        payment_plans: Dict[int, PaymentPlan], 
        payments: Dict[int, List[Payment]]
    ) -> bool:

        if self._totals_from_payments_and_payments_plans == 0:
            return False
        
        return  actualdebt_id in payment_plans

    def _totals_from_payments_and_payments_plans(
        self, 
        actualdebt_id: int, 
        payment_plans: Dict[int, PaymentPlan], 
        payments: Dict[int, List[Payment]]
    ) -> int:
        payment_plan_id = payment_plans[actualdebt_id].id
        return sum(
            amount_payment_do_it.amount 
            for amount_payment_do_it in payments[payment_plan_id]
            ) - payment_plans[actualdebt_id].amount_to_pay
