import uuid

from .base import PaymentGateway, PaymentOrder


class MockPaymentGateway(PaymentGateway):
    """
    Simulates a payment gateway order + confirmation. No real money moves.
    In mock mode, verify_payment() always succeeds so the app can be tested
    end-to-end without a merchant account.
    """

    def create_order(self, amount: float, user_id: int) -> PaymentOrder:
        order_id = f"MOCKPAY-{uuid.uuid4().hex[:10].upper()}"
        return PaymentOrder(order_id=order_id, amount=amount, checkout_url=None)

    def verify_payment(self, order_id: str, payload: dict) -> bool:
        return True
