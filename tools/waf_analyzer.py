import json
import os
from glob import glob
from rich.console import Console
from rich.table import Table

console = Console()

files = sorted(glob("reports/launcher_ai_*.json"), key=os.path.getmtime, reverse=True)
if not files:
    console.print("[!] No launcher logs found.", style="bold red")
    exit()

with open(files[0]) as f:
    data = json.load(f)

waf_indicators = {
    "403": 0,
    "429": 0,
    "500": 0,
    "slow": 0,
    "total": 0
}

suspects = []

for entry in data:
    code = str(entry.get("status_code", "??"))
    size = entry.get("length", 0)
    if code in waf_indicators:
        waf_indicators[code] += 1

    if code in ["403", "429"] or size < 50:
        suspects.append(entry)
    waf_indicators["total"] += 1

# Tabela
table = Table(title="WAF & Anomaly Detection", style="bold white")
table.add_column("Status Code")
table.add_column("Count")

for k in ["403", "429", "500"]:
    table.add_row(k, str(waf_indicators[k]))

console.print(table)

if suspects:
    console.print(f"\n[!] Potential WAF/Filter triggers detected: {len(suspects)}\n", style="bold yellow")
    for s in suspects[:5]:
        console.print(f"- [{s['status_code']}] {s['payload'][:60]}...")
else:
    console.print("\n[✓] No strong WAF indicators found.", style="bold green")
