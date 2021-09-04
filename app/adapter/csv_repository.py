import csv
import os
from app.adapter import CsvFiles
from typing import Dict, List
from app.adapter.create_from_raw import create_debts_from_raw, create_payment_plans_from_raw, create_payments_from_raw
from app.domain.auxiliar_classes import Debt, Payment, PaymentPlan
from app.domain.repository import ProcessedDebtRepository

class CsvRepository(ProcessedDebtRepository):

    def get_debts(self) -> List[Debt]:
        """
        Return a Debts´s list.
        """
    
        return create_debts_from_raw(self._get_raw_data(CsvFiles.DEBTS.value))

    def get_payments_plans(self) -> Dict[int, PaymentPlan]:
        """
        Return a Payment_plans´s list.
        Return Dict -> {debt_id, PaymentPlan}
        """

        return create_payment_plans_from_raw(self._get_raw_data(CsvFiles.PAYMENT_PLANS.value))

    def get_payments(self) -> Dict[int, List[Payment]]:
        """
        Return a Dict with int(payment_plans id´s)
        and a list of payments of that payment plan
        """
        
        return create_payments_from_raw(self._get_raw_data(CsvFiles.PAYMENTS.value))

    def _get_raw_data(self, source: str) -> List[Dict]:
        raw_data = []
        with open(source) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                raw_data.append(row)

        return raw_data