from datetime import date, timedelta
from typing import Dict, List, Optional
from app.domain.auxiliar_classes import Debt, DebtProcessed, PayFrequency, Payment, PaymentPlan
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
        if not is_in_payment_plan:
            return next_payment_due_date

        payment_plan_id = payment_plans[actualdebt.id].id

        pay = payments[payment_plan_id] if payment_plan_id in payments else []
        next_payment_due_date = self._calculate_next_due_date(payment_plans[actualdebt.id], pay)
        return next_payment_due_date



    def _calculate_next_due_date(
        self,
        payment_plan: PaymentPlan,
        payments: List[Payment],

    ) -> date:

        if len(payments) == 0:
            return payment_plan.start_date

        last_payment = max(x.date for x in payments)
        validated_date = False
        pay_frecuency_iteration = len(payments) + 1
        pay_frecuency = PayFrequency[payment_plan.installment_frecuency].value
        while (validated_date == False):
            current_payment_due = payment_plan.start_date + (timedelta(pay_frecuency  * pay_frecuency_iteration))
            if (last_payment < current_payment_due): #and ((last_payment - current_payment_due) < 7):
                return current_payment_due
            if (last_payment >= current_payment_due):
                pay_frecuency_iteration += 1


# Solucionado lo de la comparacion de pagos.
# Hay que tener en cuenta ahora la cantidad de pagos, para tambien aplicarlo a la cantidad de vencimientos

# inicia deuda:
# 2020-8-1

# primer vencimiento: 2020-8-8
# segund vencimiento: 2020-8-15
# tercer vencimiento: 2020-8-21

# el chavon hace 2 pagos el mismo dia: 2020-8-8

# Tiene cubiertos los 2 primeros vencimientos, el siguiente deberia ser el 21
# Si tomamos en cuenta solo el ultimo pago, va a informar que es el 15 el prox vencimiento

