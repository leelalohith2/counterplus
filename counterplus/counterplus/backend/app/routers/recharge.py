from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas, security
from ..database import get_db
from ..providers import get_recharge_provider

router = APIRouter(prefix="/api", tags=["recharge"])

VALID_TYPES = {"mobile_recharge", "dth_recharge", "bill_payment"}

OPERATORS = {
    "mobile_recharge": ["Airtel", "Jio", "Vi", "BSNL"],
    "dth_recharge": ["Tata Play", "Dish TV", "Airtel Digital TV", "Sun Direct"],
    "bill_payment": ["Electricity Board", "Water Board", "Piped Gas", "Broadband"],
}


@router.get("/operators")
def list_operators():
    return OPERATORS


@router.post("/recharge", response_model=schemas.TransactionOut)
def recharge(
    payload: schemas.RechargeRequest,
    user: models.User = Depends(security.get_current_user),
    db: Session = Depends(get_db),
):
    if payload.type not in VALID_TYPES:
        raise HTTPException(status_code=400, detail="Invalid transaction type")

    if user.wallet_balance < payload.amount:
        raise HTTPException(status_code=402, detail="Insufficient wallet balance")

    # Debit first (pessimistic), refund automatically if the provider fails.
    user.wallet_balance -= payload.amount

    txn = models.Transaction(
        user_id=user.id,
        type=models.TxnType(payload.type),
        operator=payload.operator,
        account_number=payload.account_number,
        amount=payload.amount,
        status=models.TxnStatus.pending,
    )
    db.add(txn)
    db.flush()  # get txn.id without committing yet

    provider = get_recharge_provider()
    result = provider.do_recharge(payload.type, payload.operator, payload.account_number, payload.amount)

    txn.provider_ref = result.provider_ref
    txn.note = result.message

    if result.success:
        txn.status = models.TxnStatus.success
    else:
        txn.status = models.TxnStatus.failed
        user.wallet_balance += payload.amount  # refund

    txn.balance_after = user.wallet_balance
    db.commit()
    db.refresh(txn)

    if not result.success:
        raise HTTPException(status_code=502, detail=result.message)

    return txn
