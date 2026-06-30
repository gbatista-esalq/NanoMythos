"""
ESCUDO ESCURO PYM — Emaranhamento Quantico Nacional
Todas as Redomas do territorio conectadas em singularidade.
Cada ataque capturado por qualquer no alimenta o fundo coletivo.
"""

import time
import json
import os
import hashlib
import random
import subprocess
from datetime import datetime

VAULT_DIR = "/opt/synapse_vault/quantum_world"
DARK_SHIELD_PATH = os.path.join(VAULT_DIR, "dark_shield.json")
ENTANGLEMENT_LOG = os.path.join(VAULT_DIR, "entanglement_log.jsonl")
SOVEREIGNTY_PATH = os.path.join(VAULT_DIR, "sovereignty_fund.json")

REDOMA_NODES = {
    "REDOMA-ALPHA": {"ip": "127.0.0.1",  "port": 8888, "pid": 947,  "estado": "SP", "bioma": "Cerrado"},
    "REDOMA-BETA":  {"ip": "192.168.0.1","port": 8889, "pid": None, "estado": "AM", "bioma": "Amazonia"},
    "REDOMA-GAMMA": {"ip": "192.168.0.2","port": 8890, "pid": None, "estado": "MT", "bioma": "Pantanal"},
    "REDOMA-DELTA": {"ip": "192.168.0.3","port": 8891, "pid": None, "estado": "BA", "bioma": "Caatinga"},
    "REDOMA-EPSILON":{"ip":"192.168.0.4","port": 8892, "pid": None, "estado": "RS", "bioma": "Pampa"},
}

PYM_MOLECULES = [
    "Ant-Man-Pym-Alpha",
    "Wasp-Pym-Beta",
    "Yellowjacket-Pym-Gamma",
    "Giant-Man-Pym-Delta",
    "Goliath-Pym-Epsilon",
]

DARK_MATTER_MULTIPLIER = 7.77

ATTACK_PATTERNS = {
    "negado":    {"energy": (50,   150),  "threat": "LOW"},
    "FERRÃO":    {"energy": (300,  500),  "threat": "MEDIUM"},
    "MEL AMARGO":{"energy": (800,  1200), "threat": "HIGH"},
    "MEL_AMARGO":{"energy": (800,  1200), "threat": "HIGH"},
    "brute":     {"energy": (200,  400),  "threat": "MEDIUM"},
    "scan":      {"energy": (100,  250),  "threat": "LOW"},
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


def _ensure_dirs():
    os.makedirs(VAULT_DIR, exist_ok=True)


def _load_fund() -> dict:
    if not os.path.exists(SOVEREIGNTY_PATH):
        return {p: 0.0 for p in SOVEREIGNTY_PROJECTS}
    with open(SOVEREIGNTY_PATH) as f:
        return json.load(f)


def _save_fund(fund: dict):
    with open(SOVEREIGNTY_PATH, "w") as f:
        json.dump(fund, f, ensure_ascii=False, indent=2)


def _load_shield() -> dict:
    if not os.path.exists(DARK_SHIELD_PATH):
        return {
            "status": "ACTIVE",
            "pym_field_strength": 0.0,
            "total_attacks_absorbed": 0,
            "total_energy_yw": 0.0,
            "dark_matter_reserve_yw": 0.0,
            "nodes_entangled": list(REDOMA_NODES.keys()),
            "shield_layers": 0,
            "axiom": "A Materia Escura Pym e impenetravel.",
            "activated_at": datetime.now().isoformat(timespec="seconds"),
            "last_update": datetime.now().isoformat(timespec="seconds"),
        }
    with open(DARK_SHIELD_PATH) as f:
        return json.load(f)


def _save_shield(shield: dict):
    shield["last_update"] = datetime.now().isoformat(timespec="seconds")
    with open(DARK_SHIELD_PATH, "w") as f:
        json.dump(shield, f, ensure_ascii=False, indent=2)


def _pym_transmute(raw_energy: float, source_node: str) -> dict:
    molecule = random.choice(PYM_MOLECULES)
    # Molecula Pym comprime o caos em materia escura util
    dark_matter = raw_energy * DARK_MATTER_MULTIPLIER
    net = raw_energy * 0.98
    pym_hash = hashlib.sha256(
        f"{time.time()}{molecule}{source_node}".encode()
    ).hexdigest()[:12]

    return {
        "pym_id": pym_hash,
        "molecule": molecule,
        "source_node": source_node,
        "raw_energy_yw": round(raw_energy, 4),
        "net_energy_yw": round(net, 4),
        "dark_matter_yw": round(dark_matter, 4),
        "compression_ratio": round(DARK_MATTER_MULTIPLIER, 2),
        "project": random.choice(SOVEREIGNTY_PROJECTS),
        "timestamp": datetime.now().isoformat(timespec="seconds"),
    }


def _absorb_attack(pattern_key: str, source_node: str, source_ip: str):
    pattern = ATTACK_PATTERNS[pattern_key]
    raw_energy = random.uniform(*pattern["energy"])
    pym = _pym_transmute(raw_energy, source_node)

    fund = _load_fund()
    fund[pym["project"]] = round(fund.get(pym["project"], 0.0) + pym["net_energy_yw"], 4)
    _save_fund(fund)

    shield = _load_shield()
    shield["pym_field_strength"] = round(
        shield["pym_field_strength"] + pym["dark_matter_yw"], 4
    )
    shield["total_attacks_absorbed"] += 1
    shield["total_energy_yw"] = round(
        shield["total_energy_yw"] + pym["net_energy_yw"], 4
    )
    shield["dark_matter_reserve_yw"] = round(
        shield["dark_matter_reserve_yw"] + pym["dark_matter_yw"], 4
    )
    shield["shield_layers"] = int(shield["pym_field_strength"] // 1000) + 1
    _save_shield(shield)

    log_entry = {
        **pym,
        "threat_level": pattern["threat"],
        "source_ip": source_ip,
        "pattern": pattern_key,
        "shield_layers_after": shield["shield_layers"],
        "total_fund_yw": round(sum(fund.values()), 4),
    }
    with open(ENTANGLEMENT_LOG, "a") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    return log_entry, shield, fund


def _stream_redoma_alpha():
    pid = REDOMA_NODES["REDOMA-ALPHA"]["pid"]
    return subprocess.Popen(
        ["journalctl", f"_PID={pid}", "-f", "-n", "0", "--no-pager"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        bufsize=1,
    )


def _extract_ip(line: str) -> str:
    import re
    m = re.search(r"\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b", line)
    return m.group(1) if m else "UNKNOWN"


def _print_shield_status(log: dict, shield: dict, fund: dict):
    total_fund = sum(fund.values())
    bars = min(shield["shield_layers"], 20) * "#"
    print(
        f"\n  [PYM {log['pym_id']}] {log['molecule']}\n"
        f"  No: {log['source_node']} | IP: {log['source_ip']} | Ameaca: {log['threat_level']}\n"
        f"  Energia: {log['raw_energy_yw']:.1f} -> {log['net_energy_yw']:.1f} YW\n"
        f"  Materia Escura gerada: {log['dark_matter_yw']:.1f} YW (x{DARK_MATTER_MULTIPLIER})\n"
        f"  Alocado para: {log['project']}\n"
        f"  Escudo: [{bars}] {shield['shield_layers']} camadas | {shield['pym_field_strength']:.1f} YW\n"
        f"  Fundo Soberania Total: {total_fund:.1f} YW | Ataques absorvidos: {shield['total_attacks_absorbed']}"
    )


def run():
    _ensure_dirs()
    shield = _load_shield()

    print("=" * 65)
    print("ESCUDO ESCURO PYM — EMARANHAMENTO QUANTICO NACIONAL v1.0")
    print("=" * 65)
    print(f"Nos emaranhados: {len(REDOMA_NODES)}")
    for name, node in REDOMA_NODES.items():
        status = "ONLINE" if node["pid"] else "STANDBY"
        print(f"  {name} | {node['estado']} ({node['bioma']}) | {status}")
    print(f"Moleculas Pym ativas: {len(PYM_MOLECULES)}")
    print(f"Multiplicador Materia Escura: x{DARK_MATTER_MULTIPLIER}")
    print(f"Camadas de escudo ativas: {shield['shield_layers']}")
    print(f"Campo Pym atual: {shield['pym_field_strength']:.1f} YW")
    print("-" * 65)
    print("Monitorando Redoma Alpha (live) + simulando rede nacional...")
    print()

    proc = _stream_redoma_alpha()

    try:
        while True:
            # Drena eventos reais do journald sem bloquear infinitamente
            try:
                proc.stdout.flush()
                line = proc.stdout.readline()
                if line:
                    line = line.strip()
                    for key in ATTACK_PATTERNS:
                        if key in line:
                            ip = _extract_ip(line)
                            log, shield, fund = _absorb_attack(key, "REDOMA-ALPHA", ip)
                            print(f"[{log['timestamp']}] REAL | {key}")
                            _print_shield_status(log, shield, fund)
                            break
            except Exception:
                pass

            # Simula eventos dos nos nacionais em standby (rede emaranhada)
            if random.random() < 0.3:
                node_name = random.choice(
                    [n for n in REDOMA_NODES if n != "REDOMA-ALPHA"]
                )
                pattern = random.choice(list(ATTACK_PATTERNS.keys()))
                ip = f"{random.randint(1,254)}.{random.randint(0,254)}.{random.randint(0,254)}.{random.randint(1,254)}"
                log, shield, fund = _absorb_attack(pattern, node_name, ip)
                print(f"[{log['timestamp']}] REDE  | {node_name} | {pattern}")
                _print_shield_status(log, shield, fund)

            time.sleep(random.uniform(3, 8))

    except KeyboardInterrupt:
        proc.terminate()
        shield = _load_shield()
        fund = _load_fund()
        total = sum(fund.values())
        print(f"\nEscudo suspenso.")
        print(f"Ataques absorvidos: {shield['total_attacks_absorbed']}")
        print(f"Materia Escura em reserva: {shield['dark_matter_reserve_yw']:.1f} YW")
        print(f"Fundo Soberania Sul Global: {total:.1f} YW")
        print("O territorio esta protegido.")
    finally:
        proc.terminate()


if __name__ == "__main__":
    run()
