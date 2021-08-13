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
        self._debt_id_1 = Debt(id=1, amount=100)

        self._payment_plan_0 = {
            0: PaymentPlan(
                id=0,
                debt_id=0,
                amount_to_pay=102.50,
                installment_frecuency="WEEKLY",
                installment_amount=51.25,
                start_date=date(2020,9,28),
            )
        }

        self._payment_plan_1 = {
            1: PaymentPlan(
                id=1,
                debt_id=1,
                amount_to_pay=100,
                installment_frecuency="WEEKLY",
                installment_amount=25.00,
                start_date=date(2020,8,1),
            )
        }


        self.payment_0 = {
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

        self.payment_1 = {
            1: [
                Payment(
                    payment_plan_id=1,
                    amount=25,
                    date=date(2020, 8, 8)
                ),
                Payment(
                    payment_plan_id=1,
                    amount=25,
                    date=date(2020, 8, 8)
                ),
            ]
        }


    def test_is_in_active_plan_equal_false_debts_has_not_active_payment_plan(self):
        repository = Mock(spec=ProcessedDebtRepository)

        service = ProcessDebtsService(repository=repository)

        repository.get_debts.return_value = [self._debt_id_0]
        repository.get_payments_plans.return_value = {}
        repository.get_payments.return_value = {}

        actual = service.analize_debt()

        self.assertFalse(actual[0].is_in_payment_plan)


    def test_is_in_active_plan_equal_True_debts_has_active_payment_plan(self):
        repository = Mock(spec=ProcessedDebtRepository)

        service = ProcessDebtsService(repository=repository)

        repository.get_debts.return_value = [self._debt_id_1]
        repository.get_payments_plans.return_value = self._payment_plan_1
        repository.get_payments.return_value = {}

        actual = service.analize_debt()

        self.assertTrue(actual[0].is_in_payment_plan)

    
    def test_is_in_active_plan_equal_False_debts_has_completed_payment_plan(self):
        repository = Mock(spec=ProcessedDebtRepository)

        service = ProcessDebtsService(repository=repository)

        repository.get_debts.return_value = [self._debt_id_0]
        repository.get_payments_plans.return_value = self._payment_plan_0
        repository.get_payments.return_value = self.payment_0

        actual = service.analize_debt()

        self.assertFalse(actual[0].is_in_payment_plan)


    def test_remaining_amount_equal_initial_debts_when_debts_has_not_active_payment_plan(self):
        repository = Mock(spec=ProcessedDebtRepository)

        service = ProcessDebtsService(repository=repository)

        repository.get_debts.return_value = [self._debt_id_0]
        repository.get_payments_plans.return_value = {}
        repository.get_payments.return_value = {}

        actual = service.analize_debt()

        self.assertEqual(actual[0].remaining_amount, self._debt_id_0.amount)

        
    def test_remaining_amount_equal_50_to_pay(self):
        repository = Mock(spec=ProcessedDebtRepository)

        service = ProcessDebtsService(repository=repository)

        repository.get_debts.return_value = [self._debt_id_1]
        repository.get_payments_plans.return_value = self._payment_plan_1
        repository.get_payments.return_value = self.payment_1

        actual = service.analize_debt()

        self.assertEqual(actual[0].remaining_amount, 50)


    def test_remaining_amount_debt_with_payment_plan_but_without_payments(self):
        repository = Mock(spec=ProcessedDebtRepository)

        service = ProcessDebtsService(repository=repository)

        repository.get_debts.return_value = [self._debt_id_0]
        repository.get_payments_plans.return_value = self._payment_plan_0
        repository.get_payments.return_value = {}

        actual = service.analize_debt()

        self.assertEqual(actual[0].remaining_amount, 102.50)

    
    def test_next_payment_due_date_equal_to_null_debt_with_out_payment_plan_or_debt_paid_off(self):
        repository = Mock(spec=ProcessedDebtRepository)

        service = ProcessDebtsService(repository=repository)

        repository.get_debts.return_value = [self._debt_id_0]
        repository.get_payments_plans.return_value = self._payment_plan_0
        repository.get_payments.return_value = self.payment_0

        actual = service.analize_debt()

        self.assertEqual(actual[0].next_payment_due_date, None)


    def test_next_payment_due_date_debt_with_active_payment_plan_with_payments_and_weekly_installent_frecuency(self):
        repository = Mock(spec=ProcessedDebtRepository)

        service = ProcessDebtsService(repository=repository)

        repository.get_debts.return_value = [self._debt_id_1]
        repository.get_payments_plans.return_value = self._payment_plan_1
        repository.get_payments.return_value = self.payment_1

        actual = service.analize_debt()

        self.assertEqual(actual[0].next_payment_due_date, date(2020, 8, 15))


if __name__ == "__main__":
    unittest.main()

                