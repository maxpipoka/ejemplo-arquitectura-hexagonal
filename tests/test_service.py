from datetime import date
from app.domain.auxiliar_classes import Debt, Payment, PaymentPlan
from app.domain.service import ProcessDebtsService
from app.domain.repository import ProcessedDebtRepository
from unittest import TestCase
import unittest
from unittest.mock import Mock


class TestPaymentPlan(unittest.TestCase):

    def setUp(self) -> None:
        self._debt_id_0 = Debt(id=0, amount=123.46)

        self._payment_plan_0 = {
            0: PaymentPlan(
                id=1,
                debt_id=0,
                amount_to_pay=123.46,
                installment_frecuency="Weekly",
                installment_amount=50.00,
                start_date=date(2021,8,10),
            )
        }


    def test_is_in_active_plan_equal_false_debts_has_not_active_payment_plan(self):
        repository = Mock(spec=ProcessedDebtRepository)

        service = ProcessDebtsService(repository=repository)

        repository.get_debts.return_value = [self._debt_id_0]
        repository.get_payments_plans.return_value = {}

        actual = service.analize_debt()

        self.assertFalse(actual[0].is_in_payment_plan)


    def test_is_in_active_plan_equal_True_debts_has_active_payment_plan(self):
        repository = Mock(spec=ProcessedDebtRepository)

        service = ProcessDebtsService(repository=repository)

        repository.get_debts.return_value = [self._debt_id_0]
        repository.get_payments_plans.return_value = self._payment_plan_0

        actual = service.analize_debt()

        self.assertTrue(actual[0].is_in_payment_plan)

    
    def test_is_in_active_plan_equal_False_debts_has_completed_payment_plan(self):
        repository = Mock(spec=ProcessedDebtRepository)

        service = ProcessDebtsService(repository=repository)

        repository.get_debts.return_value = [self._debt_id_0]
        repository.get_payments_plans.return_value = {
            0: PaymentPlan(
                id=0,
                debt_id=0,
                amount_to_pay=102.50,
                installment_frecuency="Weekly",
                installment_amount=51.25,
                start_date=date(2021,8,10),
            )
        }

        repository.get_payments.return_value = {
            0: [
                Payment(
                    payment_plan_id=0,
                    amount=51.25,
                    date=date(2020, 9, 29)
                ),
                Payment(
                    payment_plan_id=0,
                    amount=51.25,
                    date=date(2020, 10, 29)
                ),
            ]
        }

        actual = service.analize_debt()

        self.assertFalse(actual[0].is_in_payment_plan)


if __name__ == "__main__":
    unittest.main()

                