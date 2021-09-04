import requests
from app.adapter.create_from_raw import create_debts_from_raw, create_payment_plans_from_raw, create_payments_from_raw
from app.adapter import ApiUrls, JsonError, NotRequestOkError

from typing import List, Dict

from requests.api import request
from app.domain.auxiliar_classes import Debt, PaymentPlan, Payment
from app.domain.repository import ProcessedDebtRepository


class ApiRepository(ProcessedDebtRepository):

    def get_debts(self) -> List[Debt]:
        """
        Return a Debts´s list.
        """
        # print(ApiUrls.DEBTS.value)
        # exit()
        return create_debts_from_raw(self._get_raw_data(ApiUrls.DEBTS.value))

    def get_payments_plans(self) -> Dict[int, PaymentPlan]:
        """
        Return a Payment_plans´s list.
        Return Dict -> {debt_id, PaymentPlan}
        """
        
        return create_payment_plans_from_raw(self._get_raw_data(ApiUrls.PAYMENT_PLANS.value))

    def get_payments(self) -> Dict[int, List[Payment]]:
        """
        Return a Dict with int(payment_plans id´s)
        and a list of payments of that payment plan
        """
        
        return create_payments_from_raw(self._get_raw_data(ApiUrls.PAYMENTS.value))

    def _get_raw_data(self, source: str) -> List[Dict]:
        request = requests.get(source, timeout=5, verify=True)

        if not request.ok: 
            raise NotRequestOkError
        
        try:
            return request.json()
        except ValueError:
            raise JsonError

        # VER SI EL REQUEST ESTA CORRECTO
        # SI NO ESTA CORRECTO, TOMAR UNA ACCION.