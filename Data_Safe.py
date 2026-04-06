import argparse
import os
import sys

import pandas as pd
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn
from rich.table import Table

from core.analyzer import PII_Analyzer
from core.transformer import PII_Transformer
from core.vault import DataVault

VERSION = "1.1.0"
console = Console()


def process_csv(filepath, output_dir, analyzer, transformer, dry_run=False):
    """Analyze and anonymize a single CSV file. Returns a summary dict."""
    filename = os.path.basename(filepath)
    output_file = os.path.join(output_dir, f"safe_{filename}")

    try:
        df = pd.read_csv(filepath, encoding="utf-8")
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(filepath, encoding="latin-1")
        except Exception as e:
            console.print(f"[bold red]✗[/bold red] Failed to read {filename}: {e}")
            return None
    except Exception as e:
        console.print(f"[bold red]✗[/bold red] Failed to read {filename}: {e}")
        return None

    if df.empty:
        console.print(f"[bold yellow]![/bold yellow] {filename} is empty, skipping.")
        return None

    pii_counts = {}
    total_replacements = 0

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TimeRemainingColumn(),
        console=console,
    ) as progress:
        task = progress.add_task(f"Processing {filename}...", total=len(df))
        col_indices = {col: df.columns.get_loc(col) for col in df.columns}

        for idx in range(len(df)):
            for col, col_idx in col_indices.items():
                val = str(df.iat[idx, col_idx])
                if val in ("nan", "None", ""):
                    continue

                results = analyzer.analyze_text(val)
                if results:
                    entity_type = results[0].entity_type
                    if not dry_run:
                        df.iat[idx, col_idx] = transformer.get_deterministic_fake(val, entity_type)
                    pii_counts[entity_type] = pii_counts.get(entity_type, 0) + 1
                    total_replacements += 1

            progress.update(task, advance=1)

    if not dry_run:
        df.to_csv(output_file, index=False)
        console.print(f"[bold green]✔[/bold green] Saved: [bold underline]{output_file}[/bold underline]")

    return {
        "file": filename,
        "rows": len(df),
        "columns": len(df.columns),
        "replacements": total_replacements,
        "pii_types": pii_counts,
    }


def print_summary(summaries, dry_run=False):
    """Print a summary table of all processed files."""
    label = "Dry-Run Report" if dry_run else "Anonymization Report"
    table = Table(title=label, show_lines=True)
    table.add_column("File", style="cyan")
    table.add_column("Rows", justify="right")
    table.add_column("Replacements", justify="right", style="green")
    table.add_column("PII Types Detected")

    for s in summaries:
        pii_str = ", ".join(f"{k}: {v}" for k, v in sorted(s["pii_types"].items()))
        table.add_row(s["file"], str(s["rows"]), str(s["replacements"]), pii_str or "None")

    console.print()
    console.print(table)


def main():
    parser = argparse.ArgumentParser(description="diShine Data-Safe USB — Local PII Anonymizer")
    parser.add_argument("--dry-run", action="store_true", help="Scan for PII without modifying files")
    parser.add_argument("--input", default="input", help="Input directory (default: input)")
    parser.add_argument("--output", default="output", help="Output directory (default: output)")
    args = parser.parse_args()

    console.print(Panel(
        f"[bold cyan]diShine Data-Safe USB v{VERSION}[/bold cyan]\n[dim]Local PII Anonymizer[/dim]",
        expand=False,
    ))

    input_dir = args.input
    output_dir = args.output
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    csv_files = sorted(
        [f for f in os.listdir(input_dir) if f.lower().endswith(".csv")],
        key=lambda x: os.path.getmtime(os.path.join(input_dir, x)),
        reverse=True,
    )

    if not csv_files:
        console.print(f"[bold yellow]![/bold yellow] No CSV files found in [bold]{input_dir}/[/bold].")
        console.print("Drop one or more CSV files into that folder and run again.")
        return

    console.print(f"[bold green]✔[/bold green] Found {len(csv_files)} CSV file(s) in [bold]{input_dir}/[/bold]")

    if args.dry_run:
        console.print("[bold yellow]![/bold yellow] Dry-run mode — no files will be modified.\n")

    analyzer = PII_Analyzer()
    transformer = PII_Transformer()
    vault = DataVault()

    summaries = []
    for csv_file in csv_files:
        filepath = os.path.join(input_dir, csv_file)
        result = process_csv(filepath, output_dir, analyzer, transformer, dry_run=args.dry_run)
        if result:
            summaries.append(result)

    if summaries:
        print_summary(summaries, dry_run=args.dry_run)

    if not args.dry_run and transformer.mapping:
        vault.save_mapping(transformer.mapping)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold red]Cancelled by user.[/bold red]")
    except Exception as e:
        console.print(f"\n[bold red]Fatal Error:[/bold red] {e}")
        sys.exit(1)
