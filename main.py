"""
main.py — ZHONNEX Central Nerve Core
Layer 5: business loop | Layer 6: API gateway & event bus
Render entrypoint: uvicorn main:app --host 0.0.0.0 --port $PORT
"""
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import BaseModel, Field

import trust_ledger
import financial_ledger

TENANTS = {"zhonnex", "zonnchat", "zonnwatch", "zonnshop"}  # sub-brand registry


# ---- Layer 6: startup/shutdown event bus boundaries -----------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    trust_ledger.record_event("SYSTEM", "AIOS_BOOT", {"layers": 7})
    yield
    trust_ledger.record_event("SYSTEM", "AIOS_SHUTDOWN", {})


app = FastAPI(title="ZHONNEX Project-Vault-AIOS", version="1.0.0",
              lifespan=lifespan)

# ---- BOUNDARY: CORS so Vercel sites never hit blank/blocked responses ----
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://*.vercel.app",
        os.environ.get("FRONTEND_ORIGIN", "*"),
    ],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


# ---- BOUNDARY: global exception handler — API never returns a dead page --
@app.exception_handler(Exception)
async def fail_safe(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"ok": False, "error": "internal", "seal": trust_ledger.SEAL},
    )


# ---- Layer 6: gateway rate-limit boundary (simple per-IP token bucket) ----
_hits: dict[str, int] = {}
RATE = 120  # requests/minute

@app.middleware("http")
async def rate_limit(request: Request, call_next):
    ip = request.client.host if request.client else "unknown"
    _hits[ip] = _hits.get(ip, 0) + 1
    if _hits[ip] > RATE:
        return JSONResponse(status_code=429,
                            content={"ok": False, "error": "rate_limited"})
    return await call_next(request)


# ---- Layer 4: SSO endpoint -------------------------------------------------
class LoginIn(BaseModel):
    tenant: str
    user: str


@app.post("/auth/login")
def login(body: LoginIn):
    if body.tenant not in TENANTS:
        raise HTTPException(404, detail="unknown tenant")
    token = trust_ledger.session_token(f"{body.tenant}:{body.user}")
    trust_ledger.record_event(body.tenant, "SSO_LOGIN", {"user": body.user})
    return {"ok": True, "token": token, "seal": trust_ledger.SEAL,
            "scopes": list(TENANTS)}


# ---- Layer 5: Watch-to-Earn ------------------------------------------------
class AdIn(BaseModel):
    tenant: str
    user: str
    seconds: int = Field(gt=0, le=3600)


@app.post("/ads/reward")
def ad_reward(body: AdIn):
    result = financial_ledger.ad_reward(body.tenant, body.user, body.seconds)
    trust_ledger.record_event(body.tenant, "AD_REWARD",
                              {"user": body.user, "seconds": body.seconds})
    return result


# ---- Layer 5: 3-channel payment router -------------------------------------
class PayIn(BaseModel):
    tenant: str
    user: str
    amount: float = Field(gt=0)
    channel: str


@app.post("/payments")
def payments(body: PayIn):
    result = financial_ledger.process_payment(
        body.tenant, body.user, body.amount, body.channel)
    trust_ledger.record_event(body.tenant, "PAYMENT",
                              {"user": body.user, "channel": body.channel,
                               "amount": body.amount, "status": result["status"]})
    return result


@app.get("/payments/balance/{tenant}/{user}")
def get_balance(tenant: str, user: str):
    return {"tenant": tenant, "user": user,
            "balance": financial_ledger.balance(tenant, user)}


# ---- Layer 5: ledger health/integrity ---------------------------------------
@app.get("/ledger/verify")
def verify():
    return {"chain_valid": trust_ledger.verify_chain(),
            "seal": trust_ledger.SEAL}


# ---- BOUNDARY: root + health so Render never shows a blank page ------------
@app.get("/", response_class=PlainTextResponse)
def root():
    return "ZHONNEX Project-Vault-AIOS online | Seal: " + trust_ledger.SEAL


@app.get("/health")
def health():
    return {"ok": True, "layers": 7, "tenants": sorted(TENANTS)}