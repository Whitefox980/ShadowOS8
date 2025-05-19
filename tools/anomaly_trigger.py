import json
import os
import re
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

keywords = [
    "script", "alert(", "<img", "onerror", "root:x", "admin", "token",
    "SELECT", "UNION", "error", "exception"
]

suspicious = []

for entry in data:
    body_size = entry.get("length", 0)
    payload = entry.get("payload", "")
    code = str(entry.get("status_code", "??"))

    for word in keywords:
        if word.lower() in payload.lower():
            suspicious.append({
                "payload": payload,
                "match": word,
                "code": code,
                "length": body_size
            })
            break

table = Table(title="Anomaly Trigger - Suspicious Payload Indicators", style="bold white")
table.add_column("Status", justify="center")
table.add_column("Size", justify="right")
table.add_column("Matched", justify="center")
table.add_column("Payload Preview", style="cyan")

for s in suspicious:
    table.add_row(
        s["code"],
        str(s["length"]),
        s["match"],
        s["payload"][:40] + "..."
    )

if suspicious:
    console.print(table)
    console.print(f"\n[!] {len(suspicious)} anomalous payload(s) detected.", style="bold yellow")
else:
    console.print("[✓] No anomalies detected in recent payloads.", style="bold green")
