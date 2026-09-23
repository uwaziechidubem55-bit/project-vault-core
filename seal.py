"""Canonical SHA-256 seals for tamper-evident ledger blocks and records."""
import hashlib
import json


def canonical_json(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def seal(value):
    """Return a deterministic SHA-256 digest for a JSON-compatible value."""
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def verify_seal(value, expected_seal):
    """Check whether a value still matches its expected SHA-256 seal."""
    return isinstance(expected_seal, str) and seal(value) == expected_seal