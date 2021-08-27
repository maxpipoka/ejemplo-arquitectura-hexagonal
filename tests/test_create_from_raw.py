from app.domain.auxiliar_classes import Debt
from app.adapter.create_from_raw import create_debts_from_raw
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

    def test_create_debts_from_raw(self):

        debts = create_debts_from_raw(self.raw_debts)

        self.assertEqual(self.debts, debts)

