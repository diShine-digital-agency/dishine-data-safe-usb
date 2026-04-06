import os
import sys
import pandas as pd
from core.analyzer import PII_Analyzer
from core.transformer import PII_Transformer
from core.vault import DataVault
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn

console = Console()

def main():
    console.print(Panel("[bold cyan]diShine Data-Safe USB v1.0[/bold cyan]\n[dim]100% GDPR-Compliant Local Anonymizer[/dim]", expand=False))
    
    input_dir = "input"
    output_dir = "output"
    
    if not os.path.exists(input_dir):
        os.makedirs(input_dir)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    csv_files = [f for f in os.listdir(input_dir) if f.endswith(".csv")]
    
    if not csv_files:
        console.print(f"[bold yellow]![/bold yellow] No CSV files found in [bold]{input_dir}/[/bold].")
        console.print("Please drop a CSV file and run again.")
        return

    # Pick the latest CSV
    csv_files.sort(key=lambda x: os.path.getmtime(os.path.join(input_dir, x)), reverse=True)
    input_file = os.path.join(input_dir, csv_files[0])
    output_file = os.path.join(output_dir, f"safe_{csv_files[0]}")
    
    console.print(f"[bold green]✔[/bold green] Found: [bold cyan]{csv_files[0]}[/bold cyan]")
    
    # 1. Load Data
    df = pd.read_csv(input_file)
    analyzer = PII_Analyzer()
    transformer = PII_Transformer()
    vault = DataVault()
    
    # Analyze and Transform
    console.print("[bold cyan]![/bold cyan] Scanning for PII and anonymizing...")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TimeRemainingColumn(),
        console=console
    ) as progress:
        task = progress.add_task("Anonymizing rows...", total=len(df))
        
        for idx, row in df.iterrows():
            for col in df.columns:
                val = str(row[col])
                results = analyzer.analyze_text(val)
                
                # Sort by reverse order to avoid index shift
                # but for simplicity, if any PII is detected, we replace the whole cell
                if results:
                    # In a CSV column, usually the whole cell is the PII item
                    # e.g., Name column, Email column.
                    # We pick the most likely entity type
                    entity_type = results[0].entity_type
                    df.at[idx, col] = transformer.get_deterministic_fake(val, entity_type)
            
            progress.update(task, advance=1)
            
    # 2. Save Output
    df.to_csv(output_file, index=False)
    console.print(f"[bold green]✔[/bold green] Anonymized file saved: [bold underline]{output_file}[/bold underline]")
    
    # 3. Save Vault Mapping
    vault.save_mapping(transformer.mapping)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold red]Cancelled by user.[/bold red]")
    except Exception as e:
        console.print(f"\n[bold red]Fatal Error:[/bold red] {e}")
