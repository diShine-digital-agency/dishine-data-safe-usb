import json
import os
from rich.console import Console

console = Console()

class DataVault:
    def __init__(self, vault_dir="vault"):
        self.vault_dir = vault_dir
        if not os.path.exists(self.vault_dir):
            os.makedirs(self.vault_dir)

    def save_mapping(self, mapping, filename="mapping_key.json"):
        path = os.path.join(self.vault_dir, filename)
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(mapping, f, indent=4)
            console.print(f"[bold green]✔[/bold green] Vault mapping saved to: [bold underline]{path}[/bold underline]")
            return True
        except Exception as e:
            console.print(f"[bold red]Error saving vault:[/bold red] {e}")
            return False

    def load_mapping(self, filename="mapping_key.json"):
        path = os.path.join(self.vault_dir, filename)
        if not os.path.exists(path):
            return {}
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            console.print(f"[bold red]Error loading vault:[/bold red] {e}")
            return {}
