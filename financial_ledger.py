"""
financial_ledger.py — 3-channel payment system + ad earnings
Layers: 2 (Firebase real-time + JSON audit), 5 (business logic)
"""
import json
import os
import time
from pathlib import Path

VAULT_DIR = Path(__file__).parent / "vault_data"
FINANCE_FILE = VAULT_DIR / "finance.json"

VALID_CHANNELS = {"card", "crypto", "bank_transfer"}

# --- Layer 2 bridge: Firebase Realtime DB (live ads sync, soft-fail boundary) ---
try:
    import firebase_admin
    from firebase_admin import credentials, db
    if os.environ.get("FIREBASE_CREDENTIALS_JSON") and not firebase_admin._apps:
        cred = credentials.Certificate(
            json.loads(os.environ["FIREBASE_CREDENTIALS_JSON"])
        )
        firebase_admin.initialize_app(cred, {
            "databaseURL": os.environ["FIREBASE_DB_URL"]
        })
    _fb = db
except Exception:
    _fb = None


def _load() -> dict:
    try:
        return json.loads(FINANCE_FILE.read_text())
    except Exception:
        seed = {"currency": "USD",
                "payment_channels": sorted(VALID_CHANNELS),
                "accounts": [], "audit_log": []}
        _save(seed)
        return seed


def _save(data: dict) -> None:
    VAULT_DIR.mkdir(parents=True, exist_ok=True)
    FINANCE_FILE.write_text(json.dumps(data, indent=2))


def _audit(event: str, channel: str | None, amount: float) -> None:
    data = _load()
    data["audit_log"].append({
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "event": event, "channel": channel, "amount": round(amount, 2),
    })
    _save(data)


def ad_reward(tenant: str, user: str, seconds_watched: int) -> dict:
    """Watch-to-Earn engine. $0.01 per 10s watched, synced to Firebase live."""
    amount = round(seconds_watched * 0.001, 4)
    _audit("AD_REWARD", "card", amount)
    if _fb:
        try:
            _fb.reference(f"ads/{tenant}/earnings/{user}").set({
                "amount": amount, "ts": time.time()})
        except Exception:
            pass
    return {"tenant": tenant, "user": user, "reward": amount, "status": "credited"}


def process_payment(tenant: str, user: str, amount: float, channel: str) -> dict:
    """3-channel payment router: Card | Crypto | Bank Transfer."""
    if channel not in VALID_CHANNELS:
        return {"status": "rejected",
                "reason": f"channel must be one of {sorted(VALID_CHANNELS)}"}
    if amount <= 0:
        return {"status": "rejected", "reason": "amount must be positive"}

    data = _load()
    account = next((a for a in data["accounts"]
                    if a["tenant"] == tenant and a["user"] == user), None)
    if not account:
        account = {"tenant": tenant, "user": user, "balance": 0.0}
        data["accounts"].append(account)
    account["balance"] = round(account["balance"] + amount, 2)
    _save(data)
    _audit("PAYMENT", channel, amount)
    return {"status": "completed", "channel": channel,
            "new_balance": account["balance"]}


def balance(tenant: str, user: str) -> float:
    data = _load()
    acc = next((a for a in data["accounts"]
                if a["tenant"] == tenant and a["user"] == user), None)
    return acc["balance"] if acc else 0.0