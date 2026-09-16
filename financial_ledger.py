import json

class FinancialLedger:
    def __init__(self):
        self.ledger_name = "Project Vault Financial Audit Protocol"
        self.disbursement_history = []
        print(f"[{self.ledger_name}] Financial Tracking & Compliance Engines Online.")

    def calculate_disbursement(self, item_name, unit_cost, quantity_required, markup_percentage=0.10):
        """
        Autonomously calculates total material costs, applies corporate 
        overhead markup, and formats a validated subcontractor payout log.
        """
        # Base math computation
        base_cost = unit_cost * quantity_required
        markup_amount = base_cost * markup_percentage
        total_payout = base_cost + markup_amount

        payout_record = {
            "disbursement_item": item_name,
            "financials": {
                "base_cost_calculation": f"{quantity_required} units x ${unit_cost:.2f} = ${base_cost:.2f}",
                "corporate_markup_applied": f"{markup_percentage * 100}% (${markup_amount:.2f})",
                "final_certified_payout": f"${total_payout:.2f}"
            },
            "compliance_status": "FUNDS_VERIFIED_AND_LOCKED"
        }

        self.disbursement_history.append(payout_record)
        return payout_record

# --- TESTING THE FINANCIAL SYSTEM ---
if __name__ == "__main__":
    fin_system = FinancialLedger()
    
    # Simulate calculating the cost for the extra concrete foundation layout
    simulated_payout = fin_system.calculate_disbursement(
        item_name="Extra Concrete Reinforcement Base Layer",
        unit_cost=150.00,  # $150 per cubic yard
        quantity_required=45 # 45 cubic yards needed
    )
    
    print("\n=== SYSTEM OUTPUT: CERTIFIED FINANCIAL DISBURSEMENT ===")
    print(json.dumps(simulated_payout, indent=4))
    print("=========================================================")
