from app.adapter import ApiUrls
import requests

from typing import List, Dict

from requests.api import request
from app.domain.auxiliar_classes import Debt, PaymentPlan, Payment
from app.domain.repository import ProcessedDebtRepository


class ApiRepository(ProcessedDebtRepository):

    def get_debts(self) -> List[Debt]:
        """
        Return a Debts´s list.
        """
        # DRY
        raw_debts = self._get_raw_data(ApiUrls.DEBTS.value)

        debts = []

        for debt in raw_debts:
            debts.append(Debt(
                    id=debt["id"] ,
                    amount=debt["amount"],
                )
            )
        
        return debts


        temporary_debts = debt_object for debt_object in request

        # SI ESTA CORRECTO, PROCESARLO PARA DARLE EL FORMATO DE Debt.

    def get_payments_plans(self) -> Dict[int, PaymentPlan]:
        """
        Return a Payment_plans´s list.
        Return Dict -> {debt_id, PaymentPlan}
        """

        request = self._get_raw_data(ApiUrls.PAYMENT_PLANS.value)

        # SI ESTA CORRECTO, PROCESARLO PARA DARLE EL FORMATO DE Payment_plan.

    def get_payments(self) -> Dict[int, List[Payment]]:
        """
        Return a Dict with int(payment_plans id´s)
        and a list of payments of that payment plan
        """

        request = self._get_raw_data(ApiUrls.PAYMENTS.value)

        # SI ESTA CORRECTO, PROCESARLO PARA DARLE EL FORMATO DE Payment.

    def _get_raw_data(source: str) -> List[Dict]:
        request = requests.get(source, timeout=5, verify=True)

        if not request.ok: 
            pass 
            # LANZAR EXCEPTION
        
        try:
            return request.json()
        except ValueError:
            pass
            # LANZAR UNA EXCEPTION

        # VER SI EL REQUEST ESTA CORRECTO
        # SI NO ESTA CORRECTO, TOMAR UNA ACCION.