# Counter+ — Recharge & BBPS Partner Portal

A working recharge/DTH/bill-payment agent portal: register, log in, top up
your wallet, and process recharges/bill payments. Ships with a **mock**
recharge provider and payment gateway so you can run and test the whole
thing right now, with clearly marked adapters to plug in real ones later.

## What's actually real vs. mocked

| Piece | Status |
|---|---|
| Registration, login, JWT auth, password hashing | Real |
| Wallet balance & transaction ledger (SQLite) | Real |
| Recharge / bill-pay business logic (debit, refund on failure, history) | Real |
| Admin endpoints (list users/transactions) | Real |
| Recharge/BBPS provider | **Mock** — swap in `app/providers/live_provider.py` |
| Payment gateway (wallet top-up) | **Mock** — swap in `app/providers/live_payment.py` |

The mock provider/gateway behave like real ones (random failures, reference
IDs) so the whole app can be exercised end-to-end without a live account.
No real money moves anywhere in this codebase as shipped.

## Run it locally

```bash
cd backend
python3 -m venv venv && source venv/bin/activate   # optional but recommended
pip install -r requirements.txt
cp .env.example .env                                 # edit if you want
uvicorn app.main:app --reload --port 8000
```

Open **http://127.0.0.1:8000/login.html** — the FastAPI server also serves
the frontend, so there's nothing else to start.

A demo admin account is auto-created on first run:
- email: `admin@counterplus.local`
- password: `ChangeMe123!`

(Admin login uses the same login form; admin-only data is available via the
`/api/admin/users` and `/api/admin/transactions` endpoints — there's no
admin UI yet, just the API.)

## Project layout

```
backend/
  app/
    main.py            FastAPI app, mounts frontend + routers
    config.py           Settings loaded from .env
    database.py          SQLAlchemy engine/session
    models.py             User, Transaction tables
    schemas.py             Request/response validation
    security.py             Password hashing, JWT
    routers/
      auth.py                register / login / captcha / me
      wallet.py                balance / top-up
      recharge.py               operators / recharge / pay bill
      transactions.py            transaction history
      admin.py                    admin-only user/transaction views
    providers/
      base.py                  interfaces every adapter implements
      mock_provider.py          fake recharge/BBPS (default)
      live_provider.py          STUB — real aggregator goes here
      mock_payment.py           fake payment gateway (default)
      live_payment.py           STUB — real gateway goes here
frontend/
  login.html / register.html / dashboard.html / recharge.html
  api.js       shared fetch client (handles JWT, requests)
  style.css
```

## Going live: what you need to do yourself

I can't obtain these for you — they require your business to register
directly:

1. **A licensed BBPS/recharge aggregator account** (e.g. Eko, PaySprint,
   Robotics Exchange, DigiPay, Setu BBPS, or an NSDL Payments Bank BBPOU
   partnership). They'll give you a base URL, API key/secret, and their
   own request/response format. Implement `do_recharge()` in
   `app/providers/live_provider.py` using their docs, then set
   `PROVIDER_MODE=live` in `.env`.

2. **A payment gateway merchant account** (Razorpay, Cashfree, PayU, etc.)
   for real wallet top-ups. Implement `create_order()` and
   `verify_payment()` in `app/providers/live_payment.py`, add a webhook
   endpoint that calls `verify_payment()` before crediting a wallet (never
   trust the frontend alone), then set `PAYMENT_MODE=live`.

3. **Compliance**: BBPS operations in India are regulated by NPCI/RBI.
   Operating as a biller-facing agent typically means working *through* an
   authorized BBPOU/aggregator rather than integrating with NPCI directly.
   Talk to your chosen aggregator about what's required on your end (KYC,
   agreements, security audits).

4. **Before real money flows**: put this behind HTTPS, move the CORS
   `allow_origins` in `main.py` from `"*"` to your real domain, move the
   in-memory captcha store to Redis/DB if you'll run multiple server
   processes, and get a security review — this starter is a solid
   foundation, not a finished, audited payments system.
