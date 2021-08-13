from datetime import date
from typing import Dict, List, Optional
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
            next_payment_due_date = self._next_payment_due_date(actualdebt, payment_plans, payments, is_in_payment_plan)
            processed_debt = DebtProcessed(
                debt=actualdebt,
                is_in_payment_plan=is_in_payment_plan,
                remaining_amount=remaining_amount,
                next_payment_due_date=next_payment_due_date,
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

    def _next_payment_due_date(
        self,
        actualdebt: Debt,
        payment_plans: Dict[int, PaymentPlan],
        payments: Dict[int, List[Payment]],
        is_in_payment_plan: bool,
    ) -> Optional[date]: 
        
        next_payment_due_date: Optional[date] = None
        if is_in_payment_plan == True:
            payment_plan_id = payment_plans[actualdebt.id].id
            next_payment_due_date = self._calculate_next_due_date(payment_plans[actualdebt.id], payments[payment_plan_id])

        return next_payment_due_date



    def _calculate_next_due_date(
        self,
        payment_plans: Dict[int, PaymentPlan],
        payments: Dict[int, List[Payment]],

    ) -> Date:
        date_to_return = date(2020, 8, 15)
        # order_payments = payments.sort()

        return date_to_return
# Hay que pasar el diccionario de pagos a lista en caso de plan activo
# Hay que ordenar esa lista para que al ultimo quede la ultima fecha de pago
# hay que calcular la proxima fecha de pago dependiendo la periodicidad del plan de pagos
#  