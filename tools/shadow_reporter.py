from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import json, os
from glob import glob
from datetime import datetime

def generate_report(log_path, output_pdf):
    c = canvas.Canvas(output_pdf, pagesize=A4)
    width, height = A4
    c.setFont("Helvetica", 10)
    y = height - 40

    with open(log_path) as f:
        data = json.load(f)

    c.drawString(40, y, f"ShadowFox Payload Report – {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    y -= 30

    for entry in data:
        payload = entry.get("payload", "")
        score = entry.get("score", "N/A")
        cat = entry.get("category", "N/A")
        y -= 15
        if y < 50:
            c.showPage()
            y = height - 40
            c.setFont("Helvetica", 10)
        c.drawString(40, y, f"[{cat}] Score: {score} → {payload[:100]}")

    c.save()
    print(f"[✓] PDF generisan: {output_pdf}")

# Auto-find poslednji log
logs = sorted(glob("logs/*.json"), key=os.path.getmtime, reverse=True)
if not logs:
    print("[!] Nema dostupnih log fajlova u logs/")
else:
    log_file = logs[0]
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = f"reports/report_{ts}.pdf"
    generate_report(log_file, out)
