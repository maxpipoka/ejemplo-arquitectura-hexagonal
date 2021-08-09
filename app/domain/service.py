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

        return  actualdebt_id in payment_plans
