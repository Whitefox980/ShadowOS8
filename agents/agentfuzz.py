import os
import importlib
from glob import glob
from rich import print

def run_agentfuzz(target):
    print(f"[●] AgentFuzz aktivan na meti: [yellow]{target}[/yellow]")

    base_dir = "core_fuzz"
    modules = glob(f"{base_dir}/fuzz_*.py")
    summary = []

    for path in modules:
        modname = os.path.basename(path).replace(".py", "")
        try:
            module = importlib.import_module(f"{base_dir}.{modname}")
            if hasattr(module, "run"):
                print(f"[+] Pokrećem modul: [cyan]{modname}[/cyan]")
                result = module.run(target)
                summary.append(result)
        except Exception as e:
            print(f"[×] Greška u {modname}: {e}")

    if summary:
        from tools.utils import save_json
        save_json(summary, "agentfuzz_result")
        print(f"[✓] Rezultati sačuvani u: reports/agentfuzz_result_*.json")
    else:
        print("[!] Nema rezultata.")
