"""Persistent, hash-chained trust ledger."""
import json
import time
from pathlib import Path

from company_core import BLOCKCHAIN_FILE, VAULT_DATA_DIR
from seal import seal, verify_seal


class TrustProtocol:
    def __init__(self, storage_path=None):
        self.storage_path = Path(storage_path) if storage_path else BLOCKCHAIN_FILE
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self.blockchain = self._load_chain()
        if not self.blockchain:
            self.create_block(
                proof=100,
                previous_hash="0" * 64,
                data="Project Vault Genesis Protocol Activated",
            )

    def _load_chain(self):
        if not self.storage_path.exists():
            return []
        try:
            with self.storage_path.open("r", encoding="utf-8") as handle:
                chain = json.load(handle)
        except (json.JSONDecodeError, OSError) as exc:
            raise ValueError(f"Unable to load blockchain file {self.storage_path}: {exc}") from exc
        if not isinstance(chain, list):
            raise ValueError("Blockchain data must be a JSON list.")
        return chain

    def _save_chain(self):
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.storage_path.with_suffix(self.storage_path.suffix + ".tmp")
        with temporary.open("w", encoding="utf-8") as handle:
            json.dump(self.blockchain, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
        temporary.replace(self.storage_path)

    def create_block(self, proof, previous_hash, data):
        """Create, seal, append, and persist one block."""
        block = {
            "index": len(self.blockchain) + 1,
            "timestamp": time.time(),
            "proof": proof,
            "previous_hash": previous_hash,
            "project_data": data,
        }
        block["hash"] = seal(block)
        self.blockchain.append(block)
        self._save_chain()
        return block

    def get_last_block(self):
        if not self.blockchain:
            raise IndexError("The trust ledger has no blocks.")
        return self.blockchain[-1]

    def verify_chain(self):
        """Validate every block seal and its link to the preceding block."""
        if not self.blockchain:
            return False
        for index, block in enumerate(self.blockchain):
            if not isinstance(block, dict) or "hash" not in block:
                return False
            body = {key: value for key, value in block.items() if key != "hash"}
            if not verify_seal(body, block["hash"]):
                return False
            if block.get("index") != index + 1:
                return False
            expected_previous = "0" * 64 if index == 0 else self.blockchain[index - 1].get("hash")
            if block.get("previous_hash") != expected_previous:
                return False
        return True

    @staticmethod
    def hash_block(block):
        """Return the SHA-256 seal of a block, excluding any existing hash field."""
        body = {key: value for key, value in block.items() if key != "hash"}
        return seal(body)

    @staticmethod
    def verify_block(block):
        if not isinstance(block, dict) or "hash" not in block:
            return False
        body = {key: value for key, value in block.items() if key != "hash"}
        return verify_seal(body, block["hash"])


if __name__ == "__main__":
    protocol = TrustProtocol()
    print(json.dumps({"blocks": len(protocol.blockchain), "chain_valid": protocol.verify_chain()}, indent=2))