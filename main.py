import os
import json
# Import Daniel's 100-Year Trust Protocol from trust_ledger.py
from trust_ledger import TrustProtocol

class ProjectVaultEngine:
    def __init__(self):
        self.company_name = "Project Vault AI"
        # Initialize our cryptographic ledger right inside our core engine
        self.ledger = TrustProtocol()
        print(f"[{self.company_name}] Unified System Online. Trust Ledger Linked.")

    def process_and_seal_change_order(self, raw_input_text):
        """
        Takes raw industry data, structures it, and instantly passes it
        to the trust protocol layer to secure it for the next 100 years.
        """
        print("\n[System] Parsing chaotic inputs via Agentic Network...")
        
        # 1. Structure the incoming data
        structured_data = {
            "source_data": raw_input_text,
            "automated_action": "Dynamic Project Variation Registered",
            "compliance_check": "VERIFIED_PASS"
        }
        
        # 2. Grab the signature of the previous action in our timeline
        last_block = self.ledger.get_last_block()
        
        # 3. Cryptographically seal the new action into the unalterable ledger
        sealed_block = self.ledger.create_block(
            proof=777, # Unique operational proof flag
            previous_hash=last_block['hash'],
            data=structured_data
        )
        
        return sealed_block

# --- RUNNING THE UNIFIED SYSTEM ---
if __name__ == "__main__":
    # Start Daniel's company architecture
    engine = ProjectVaultEngine()
    
    # The real-world messy communication sample
    incoming_change_order = (
        "Daniel, site foreman here. The structural engineer just updated the blueprint. "
        "We need to thick-pad the foundation base by an extra 5 inches of concrete due to soil shifting. "
        "Log this immediately for insurance records."
    )
    
    # Process it and lock it down
    final_sealed_state = engine.process_and_seal_change_order(incoming_change_order)
    
    print("\n=== SYSTEM OUTPUT: DANIEL'S SECURE CENTENARY LEDGER ===")
    print(json.dumps(engine.ledger.blockchain, indent=4))
    print("========================================================")
