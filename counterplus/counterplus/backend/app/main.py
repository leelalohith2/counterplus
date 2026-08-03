from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .database import Base, engine, SessionLocal
from . import models, security
from .routers import auth, wallet, recharge, transactions, admin

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Counter+ API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this to your real frontend origin before going live
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(wallet.router)
app.include_router(recharge.router)
app.include_router(transactions.router)
app.include_router(admin.router)


@app.on_event("startup")
def seed_admin():
    """Creates a default admin account on first run, for local testing only."""
    db = SessionLocal()
    try:
        existing = db.query(models.User).filter(models.User.email == "admin@counterplus.local").first()
        if not existing:
            admin_user = models.User(
                shop_name="Counter+ HQ",
                owner_name="Admin",
                mobile="9999999999",
                email="admin@counterplus.local",
                password_hash=security.hash_password("ChangeMe123!"),
                is_admin=True,
                kyc_status=models.KycStatus.verified,
                wallet_balance=0.0,
            )
            db.add(admin_user)
            db.commit()
    finally:
        db.close()


@app.get("/api/health")
def health():
    return {"status": "ok"}


# Serve the static frontend (login/register/dashboard pages) from the same server.
app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")
