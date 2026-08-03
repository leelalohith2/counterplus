import random
import uuid

from .base import RechargeProvider, RechargeResult


class MockRechargeProvider(RechargeProvider):
    """
    Simulates a real BBPS/recharge aggregator: returns success most of the
    time, with a small realistic failure rate, and a fake provider reference.
    No real money or network calls are involved.
    """

    FAILURE_RATE = 0.06

    def do_recharge(self, txn_type: str, operator: str, account_number: str, amount: float) -> RechargeResult:
        ref = f"MOCK-{uuid.uuid4().hex[:10].upper()}"
        if random.random() < self.FAILURE_RATE:
            return RechargeResult(
                success=False,
                provider_ref=ref,
                message=f"Simulated failure from {operator} gateway (mock mode).",
            )
        return RechargeResult(
            success=True,
            provider_ref=ref,
            message=f"{txn_type.replace('_', ' ').title()} of ₹{amount:.2f} to {account_number} "
                    f"via {operator} completed (mock mode).",
        )
