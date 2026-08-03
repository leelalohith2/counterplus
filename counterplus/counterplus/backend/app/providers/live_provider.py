"""
Real BBPS / recharge aggregator adapter.

This is a STUB. Fill it in once you've signed up with a licensed
aggregator (e.g. Eko, PaySprint, Robotics Exchange, DigiPay, Setu BBPS,
NSDL Payments Bank BBPOU, etc). Every aggregator has its own request/response
format and auth scheme (API key + secret, HMAC signing, etc.) — copy their
API docs and implement do_recharge() accordingly.

Wire this in by setting PROVIDER_MODE=live in your .env file; see
app/providers/__init__.py for how the active provider is selected.
"""

import httpx

from ..config import settings
from .base import RechargeProvider, RechargeResult


class LiveRechargeProvider(RechargeProvider):
    def __init__(self):
        self.base_url = settings.bbps_api_base_url
        self.api_key = settings.bbps_api_key
        self.api_secret = settings.bbps_api_secret

        if not (self.base_url and self.api_key and self.api_secret):
            raise RuntimeError(
                "PROVIDER_MODE=live requires BBPS_API_BASE_URL, BBPS_API_KEY "
                "and BBPS_API_SECRET to be set in your .env file."
            )

    def do_recharge(self, txn_type: str, operator: str, account_number: str, amount: float) -> RechargeResult:
        # --- Example shape only. Replace with your aggregator's real
        # --- endpoint, payload, and signing scheme.
        #
        # with httpx.Client(timeout=15) as client:
        #     resp = client.post(
        #         f"{self.base_url}/recharge",
        #         headers={"Authorization": f"Bearer {self.api_key}"},
        #         json={
        #             "type": txn_type,
        #             "operator": operator,
        #             "account_number": account_number,
        #             "amount": amount,
        #         },
        #     )
        #     data = resp.json()
        #     return RechargeResult(
        #         success=data["status"] == "SUCCESS",
        #         provider_ref=data["ref_id"],
        #         message=data.get("message", ""),
        #     )
        raise NotImplementedError(
            "Implement do_recharge() using your aggregator's real API before "
            "switching PROVIDER_MODE to 'live'."
        )
