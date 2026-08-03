from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    shop_name: str
    owner_name: str
    mobile: str = Field(min_length=10, max_length=10)
    email: EmailStr
    password: str = Field(min_length=8)
    referral_code: Optional[str] = None
    captcha_id: str
    captcha_answer: str


class LoginRequest(BaseModel):
    identifier: str  # email / mobile / user id
    password: str
    captcha_id: str
    captcha_answer: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: int
    shop_name: str
    owner_name: str
    mobile: str
    email: str
    kyc_status: str
    wallet_balance: float
    is_admin: bool

    class Config:
        from_attributes = True


class CaptchaResponse(BaseModel):
    captcha_id: str
    captcha_text: str  # returned as an image would be in production; plain text for this starter


class TopupRequest(BaseModel):
    amount: float = Field(gt=0)


class RechargeRequest(BaseModel):
    type: str  # "mobile_recharge" | "dth_recharge" | "bill_payment"
    operator: str
    account_number: str
    amount: float = Field(gt=0)


class TransactionOut(BaseModel):
    id: int
    type: str
    operator: Optional[str]
    account_number: Optional[str]
    amount: float
    status: str
    provider_ref: Optional[str]
    balance_after: Optional[float]
    created_at: datetime

    class Config:
        from_attributes = True
