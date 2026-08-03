"""
Real payment gateway adapter.

This is a STUB. Fill it in once you've signed up with a payment gateway
(e.g. Razorpay, Cashfree, PayU, Instamojo). Typical flow:

  1. create_order() calls the gateway's "create order" API, returns an
     order_id and a checkout_url or client key the frontend uses to open
     their checkout widget.
  2. The gateway calls YOUR webhook (or the frontend calls a "verify"
     endpoint) after the user pays.
  3. verify_payment() checks the signature/status against PAYMENT_WEBHOOK_SECRET
     before you credit the wallet — never credit on the frontend's word alone.

Wire this in by setting PAYMENT_MODE=live in your .env file.
"""

import hmac
import hashlib

from ..config import settings
from .base import PaymentGateway, PaymentOrder


class LivePaymentGateway(PaymentGateway):
    def __init__(self):
        if not (settings.payment_api_key and settings.payment_api_secret):
            raise RuntimeError(
                "PAYMENT_MODE=live requires PAYMENT_API_KEY and PAYMENT_API_SECRET "
                "to be set in your .env file."
            )

    def create_order(self, amount: float, user_id: int) -> PaymentOrder:
        # Example only — replace with a real call to your gateway's
        # "create order" endpoint.
        raise NotImplementedError(
            "Implement create_order() using your payment gateway's real API "
            "before switching PAYMENT_MODE to 'live'."
        )

    def verify_payment(self, order_id: str, payload: dict) -> bool:
        # Example HMAC verification pattern — adapt to your gateway's actual
        # signature scheme (field names vary by provider).
        received_sig = payload.get("signature", "")
        expected_sig = hmac.new(
            settings.payment_webhook_secret.encode(),
            order_id.encode(),
            hashlib.sha256,
        ).hexdigest()
        return hmac.compare_digest(received_sig, expected_sig)
