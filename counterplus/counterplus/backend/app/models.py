import enum
from datetime import datetime

from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Enum, ForeignKey, Boolean, Text
)
from sqlalchemy.orm import relationship

from .database import Base


class KycStatus(str, enum.Enum):
    pending = "pending"
    verified = "verified"
    rejected = "rejected"


class TxnType(str, enum.Enum):
    mobile_recharge = "mobile_recharge"
    dth_recharge = "dth_recharge"
    bill_payment = "bill_payment"
    wallet_topup = "wallet_topup"


class TxnStatus(str, enum.Enum):
    pending = "pending"
    success = "success"
    failed = "failed"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    shop_name = Column(String, nullable=False)
    owner_name = Column(String, nullable=False)
    mobile = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    referral_code = Column(String, nullable=True)
    is_admin = Column(Boolean, default=False)
    kyc_status = Column(Enum(KycStatus), default=KycStatus.pending)
    wallet_balance = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    transactions = relationship("Transaction", back_populates="user")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(Enum(TxnType), nullable=False)
    operator = Column(String, nullable=True)      # e.g. "Airtel", "Tata Play"
    account_number = Column(String, nullable=True)  # mobile no. / consumer no.
    amount = Column(Float, nullable=False)
    status = Column(Enum(TxnStatus), default=TxnStatus.pending)
    provider_ref = Column(String, nullable=True)
    balance_after = Column(Float, nullable=True)
    note = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="transactions")
