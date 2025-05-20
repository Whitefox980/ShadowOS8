import requests

def run(target):
    payloads = [
        "https://evil.com",
        "//evil.com",
        "/\\evil.com",
        "http://evil.com@legit.com",
        "https://evil.com#@legit.com"
    ]

    reflections = 0
    hits = 0
    sent = 0

    for payload in payloads:
        try:
            url = f"{target}?redirect={payload}"
            r = requests.get(url, allow_redirects=False, timeout=6)
            sent += 1
            if "Location" in r.headers and "evil.com" in r.headers["Location"]:
                hits += 1
        except:
            continue

    return {
        "module": "fuzz_redirect",
        "payloads_sent": sent,
        "reflections": reflections,
        "hits": hits,
        "notes": "Open redirect detection"
    }
