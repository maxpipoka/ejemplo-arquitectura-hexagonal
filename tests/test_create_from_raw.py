from datetime import date
from app.domain.auxiliar_classes import Debt, Payment, PaymentPlan
from app.adapter.create_from_raw import create_debts_from_raw, create_payment_plans_from_raw, create_payments_from_raw
import unittest


class TestCreateFromRaw(unittest.TestCase):

    def setUp(self) -> None:
        self.raw_debts = [
        {
            "amount": 123.46,
            "id": 0
        },
        {
            "amount": 100,
            "id": 1
        },
        {
            "amount": 4920.34,
            "id": 2
        },
        {
            "amount": 12938,
            "id": 3
        },
        {
            "amount": 9238.02,
            "id": 4
        }
    ]

        self.debts = [
            Debt(
                amount=123.46,
                id=0, 
            ),
            Debt(
                amount=100,
                id=1, 
            ),
            Debt(
                amount=4920.34,
                id=2, 
            ),
            Debt(
                amount=12938,
                id=3, 
            ),
            Debt(
                amount=9238.02,
                id=4, 
            )
        ]

        self.raw_payment_plans = [
            {
                "amount_to_pay": 102.5,
                "debt_id": 0,
                "id": 0,
                "installment_amount": 51.25,
                "installment_frequency": "WEEKLY",
                "start_date": "2020-09-28",
            },
            {
                "amount_to_pay": 100,
                "debt_id": 1,
                "id": 1,
                "installment_amount": 25,
                "installment_frequency": "WEEKLY",
                "start_date": "2020-08-01",
            },
            {
                "amount_to_pay": 4920.34,
                "debt_id": 2,
                "id": 2,
                "installment_amount": 1230.085,
                "installment_frequency": "BI_WEEKLY",
                "start_date": "2020-01-01",
            },
            {
                "amount_to_pay": 4312.67,
                "debt_id": 3,
                "id": 3,
                "installment_amount": 1230.085,
                "installment_frequency": "WEEKLY",
                "start_date": "2020-08-01",
            }
        ]

        self.payment_plans = {
            0: PaymentPlan(
                amount_to_pay=102.50,
                debt_id=0,
                id=0,
                installment_amount=51.25,
                installment_frequency="WEEKLY",
                start_date=date(2020, 9, 28),
            )
        ,
            1: PaymentPlan(
                amount_to_pay=100,
                debt_id=1,
                id=1,
                installment_amount=25,
                installment_frequency="WEEKLY",
                start_date=date(2020, 8, 1),
            )
        ,
            2: PaymentPlan(
                amount_to_pay=4920.34,
                debt_id=2,
                id=2,
                installment_amount=1230.085,
                installment_frequency="BI_WEEKLY",
                start_date=date(2020, 1, 1),
            )
        ,
            3: PaymentPlan(
                amount_to_pay=4312.67,
                debt_id=3,
                id=3,
                installment_amount=1230.085,
                installment_frequency="WEEKLY",
                start_date=date(2020, 8, 1),
            )
        }
        
        self.raw_payments = [
            {
                "amount": 51.25,
                "date": "2020-09-29",
                "payment_plan_id": 0
            },
            {
                "amount": 51.25,
                "date": "2020-10-29",
                "payment_plan_id": 0
            },
            {
                "amount": 25,
                "date": "2020-08-08",
                "payment_plan_id": 1
            },
            {
                "amount": 25,
                "date": "2020-08-08",
                "payment_plan_id": 1
            },
            {
                "amount": 4312.67,
                "date": "2020-08-08",
                "payment_plan_id": 2
            },
            {
                "amount": 1230.085,
                "date": "2020-08-01",
                "payment_plan_id": 3
            },
            {
                "amount": 1230.085,
                "date": "2020-08-08",
                "payment_plan_id": 3
            },
            {
                "amount": 1230.085,
                "date": "2020-08-15",
                "payment_plan_id": 3
            }
        ]

        self.payments = {
            0: [
                Payment(
                    amount=51.25,
                    date=date(2020, 9, 29),
                    payment_plan_id=0,
                ),
                Payment(
                    amount=51.25,
                    date=date(2020, 10, 29),
                    payment_plan_id=0,
                ),
            ],
            1: [
                Payment(
                    amount=25,
                    date=date(2020, 8, 8),
                    payment_plan_id=1,
                ),
                Payment(
                    amount=25,
                    date=date(2020, 8, 8),
                    payment_plan_id=1,
                ),
            ],
            2: [
                Payment(
                    amount=4312.67,
                    date=date(2020, 8, 8),
                    payment_plan_id=2,
                ),
            ],
            3: [
                Payment(
                    amount=1230.085,
                    date=date(2020, 8, 1),
                    payment_plan_id=3,
                ),
                Payment(
                    amount=1230.085,
                    date=date(2020, 8, 8),
                    payment_plan_id=3,
                ),
                Payment(
                    amount=1230.085,
                    date=date(2020, 8, 15),
                    payment_plan_id=3,
                ),
            ]
        }

    def test_create_debts_from_raw(self):
        debts = create_debts_from_raw(self.raw_debts)
        self.assertEqual(self.debts, debts)
    
    def test_create_payment_plans_from_raw(self):
        payment_plans = create_payment_plans_from_raw(self.raw_payment_plans)
        self.assertEqual(self.payment_plans, payment_plans)
    
    def test_create_payments_from_raw(self):
        payments = create_payments_from_raw(self.raw_payments)
        self.assertEqual(self.payments, payments)

