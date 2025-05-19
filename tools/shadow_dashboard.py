from rich.console import Console
from rich.table import Table
from glob import glob
import json
import os

console = Console()
logs = sorted(glob("logs/*.json"), key=os.path.getmtime, reverse=True)
if not logs:
    console.print("[red]Nema dostupnih log fajlova.[/red]")
    exit()

# Učitaj poslednji log
with open(logs[0]) as f:
    data = json.load(f)

if not data:
    console.print("[yellow]Log fajl je prazan.[/yellow]")
    exit()

# Proračunaj statistiku
total = len(data)
avg = sum(d["score"] for d in data) / total
hit_count = sum(1 for d in data if d["score"] >= 60)
top5 = sorted(data, key=lambda x: x["score"], reverse=True)[:5]

# Prikaz
console.rule("[bold green]ShadowFox Dashboard")

table = Table(show_header=True, header_style="bold magenta")
table.add_column("Stat", style="cyan", width=22)
table.add_column("Vrednost", style="white")

table.add_row("Ukupno payload-a", str(total))
table.add_row("Prosečan score", f"{avg:.2f}")
table.add_row("HIT-ova (score≥60)", str(hit_count))

console.print(table)

console.print("\n[bold green]Top 5 Payloada:\n")
for i, p in enumerate(top5, 1):
    console.print(f"[{i}] ({p['score']}) [{p['category']}] → {p['payload']}")
