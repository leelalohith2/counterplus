from abc import ABC, abstractmethod
from typing import Optional
from dataclasses import dataclass


@dataclass
class RechargeResult:
    success: bool
    provider_ref: str
    message: str


@dataclass
class PaymentOrder:
    order_id: str
    amount: float
    checkout_url: Optional[str] = None


class RechargeProvider(ABC):
    """Interface every recharge/BBPS provider adapter must implement."""

    @abstractmethod
    def do_recharge(self, txn_type: str, operator: str, account_number: str, amount: float) -> RechargeResult:
        ...


class PaymentGateway(ABC):
    """Interface every payment gateway adapter must implement."""

    @abstractmethod
    def create_order(self, amount: float, user_id: int) -> PaymentOrder:
        ...

    @abstractmethod
    def verify_payment(self, order_id: str, payload: dict) -> bool:
        ...
