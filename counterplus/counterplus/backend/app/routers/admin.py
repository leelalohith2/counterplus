from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, schemas, security
from ..database import get_db

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/users", response_model=List[schemas.UserOut])
def list_users(
    admin: models.User = Depends(security.get_current_admin),
    db: Session = Depends(get_db),
):
    return db.query(models.User).order_by(models.User.created_at.desc()).all()


@router.get("/transactions", response_model=List[schemas.TransactionOut])
def list_all_transactions(
    admin: models.User = Depends(security.get_current_admin),
    db: Session = Depends(get_db),
):
    return (
        db.query(models.Transaction)
        .order_by(models.Transaction.created_at.desc())
        .limit(500)
        .all()
    )
