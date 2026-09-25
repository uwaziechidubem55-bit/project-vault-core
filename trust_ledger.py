"""
trust_ledger.py — ZHONNEX Cryptographic Vault
Layers: 2 (Supabase persistence), 4 (Seal/Identity), 5 (logic)
"""
import hashlib
import json
import os
import time
from pathlib import Path

SEAL = "ZHONNEX_SEAL_GEN_I"
VAULT_DIR = Path(__file__).parent / "vault_data"
CHAIN_FILE = VAULT_DIR / "blockchain.json"

# --- Layer 2 bridge: Supabase (optional; local JSON is the fallback boundary) ---
try:
    from supabase import create_client
    _sb = create_client(
        os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"]
    ) if os.environ.get("SUPABASE_URL") else None
except Exception:
    _sb = None  # boundary: never crash the core if Supabase is unreachable


def _load_chain() -> dict:
    """Boundary rule: if file is missing/corrupt, rebuild from genesis."""
    try:
        return json.loads(CHAIN_FILE.read_text())
    except Exception:
        genesis = {
            "chain_name": "ZHONNEX_MULTI_TENANT_LEDGER",
            "seal": SEAL,
            "blocks": [{
                "index": 0, "timestamp": "2026-01-01T00:00:00Z",
                "tenant": "SYSTEM", "action": "GENESIS_BLOCK",
                "prev_hash": "0", "hash": "seed",
            }],
        }
        _save_chain(genesis)
        return genesis


def _save_chain(chain: dict) -> None:
    VAULT_DIR.mkdir(parents=True, exist_ok=True)
    CHAIN_FILE.write_text(json.dumps(chain, indent=2))
    if _sb:
        try:
            _sb.table("zhonnex_ledger_backup").upsert(
                {"id": 1, "payload": json.dumps(chain)}
            ).execute()
        except Exception:
            pass  # soft-fail: local vault remains source of truth


def _hash_block(block: dict) -> str:
    raw = json.dumps(block, sort_keys=True) + SEAL
    return hashlib.sha256(raw.encode()).hexdigest()


def record_event(tenant: str, action: str, payload: dict | None = None) -> dict:
    """Append an immutable, sealed block. Every brand activity gets the Seal."""
    chain = _load_chain()
    prev = chain["blocks"][-1]
    block = {
        "index": prev["index"] + 1,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "tenant": tenant,
        "action": action,
        "payload": payload or {},
        "seal": SEAL,
        "prev_hash": prev["hash"],
        "hash": "",
    }
    block["hash"] = _hash_block(block)
    chain["blocks"].append(block)
    _save_chain(chain)
    return block


def verify_chain() -> bool:
    """Layer 4 integrity check — tamper detection across all tenants."""
    chain = _load_chain()
    prev_hash = "0"
    for b in chain["blocks"]:
        candidate = {k: v for k, v in b.items() if k != "hash"}
        if b["prev_hash"] != prev_hash:
            return False
        if b.get("hash") not in ("seed",) and b["hash"] != _hash_block(candidate):
            return False
        prev_hash = b["hash"]
    return True


def session_token(tenant_user: str) -> str:
    """Layer 4 SSO handshake: one token valid across the whole ecosystem."""
    raw = f"{tenant_user}:{SEAL}:{int(time.time() // 86400)}"  # daily rotation
    return hashlib.sha256(raw.encode()).hexdigest()