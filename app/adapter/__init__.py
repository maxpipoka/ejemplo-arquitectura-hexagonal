import enum

class ApiUrls(enum.Enum):
    DEBTS = "https://my-json-server.typicode.com/druska/trueaccord-mock-payments-api/debtss"
    PAYMENT_PLANS = "https://my-json-server.typicode.com/druska/trueaccord-mock-payments-api/payment_plans"
    PAYMENTS = "https://my-json-server.typicode.com/druska/trueaccord-mock-payments-api/payments"


class NotRequestOkError(Exception):
    MESSAGE = "No request Ok Error."

    def __init__(self) -> None:
        super().__init__(self.MESSAGE)


class JsonError(Exception):
    MESSAGE = "Json error."

    def __init__(self) -> None:
        super().__init__(self.MESSAGE)