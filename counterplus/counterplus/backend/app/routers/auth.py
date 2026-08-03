from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas, security
from ..database import get_db
from ..utils.captcha import generate_captcha, verify_captcha

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.get("/captcha", response_model=schemas.CaptchaResponse)
def get_captcha():
    captcha_id, text = generate_captcha()
    # In production, render `text` into an actual distorted image and only
    # return captcha_id + the image. Returned as plain text here since this
    # starter has no image-rendering dependency installed.
    return schemas.CaptchaResponse(captcha_id=captcha_id, captcha_text=text)


@router.post("/register", response_model=schemas.TokenResponse)
def register(payload: schemas.RegisterRequest, db: Session = Depends(get_db)):
    if not verify_captcha(payload.captcha_id, payload.captcha_answer):
        raise HTTPException(status_code=400, detail="Incorrect security code")

    if db.query(models.User).filter(
        (models.User.email == payload.email) | (models.User.mobile == payload.mobile)
    ).first():
        raise HTTPException(status_code=400, detail="Email or mobile already registered")

    user = models.User(
        shop_name=payload.shop_name,
        owner_name=payload.owner_name,
        mobile=payload.mobile,
        email=payload.email,
        password_hash=security.hash_password(payload.password),
        referral_code=payload.referral_code,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = security.create_access_token(str(user.id))
    return schemas.TokenResponse(access_token=token)


@router.post("/login", response_model=schemas.TokenResponse)
def login(payload: schemas.LoginRequest, db: Session = Depends(get_db)):
    if not verify_captcha(payload.captcha_id, payload.captcha_answer):
        raise HTTPException(status_code=400, detail="Incorrect security code")

    user = db.query(models.User).filter(
        (models.User.email == payload.identifier) | (models.User.mobile == payload.identifier)
    ).first()

    if not user or not security.verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = security.create_access_token(str(user.id))
    return schemas.TokenResponse(access_token=token)


@router.get("/me", response_model=schemas.UserOut)
def me(user: models.User = Depends(security.get_current_user)):
    return user
