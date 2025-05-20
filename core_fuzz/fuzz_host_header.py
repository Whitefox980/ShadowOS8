import requests

def run(target):
    payloads = [
        "evil.com",
        "attacker.com",
        "localhost",
        "127.0.0.1",
        "google.com"
    ]

    reflections = 0
    hits = 0
    sent = 0

    for payload in payloads:
        try:
            headers = {"Host": payload}
            r = requests.get(target, headers=headers, timeout=6)
            sent += 1
            if payload in r.text or "Invalid Host" not in r.text:
                hits += 1
        except:
            continue

    return {
        "module": "fuzz_host_header",
        "payloads_sent": sent,
        "reflections": reflections,
        "hits": hits,
        "notes": "Host Header Injection test"
    }
