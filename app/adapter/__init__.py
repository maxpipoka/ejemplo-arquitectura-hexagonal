import enum
import os

class ApiUrls(enum.Enum):
    DEBTS = "https://my-json-server.typicode.com/druska/trueaccord-mock-payments-api/debts"
    PAYMENT_PLANS = "https://my-json-server.typicode.com/druska/trueaccord-mock-payments-api/payment_plans"
    PAYMENTS = "https://my-json-server.typicode.com/druska/trueaccord-mock-payments-api/payments"

class CsvFiles(enum.Enum):
    _PATH = os.path.dirname(
            os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))
            )
        )

    DEBTS = _PATH + "/csv_data/debts.csv"
    PAYMENT_PLANS = _PATH + "/csv_data/payment_plans.csv"
    PAYMENTS = _PATH + "/csv_data/payments.csv"

class NotRequestOkError(Exception):
    MESSAGE = "No request Ok Error."

    def __init__(self) -> None:
        super().__init__(self.MESSAGE)


class JsonError(Exception):
    MESSAGE = "Json error."

    def __init__(self) -> None:
        super().__init__(self.MESSAGE)