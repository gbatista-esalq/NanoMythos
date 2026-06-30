import time
import json
import os
import hashlib
import subprocess
import random
from datetime import datetime

VAULT_DIR = "/opt/synapse_vault/quantum_world"
BATTERY_PATH = os.path.join(VAULT_DIR, "batteries.json")
AUDIT_PATH = os.path.join(VAULT_DIR, "transmutation_audit.json")
SOVEREIGNTY_PATH = os.path.join(VAULT_DIR, "sovereignty_fund.json")
REDOMA_PID = 947

ATTACK_VECTORS = {
    "negado": {
        "name": "Tentativa-Acesso-Negado",
        "charge_range": (50.0, 150.0),
        "label": "INTRUSAO_BLOQUEADA",
    },
    "FERRÃO": {
        "name": "Ferrão-IP-Bloqueado",
        "charge_range": (300.0, 500.0),
        "label": "IP_ELIMINADO",
    },
    "MEL AMARGO": {
        "name": "Mel-Amargo-Honeypot",
        "charge_range": (800.0, 1200.0),
        "label": "ATACANTE_SUGADO",
    },
    "MEL_AMARGO": {
        "name": "Mel-Amargo-Honeypot",
        "charge_range": (800.0, 1200.0),
        "label": "ATACANTE_SUGADO",
    },
}

SOVEREIGNTY_PROJECTS = [
    "Redoma-V2-Shield",
    "Dossel-Monitor-Amazonia",
    "MOONDO-Biotech-Bioreator",
    "Sul-Global-Network-Node",
    "Obsidian-Vault-Preservation",
    "Chronicles-Framework-Production",
    "Amazonia-Legal-DataBridge",
]

HAWKING_LOSS = 0.02


def _ensure_dirs():
    os.makedirs(VAULT_DIR, exist_ok=True)


def _load_sovereignty():
    if not os.path.exists(SOVEREIGNTY_PATH):
        return {p: 0.0 for p in SOVEREIGNTY_PROJECTS}
    with open(SOVEREIGNTY_PATH) as f:
        return json.load(f)


def _save_sovereignty(fund: dict):
    with open(SOVEREIGNTY_PATH, "w") as f:
        json.dump(fund, f, ensure_ascii=False, indent=2)


def _charge_battery(vector_key: str, source_ip: str, raw_line: str) -> dict:
    vector = ATTACK_VECTORS[vector_key]
    raw_charge = random.uniform(*vector["charge_range"])
    net_charge = raw_charge * (1.0 - HAWKING_LOSS)
    ts = time.time()
    battery_id = hashlib.sha256(f"{ts}{source_ip}{vector_key}".encode()).hexdigest()[:16]

    project = random.choice(SOVEREIGNTY_PROJECTS)

    cell = {
        "battery_id": battery_id,
        "charged_at": datetime.now().isoformat(timespec="seconds"),
        "source_vector": vector["name"],
        "source_ip": source_ip,
        "label": vector["label"],
        "raw_charge_yw": round(raw_charge, 4),
        "hawking_loss_yw": round(raw_charge * HAWKING_LOSS, 4),
        "net_energy_yw": round(net_charge, 4),
        "allocated_to": project,
        "status": "CHARGED",
        "axiom": "O Caos e o combustivel da Ordem Soberana.",
    }

    with open(BATTERY_PATH, "a") as f:
        f.write(json.dumps(cell, ensure_ascii=False) + "\n")

    fund = _load_sovereignty()
    fund[project] = round(fund.get(project, 0.0) + net_charge, 4)
    _save_sovereignty(fund)

    with open(AUDIT_PATH, "a") as f:
        f.write(
            json.dumps(
                {
                    "timestamp": ts,
                    "battery_id": battery_id,
                    "input_entropy_yw": round(raw_charge, 4),
                    "output_energy_yw": round(net_charge, 4),
                    "allocated_to": project,
                    "status": "TRANSMUTED",
                    "axiom": "O Caos e o combustivel da Ordem Soberana.",
                },
                ensure_ascii=False,
            )
            + "\n"
        )

    return cell


def _extract_ip(line: str) -> str:
    import re
    m = re.search(r"\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b", line)
    return m.group(1) if m else "UNKNOWN"


def _print_status(cell: dict, fund: dict):
    total = sum(fund.values())
    top = max(fund, key=fund.get)
    print(
        f"  [BATERIA {cell['battery_id'][:8]}] {cell['label']} "
        f"| {cell['net_energy_yw']:.1f} YW -> {cell['allocated_to']}\n"
        f"  Fundo Soberania: {total:.1f} YW acumulados | Lider: {top}"
    )


def _stream_redoma(pid: int):
    return subprocess.Popen(
        ["journalctl", f"_PID={pid}", "-f", "-n", "0", "--no-pager"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        bufsize=1,
    )


def run():
    _ensure_dirs()
    print("TRANSMUTADOR DE BATERIA QUANTICA v2.0 — REDOMA DA BIODIVERSIDADE")
    print(f"Monitorando Redoma (PID {REDOMA_PID}) via journald...")
    print(f"Vault: {VAULT_DIR}")
    print(f"Projetos de Soberania: {len(SOVEREIGNTY_PROJECTS)}")
    print("-" * 60)

    total_cells = 0
    proc = _stream_redoma(REDOMA_PID)

    try:
        for line in proc.stdout:
            line = line.strip()

            matched_key = None
            for key in ATTACK_VECTORS:
                if key in line:
                    matched_key = key
                    break

            if not matched_key:
                continue

            source_ip = _extract_ip(line)
            cell = _charge_battery(matched_key, source_ip, line)
            total_cells += 1
            fund = _load_sovereignty()
            print(f"\n[{cell['charged_at']}] ATAQUE CAPTURADO: {cell['source_vector']}")
            print(f"  IP: {source_ip}")
            _print_status(cell, fund)
            print(f"  Baterias totais: {total_cells}")

    except KeyboardInterrupt:
        proc.terminate()
        fund = _load_sovereignty()
        total = sum(fund.values())
        print(f"\nTransmutacao suspensa. {total_cells} baterias carregadas. {total:.1f} YW para o Sul Global.")
    finally:
        proc.terminate()


if __name__ == "__main__":
    run()
