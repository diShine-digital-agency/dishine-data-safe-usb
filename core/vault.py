import json
import os

from rich.console import Console

console = Console()


class DataVault:
    """Stores original-to-fake PII mappings locally as JSON files."""

    def __init__(self, vault_dir="vault"):
        self.vault_dir = vault_dir
        os.makedirs(self.vault_dir, exist_ok=True)

    def save_mapping(self, mapping, filename="mapping_key.json"):
        """Persist the mapping dictionary to a JSON file."""
        path = os.path.join(self.vault_dir, filename)
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(mapping, f, indent=4, ensure_ascii=False)
            console.print(f"[bold green]✔[/bold green] Vault mapping saved to: [bold underline]{path}[/bold underline]")
            return True
        except Exception as e:
            console.print(f"[bold red]Error saving vault:[/bold red] {e}")
            return False

    def load_mapping(self, filename="mapping_key.json"):
        """Load a previously saved mapping from the vault."""
        path = os.path.join(self.vault_dir, filename)
        if not os.path.exists(path):
            return {}
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            console.print(f"[bold red]Error loading vault:[/bold red] {e}")
            return {}
