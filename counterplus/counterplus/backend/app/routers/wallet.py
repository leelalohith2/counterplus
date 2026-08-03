from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas, security
from ..database import get_db
from ..providers import get_payment_gateway

router = APIRouter(prefix="/api/wallet", tags=["wallet"])


@router.get("/balance")
def balance(user: models.User = Depends(security.get_current_user)):
    return {"wallet_balance": user.wallet_balance}


@router.post("/topup", response_model=schemas.TransactionOut)
def topup(
    payload: schemas.TopupRequest,
    user: models.User = Depends(security.get_current_user),
    db: Session = Depends(get_db),
):
    gateway = get_payment_gateway()
    order = gateway.create_order(payload.amount, user.id)

    # In mock mode this verifies immediately. In live mode, this endpoint
    # would instead just return the order/checkout details, and a separate
    # webhook endpoint would call verify_payment() before crediting the wallet.
    verified = gateway.verify_payment(order.order_id, {})
    if not verified:
        raise HTTPException(status_code=402, detail="Payment could not be verified")

    user.wallet_balance += payload.amount
    txn = models.Transaction(
        user_id=user.id,
        type=models.TxnType.wallet_topup,
        amount=payload.amount,
        status=models.TxnStatus.success,
        provider_ref=order.order_id,
        balance_after=user.wallet_balance,
        note="Wallet top-up",
    )
    db.add(txn)
    db.commit()
    db.refresh(txn)
    return txn
