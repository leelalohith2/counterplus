from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, schemas, security
from ..database import get_db

router = APIRouter(prefix="/api/transactions", tags=["transactions"])


@router.get("", response_model=List[schemas.TransactionOut])
def list_transactions(
    user: models.User = Depends(security.get_current_user),
    db: Session = Depends(get_db),
):
    return (
        db.query(models.Transaction)
        .filter(models.Transaction.user_id == user.id)
        .order_by(models.Transaction.created_at.desc())
        .limit(200)
        .all()
    )
