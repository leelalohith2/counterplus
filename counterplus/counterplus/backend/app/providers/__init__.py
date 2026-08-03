from ..config import settings
from .base import RechargeProvider, PaymentGateway
from .mock_provider import MockRechargeProvider
from .mock_payment import MockPaymentGateway


def get_recharge_provider() -> RechargeProvider:
    if settings.provider_mode == "live":
        from .live_provider import LiveRechargeProvider
        return LiveRechargeProvider()
    return MockRechargeProvider()


def get_payment_gateway() -> PaymentGateway:
    if settings.payment_mode == "live":
        from .live_payment import LivePaymentGateway
        return LivePaymentGateway()
    return MockPaymentGateway()
