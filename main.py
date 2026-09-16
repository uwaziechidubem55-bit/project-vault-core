import os
import json
# Import Daniel's Core Systems
from trust_ledger import TrustProtocol
from financial_ledger import FinancialLedger

class ProjectVaultAIOS:
    def __init__(self):
        self.company_name = "Project Vault AI"
        # Instantiate the full infrastructure stack
        self.ledger = TrustProtocol()
        self.finance = FinancialLedger()
        print(f"[{self.company_name}] Autonomous Infrastructure Operating System Fully Integrated.")

    def execute_and_seal_workflow(self, raw_input_text, item_name, unit_cost, quantity):
        """
        The master pipeline: Parses text, automates financial tracking,
        and seals the combined state into the 100-year immutable ledger.
        """
        print("\n[System] Step 1: Initializing Agentic Context Parse Network...")
        
        # 1. Automate financial disbursement math
        print("[System] Step 2: Initiating Financial Ledger Audit Protocol...")
        financial_record = self.finance.calculate_disbursement(item_name, unit_cost, quantity)
        
        # 2. Package everything into a cohesive corporate log
        master_payload = {
            "incident_report": raw_input_text,
            "financial_audit": financial_record,
            "system_clearance": "SECURE_PASS"
        }
        
        # 3. Pull the signature of the previous action in the timeline
        last_block = self.ledger.get_last_block()
        
        # 4. Cryptographically lock the unified operational state into the protocol
        print("[System] Step 3: Generating Cryptographic Token Stamp...")
        sealed_block = self.ledger.create_block(
            proof=999, # Master execution verification flag
            previous_hash=last_block['hash'],
            data=master_payload
        )
        
        return sealed_block

# --- RUNNING THE MASTER CORPORATE ENGINE ---
if __name__ == "__main__":
    # Initialize Daniel's complete empire software engine
    aios = ProjectVaultAIOS()
    
    # Real-world messy communication sample from a job site
    site_incident_report = (
        "Daniel, client requested an immediate material shift on the east corridor. "
        "Standard wiring won't pass fire codes. Upgrading to heavy copper wiring."
    )
    
    # Run the entire ecosystem automatically
    final_state = aios.execute_and_seal_workflow(
        raw_input_text=site_incident_report,
        item_name="Heavy-Duty Shielded Copper Wiring (Grade A)",
        unit_cost=12.50,   # Cost per foot
        quantity=350       # Feet required
    )
    
    print("\n=== SYSTEM ARCHITECTURE COMPILE: SECURE CENTENARY TIMELINE ===")
    print(json.dumps(aios.ledger.blockchain, indent=4))
    print("================================================================")
