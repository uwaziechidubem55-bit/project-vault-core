"""Persistent financial calculations and payout history."""
import json
from pathlib import Path

from company_core import FINANCE_FILE


class FinancialLedger:
    def __init__(self, storage_path=None):
        self.ledger_name = "Project Vault Financial Audit Protocol"
        self.storage_path = Path(storage_path) if storage_path else FINANCE_FILE
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self.disbursement_history = self._load_history()
        print(f"[{self.ledger_name}] Financial Tracking & Compliance Engines Online.")

    def _load_history(self):
        if not self.storage_path.exists():
            return []
        try:
            with self.storage_path.open("r", encoding="utf-8") as handle:
                history = json.load(handle)
        except (json.JSONDecodeError, OSError) as exc:
            raise ValueError(f"Unable to load finance file {self.storage_path}: {exc}") from exc
        if not isinstance(history, list):
            raise ValueError("Finance data must be a JSON list.")
        return history

    def _save_history(self):
        temporary = self.storage_path.with_suffix(self.storage_path.suffix + ".tmp")
        with temporary.open("w", encoding="utf-8") as handle:
            json.dump(self.disbursement_history, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
        temporary.replace(self.storage_path)

    def calculate_disbursement(self, item_name, unit_cost, quantity_required, markup_percentage=0.10):
        """Calculate payout, record the audit entry, and persist it."""
        if unit_cost < 0 or quantity_required < 0 or markup_percentage < 0:
            raise ValueError("Cost, quantity, and markup must be non-negative.")
        base_cost = unit_cost * quantity_required
        markup_amount = base_cost * markup_percentage
        total_payout = base_cost + markup_amount
        payout_record = {
            "disbursement_item": item_name,
            "financials": {
                "base_cost_calculation": f"{quantity_required} units x ${unit_cost:.2f} = ${base_cost:.2f}",
                "corporate_markup_applied": f"{markup_percentage * 100}% (${markup_amount:.2f})",
                "final_certified_payout": f"${total_payout:.2f}",
            },
            "compliance_status": "FUNDS_VERIFIED_AND_LOCKED",
        }
        self.disbursement_history.append(payout_record)
        self._save_history()
        return payout_record


if __name__ == "__main__":
    financial = FinancialLedger()
    record = financial.calculate_disbursement(
        item_name="Extra Concrete Reinforcement Base Layer",
        unit_cost=150.00,
        quantity_required=45,
    )
    print(json.dumps(record, indent=2))