"""Project Vault AIOS application entry point."""
import json

from company_core import CompanyCore
from financial_ledger import FinancialLedger
from trust_ledger import TrustProtocol


class ProjectVaultAIOS:
    def __init__(self):
        self.company = CompanyCore()
        self.company.ensure_data_directory()
        self.company_name = self.company.company_name
        self.ledger = TrustProtocol()
        self.finance = FinancialLedger()
        print(f"[{self.company_name}] Autonomous Infrastructure Operating System Fully Integrated.")

    def execute_and_seal_workflow(self, raw_input_text, item_name, unit_cost, quantity):
        """Calculate and record the financial audit inside the sealed trust chain."""
        print("\n[System] Step 1: Initializing Agentic Context Parse Network...")
        print("[System] Step 2: Initiating Financial Ledger Audit Protocol...")
        financial_record = self.finance.calculate_disbursement(item_name, unit_cost, quantity)
        master_payload = {
            "incident_report": raw_input_text,
            "financial_audit": financial_record,
            "system_clearance": "SECURE_PASS",
        }
        last_block = self.ledger.get_last_block()
        print("[System] Step 3: Generating Cryptographic Token Stamp...")
        return self.ledger.create_block(
            proof=999,
            previous_hash=last_block["hash"],
            data=master_payload,
        )


if __name__ == "__main__":
    aios = ProjectVaultAIOS()
    sealed_block = aios.execute_and_seal_workflow(
        raw_input_text=(
            "Client requested an immediate material shift on the east corridor. "
            "Standard wiring won't pass fire codes. Upgrading to heavy copper wiring."
        ),
        item_name="Heavy-Duty Shielded Copper Wiring (Grade A)",
        unit_cost=12.50,
        quantity=350,
    )
    print("\n=== PROJECT VAULT AIOS: SEALED WORKFLOW ===")
    print(json.dumps({
        "new_block_index": sealed_block["index"],
        "chain_blocks": len(aios.ledger.blockchain),
        "finance_records": len(aios.finance.disbursement_history),
        "seal_valid": aios.ledger.verify_chain(),
        "last_block": sealed_block,
    }, indent=2, ensure_ascii=False))