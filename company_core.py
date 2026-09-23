"""Company identity and runtime configuration for Project Vault AIOS."""
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
VAULT_DATA_DIR = PROJECT_ROOT / "vault_data"
BLOCKCHAIN_FILE = VAULT_DATA_DIR / "blockchain.json"
FINANCE_FILE = VAULT_DATA_DIR / "finance.json"


class CompanyCore:
    """Central company identity/configuration shared by the application."""

    def __init__(self, company_name="Project Vault AI"):
        self.company_name = company_name
        self.product_name = "Project Vault AIOS"
        self.data_directory = VAULT_DATA_DIR

    def ensure_data_directory(self):
        self.data_directory.mkdir(parents=True, exist_ok=True)