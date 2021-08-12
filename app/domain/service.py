from typing import Dict, List
from app.domain.auxiliar_classes import Debt, DebtProcessed, Payment, PaymentPlan
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
            remaining_amount = self._remaining_amount(actualdebt, payment_plans, payments)
            is_in_payment_plan = self._is_in_payment_plan(actualdebt.id, payment_plans, remaining_amount)
            processed_debt = DebtProcessed(
                debt=actualdebt,
                is_in_payment_plan=is_in_payment_plan,
                remaining_amount=remaining_amount,
            )
            debts_processeds.append(processed_debt)

        return debts_processeds


    def _is_in_payment_plan(
        self, 
        actualdebt_id: int, 
        payment_plans: Dict[int, PaymentPlan], 
        remaining_amount: float,
    ) -> bool:
        
        if remaining_amount == 0:
                return False
            
        return  actualdebt_id in payment_plans


    def _remaining_amount(
        self, 
        actualdebt: Debt, 
        payment_plans: Dict[int, PaymentPlan], 
        payments: Dict[int, List[Payment]],
    ) -> float:

        remaining_amount = actualdebt.amount
        
        if actualdebt.id in payment_plans:
            remaining_amount = payment_plans[actualdebt.id].amount_to_pay
            payment_plan_id = payment_plans[actualdebt.id].id

            if  payment_plan_id in payments:   
                remaining_amount = payment_plans[actualdebt.id].amount_to_pay - sum(
                    amount_payment_do_it.amount 
                    for amount_payment_do_it in payments[payment_plan_id]
                )

        return remaining_amount

    
