import hashlib
import time
import json

class TrustProtocol:
    def __init__(self):
        self.blockchain = []
        # Create the foundational "Genesis Block" of Daniel's empire
        self.create_block(proof=100, previous_hash='0' * 64, data="Project Vault Genesis Protocol Activated")

    def create_block(self, proof, previous_hash, data):
        """
        Generates an immutable cryptographic block representing a verified 
        action within the commercial construction ecosystem.
        """
        block = {
            'index': len(self.blockchain) + 1,
            'timestamp': time.time(),
            'proof': proof,
            'previous_hash': previous_hash,
            'project_data': data
        }
        # Securely hash the block using SHA-256 encryption
        block['hash'] = self.hash_block(block)
        self.blockchain.append(block)
        return block

    def get_last_block(self):
        return self.blockchain[-1]

    @staticmethod
    def hash_block(block):
        """
        Encodes a block into a string and returns a secure cryptographic signature.
        """
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

# --- TESTING DANIEL'S SECURE LEDGER LAYER ---
if __name__ == "__main__":
    protocol = TrustProtocol()
    
    # Simulating data arriving from our main engine (e.g., from main.py)
    verified_change_order = {
        "action": "Change Order Approved",
        "detail": "Reinforced brick subbed for drywall on North Wall",
        "cost_impact": "+$8,450"
    }
    
    # Lock the data permanently into the protocol
    last_block = protocol.get_last_block()
    new_block = protocol.create_block(
        proof=200, 
        previous_hash=last_block['hash'], 
        data=verified_change_order
    )
    
    print("\n=== PROJECT VAULT TRUST PROTOCOL TIMELINE ===")
    print(json.dumps(protocol.blockchain, indent=4))
    print("==============================================")
