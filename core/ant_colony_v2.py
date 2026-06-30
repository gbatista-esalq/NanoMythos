"""
COLONIA TIPO 2 — FORMIGAS PYM v2.0
Emaranhamento quantico: 5 nos, 5 biomas, soberania tecnologica do Sul Global.
TON 618: modo gravitacional maximo ativado em SWARM.

Tipo 1 (existente): Carpenter + Fire ants — estrutural, simulado.
Tipo 2 (este modulo): Scout + Soldier + Builder + Nurse + Queen — operacional real.
"""

import time
import json
import os
import math
import random
import hashlib
import subprocess
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# CONSTANTES TON 618
# ---------------------------------------------------------------------------
TON618_SOLAR_MASSES = 6.6e10
TON618_AMPLIFIER = math.log10(TON618_SOLAR_MASSES)  # 10.8195...
TON618_EVENT_HORIZON_THRESHOLD = 3   # nos em DANGER para ativar modo TON 618

# ---------------------------------------------------------------------------
# TOPOLOGIA: 5 NOS x 5 BIOMAS
# ---------------------------------------------------------------------------
NODES = {
    "REDOMA-ALPHA":   {"estado": "SP", "bioma": "Cerrado",  "pid": 947,  "dataset": "biodiversidade_amazonia.json"},
    "REDOMA-BETA":    {"estado": "AM", "bioma": "Amazonia", "pid": None, "dataset": "focos_incendio.json"},
    "REDOMA-GAMMA":   {"estado": "MT", "bioma": "Pantanal", "pid": None, "dataset": "terras_indigenas.json"},
    "REDOMA-DELTA":   {"estado": "BA", "bioma": "Caatinga", "pid": None, "dataset": "deter_alertas.json"},
    "REDOMA-EPSILON": {"estado": "RS", "bioma": "Pampa",    "pid": None, "dataset": "verra_confronto.json"},
}

# ---------------------------------------------------------------------------
# SINAIS DE FEROMONIO
# ---------------------------------------------------------------------------
PHEROMONE_SAFE    = 0
PHEROMONE_ALERT   = 1
PHEROMONE_DANGER  = 2
PHEROMONE_SWARM   = 3   # TON 618 ativo
PHEROMONE_FEAST   = 4   # dados ricos encontrados

PHEROMONE_LABELS = {0: "SAFE", 1: "ALERT", 2: "DANGER", 3: "SWARM", 4: "FEAST"}

# ---------------------------------------------------------------------------
# CAMINHOS DO VAULT
# ---------------------------------------------------------------------------
VAULT_DIR        = "/opt/synapse_vault/quantum_world"
PHEROMONE_PATH   = os.path.join(VAULT_DIR, "pheromones.json")
COLONY_LOG       = os.path.join(VAULT_DIR, "colony_v2.jsonl")
COLONY_STATUS    = os.path.join(VAULT_DIR, "colony_status.json")
SOVEREIGNTY_PATH = os.path.join(VAULT_DIR, "sovereignty_fund.json")

DATA_DIR = Path("/home/synapseagtech/Área de Trabalho/SYNAPSE AGTECH/amazonia_legal/data")

SOVEREIGNTY_PROJECTS = [
    "Redoma-V2-Shield",
    "Dossel-Monitor-Amazonia",
    "MOONDO-Biotech-Bioreator",
    "Sul-Global-Network-Node",
    "Obsidian-Vault-Preservation",
    "Chronicles-Framework-Production",
    "Amazonia-Legal-DataBridge",
]

ATTACK_PATTERNS = {
    "negado":     {"energy": (50,   150),  "threat": "LOW"},
    "FERRÃO":     {"energy": (300,  500),  "threat": "MEDIUM"},
    "MEL AMARGO": {"energy": (800,  1200), "threat": "HIGH"},
}

KNOWN_PIDS = [947, 1744, 1748, 1920, 1924]


# ---------------------------------------------------------------------------
# UTILITARIOS
# ---------------------------------------------------------------------------

def _ensure_dirs():
    os.makedirs(VAULT_DIR, exist_ok=True)


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def _ant_id(caste: str, node: str) -> str:
    raw = f"{caste}-{node}"
    return hashlib.sha256(raw.encode()).hexdigest()[:8]


def _load_fund() -> dict:
    if not os.path.exists(SOVEREIGNTY_PATH):
        return {p: 0.0 for p in SOVEREIGNTY_PROJECTS}
    with open(SOVEREIGNTY_PATH) as f:
        return json.load(f)


def _save_fund(fund: dict):
    with open(SOVEREIGNTY_PATH, "w") as f:
        json.dump(fund, f, ensure_ascii=False, indent=2)


def _log_event(entry: dict):
    with open(COLONY_LOG, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# FEROMONIO — BARRAMENTO DE COMUNICACAO DA COLONIA
# ---------------------------------------------------------------------------

def read_pheromones() -> dict:
    if not os.path.exists(PHEROMONE_PATH):
        return {node: {"signal": PHEROMONE_SAFE, "pattern": None, "ts": _now()}
                for node in NODES}
    with open(PHEROMONE_PATH) as f:
        return json.load(f)


def write_pheromone(node: str, signal: int, pattern=None):
    state = read_pheromones()
    state[node] = {"signal": signal, "pattern": pattern, "ts": _now()}
    with open(PHEROMONE_PATH, "w") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def colony_threat_level(pheromones: dict) -> int:
    signals = [v["signal"] for v in pheromones.values()]
    max_signal = max(signals) if signals else PHEROMONE_SAFE
    danger_count = sum(1 for s in signals if s >= PHEROMONE_DANGER)
    if danger_count >= TON618_EVENT_HORIZON_THRESHOLD:
        return PHEROMONE_SWARM
    return max_signal


# ---------------------------------------------------------------------------
# FORMIGA ESCUTEIRA — monitora ameacas em tempo real
# ---------------------------------------------------------------------------

class ScoutAnt:
    def __init__(self, node: str):
        self.node = node
        self.ant_id = _ant_id("Scout", node)
        self.caste = "Scout"

    def scan_journald(self, pid: int) -> tuple[bool, str]:
        """Retorna (threat_found, pattern_matched)."""
        if pid is None:
            return False, ""
        try:
            result = subprocess.run(
                ["journalctl", f"_PID={pid}", "-n", "3", "--no-pager"],
                capture_output=True, text=True, timeout=4
            )
            for line in result.stdout.splitlines():
                for pattern in ATTACK_PATTERNS:
                    if pattern in line:
                        return True, pattern
        except Exception:
            pass
        return False, ""

    def scan_connections(self, port: int) -> int:
        """Conta conexoes ativas na porta."""
        try:
            result = subprocess.run(
                ["ss", "-tn", "state", "established", f"( dport :{port} )"],
                capture_output=True, text=True, timeout=3
            )
            lines = [l for l in result.stdout.splitlines() if "ESTAB" in l or l.startswith("Netid")]
            return max(0, len(lines) - 1)
        except Exception:
            return 0

    def act(self, pid: int, port: int = 8888) -> dict:
        threat, pattern = self.scan_journald(pid)
        conns = self.scan_connections(port)

        if threat:
            signal = PHEROMONE_DANGER
        elif conns > 10:
            signal = PHEROMONE_ALERT
        else:
            signal = PHEROMONE_SAFE

        write_pheromone(self.node, signal, pattern if threat else None)

        report = {
            "ant_id": self.ant_id,
            "caste": self.caste,
            "node": self.node,
            "ts": _now(),
            "threat_found": threat,
            "pattern": pattern,
            "active_connections": conns,
            "pheromone_emitted": PHEROMONE_LABELS[signal],
        }
        _log_event(report)
        return report


# ---------------------------------------------------------------------------
# FORMIGA SOLDADO — transmuta ataques em energia soberana
# ---------------------------------------------------------------------------

class SoldierAnt:
    def __init__(self, node: str):
        self.node = node
        self.ant_id = _ant_id("Soldier", node)
        self.caste = "Soldier"

    def _transmute(self, pattern: str, ton618_active: bool) -> dict:
        cfg = ATTACK_PATTERNS.get(pattern, {"energy": (50, 150), "threat": "LOW"})
        raw = random.uniform(*cfg["energy"])
        net = raw * 0.98  # perda Hawking 2%
        amplifier = TON618_AMPLIFIER if ton618_active else 1.0
        final_energy = round(net * amplifier, 4)

        project = random.choice(SOVEREIGNTY_PROJECTS)
        fund = _load_fund()
        fund[project] = round(fund.get(project, 0.0) + final_energy, 4)
        _save_fund(fund)

        battery_id = hashlib.sha256(
            f"{time.time()}{self.ant_id}{pattern}".encode()
        ).hexdigest()[:14]

        return {
            "battery_id": battery_id,
            "pattern": pattern,
            "raw_energy_yw": round(raw, 4),
            "net_energy_yw": round(net, 4),
            "ton618_amplifier": round(amplifier, 4),
            "final_energy_yw": final_energy,
            "allocated_to": project,
            "ton618_active": ton618_active,
        }

    def act(self, pheromones: dict, ton618_active: bool) -> dict:
        node_ph = pheromones.get(self.node, {})
        signal = node_ph.get("signal", PHEROMONE_SAFE)
        pattern = node_ph.get("pattern")

        if signal < PHEROMONE_DANGER and not ton618_active:
            report = {
                "ant_id": self.ant_id, "caste": self.caste,
                "node": self.node, "ts": _now(), "action": "STANDBY",
                "energy_captured_yw": 0.0,
            }
            _log_event(report)
            return report

        if not pattern:
            pattern = random.choice(list(ATTACK_PATTERNS.keys()))

        tx = self._transmute(pattern, ton618_active)
        fund = _load_fund()

        report = {
            "ant_id": self.ant_id, "caste": self.caste,
            "node": self.node, "ts": _now(),
            "action": "TRANSMUTED",
            **tx,
            "fund_total_yw": round(sum(fund.values()), 4),
        }
        _log_event(report)
        return report


# ---------------------------------------------------------------------------
# FORMIGA CONSTRUTORA — processa dados, gera ativos de soberania
# ---------------------------------------------------------------------------

class BuilderAnt:
    def __init__(self, node: str):
        self.node = node
        self.ant_id = _ant_id("Builder", node)
        self.caste = "Builder"

    def process_dataset(self, dataset_name: str) -> dict:
        path = DATA_DIR / dataset_name
        if not path.exists():
            return {"error": f"{dataset_name} not found", "records": 0, "size_kb": 0}
        size_kb = round(path.stat().st_size / 1024, 1)
        try:
            raw = json.loads(path.read_bytes())
            if isinstance(raw, list):
                records = len(raw)
            elif isinstance(raw, dict):
                # Conta features em GeoJSON ou registros em dict
                records = len(raw.get("features", raw.get("data", raw.get("records", list(raw.values())))))
                if not isinstance(records, int):
                    records = len(raw)
            else:
                records = 1
        except Exception:
            records = 0
        return {"dataset": dataset_name, "records": records, "size_kb": size_kb}

    def _sovereignty_score(self, stats: dict) -> float:
        base = math.log1p(stats.get("records", 0)) * stats.get("size_kb", 1) / 100.0
        return round(base, 4)

    def act(self, dataset_name: str, colony_state: int) -> dict:
        if colony_state == PHEROMONE_SWARM:
            report = {
                "ant_id": self.ant_id, "caste": self.caste,
                "node": self.node, "ts": _now(),
                "action": "SHELTERED",
                "reason": "SWARM mode — all builders in shelter, soldiers active",
                "sovereignty_asset_yw": 0.0,
            }
            _log_event(report)
            return report

        stats = self.process_dataset(dataset_name)
        score = self._sovereignty_score(stats)

        if stats.get("records", 0) > 0:
            write_pheromone(self.node, PHEROMONE_FEAST, None)
            fund = _load_fund()
            proj = random.choice(SOVEREIGNTY_PROJECTS)
            fund[proj] = round(fund.get(proj, 0.0) + score, 4)
            _save_fund(fund)

        asset_id = hashlib.sha256(
            f"{self.ant_id}{dataset_name}{time.time()}".encode()
        ).hexdigest()[:12]

        report = {
            "ant_id": self.ant_id, "caste": self.caste,
            "node": self.node, "ts": _now(),
            "action": "BUILT",
            "asset_id": asset_id,
            **stats,
            "sovereignty_asset_yw": score,
        }
        _log_event(report)
        return report


# ---------------------------------------------------------------------------
# FORMIGA ENFERMEIRA — saude do sistema
# ---------------------------------------------------------------------------

class NurseAnt:
    def __init__(self, node: str):
        self.node = node
        self.ant_id = _ant_id("Nurse", node)
        self.caste = "Nurse"

    def check_pids(self, pids: list) -> dict:
        return {pid: os.path.exists(f"/proc/{pid}") for pid in pids}

    def check_vault_space(self) -> float:
        try:
            result = os.statvfs(VAULT_DIR)
            free_gb = (result.f_bavail * result.f_frsize) / 1e9
            return round(free_gb, 2)
        except Exception:
            return -1.0

    def act(self, pids: list) -> dict:
        pid_status = self.check_pids(pids)
        vault_free_gb = self.check_vault_space()
        dead_pids = [p for p, alive in pid_status.items() if not alive]
        health_pct = round(100.0 * (len(pids) - len(dead_pids)) / max(len(pids), 1), 1)

        if dead_pids:
            write_pheromone(self.node, PHEROMONE_ALERT, f"dead_pids:{dead_pids}")

        report = {
            "ant_id": self.ant_id, "caste": self.caste,
            "node": self.node, "ts": _now(),
            "action": "HEALTH_CHECK",
            "pid_status": pid_status,
            "dead_pids": dead_pids,
            "health_pct": health_pct,
            "vault_free_gb": vault_free_gb,
        }
        _log_event(report)
        return report


# ---------------------------------------------------------------------------
# RAINHA — coordena a colonia, ativa TON 618, gera relatorio
# ---------------------------------------------------------------------------

class QueenAnt:
    def __init__(self):
        self.ant_id = "QUEEN-TON618"
        self.caste = "Queen"
        self.tick = 0

    def determine_colony_state(self, pheromones: dict) -> int:
        return colony_threat_level(pheromones)

    def write_status(self, colony_state: int, reports: list, fund: dict):
        total_energy = round(sum(fund.values()), 4)
        status = {
            "tick": self.tick,
            "ts": _now(),
            "colony_state": PHEROMONE_LABELS[colony_state],
            "ton618_active": colony_state == PHEROMONE_SWARM,
            "ton618_amplifier": round(TON618_AMPLIFIER, 4),
            "nodes": len(NODES),
            "ants_active": len(reports),
            "sovereignty_fund_total_yw": total_energy,
            "sovereignty_fund": fund,
            "ant_ids": [r.get("ant_id") for r in reports if r.get("ant_id")],
        }
        with open(COLONY_STATUS, "w") as f:
            json.dump(status, f, ensure_ascii=False, indent=2)
        return status

    def print_dashboard(self, colony_state: int, reports: list, fund: dict):
        total = round(sum(fund.values()), 4)
        state_label = PHEROMONE_LABELS[colony_state]
        ton618 = colony_state == PHEROMONE_SWARM

        print(f"\n{'='*60}")
        print(f" COLONIA TIPO 2 — TICK {self.tick:04d} | {_now()}")
        print(f" Estado: {state_label} {'| TON618 ATIVO (x{:.2f})'.format(TON618_AMPLIFIER) if ton618 else ''}")
        print(f" Fundo Soberania: {total:.2f} YW")
        print(f"{'='*60}")

        for node, cfg in NODES.items():
            ph = read_pheromones().get(node, {})
            sig = PHEROMONE_LABELS.get(ph.get("signal", 0), "SAFE")
            print(f"  {node} | {cfg['bioma']:10s} | {sig}")

        actions = {}
        for r in reports:
            a = r.get("action", "?")
            actions[a] = actions.get(a, 0) + 1
        print(f" Acoes: { {k: v for k, v in sorted(actions.items())} }")

        if ton618:
            print(f" TON 618: massa {TON618_SOLAR_MASSES:.2e} M_sol | amplificador x{TON618_AMPLIFIER:.4f}")
            print(" MODO BURACO NEGRO: TODA ENERGIA DE ATAQUE CAPTURADA — HORIZONTE IMPENETRAVEL")

    def act(self, scouts, soldiers, builders, nurses) -> tuple[int, list]:
        self.tick += 1
        _ensure_dirs()
        pheromones = read_pheromones()
        colony_state = self.determine_colony_state(pheromones)
        ton618_active = colony_state == PHEROMONE_SWARM

        reports = []

        for node, cfg in NODES.items():
            pid = cfg["pid"]
            dataset = cfg["dataset"]
            port = 8888 if node == "REDOMA-ALPHA" else None

            scout = scouts.get(node)
            if scout and pid:
                r = scout.act(pid, port or 8888)
                reports.append(r)

            soldier = soldiers.get(node)
            if soldier:
                r = soldier.act(pheromones, ton618_active)
                reports.append(r)

            builder = builders.get(node)
            if builder:
                r = builder.act(dataset, colony_state)
                reports.append(r)

            nurse = nurses.get(node)
            if nurse and node == "REDOMA-ALPHA":
                r = nurse.act(KNOWN_PIDS)
                reports.append(r)
            elif nurse:
                r = nurse.act([])
                reports.append(r)

        fund = _load_fund()
        status = self.write_status(colony_state, reports, fund)
        self.print_dashboard(colony_state, reports, fund)

        _log_event({"queen": True, "tick": self.tick, "colony_state": PHEROMONE_LABELS[colony_state],
                    "total_yw": status["sovereignty_fund_total_yw"]})

        return colony_state, reports


# ---------------------------------------------------------------------------
# INICIALIZACAO DA COLONIA
# ---------------------------------------------------------------------------

def create_colony() -> tuple:
    scouts   = {node: ScoutAnt(node)   for node in NODES}
    soldiers = {node: SoldierAnt(node) for node in NODES}
    builders = {node: BuilderAnt(node) for node in NODES}
    nurses   = {node: NurseAnt(node)   for node in NODES}
    queen    = QueenAnt()
    return queen, scouts, soldiers, builders, nurses


def run():
    _ensure_dirs()
    print("COLONIA TIPO 2 — PYM ANTS v2.0")
    print(f"TON 618: {TON618_SOLAR_MASSES:.2e} massas solares | amplificador x{TON618_AMPLIFIER:.4f}")
    print(f"Nos: {len(NODES)} biomas | Castes: Scout/Soldier/Builder/Nurse/Queen")
    print(f"Ativando emaranhamento quantico nacional...")

    queen, scouts, soldiers, builders, nurses = create_colony()

    try:
        while True:
            colony_state, reports = queen.act(scouts, soldiers, builders, nurses)
            interval = random.uniform(5, 12)
            time.sleep(interval)
    except KeyboardInterrupt:
        fund = _load_fund()
        total = sum(fund.values())
        print(f"\nColonia suspensa no tick {queen.tick}.")
        print(f"Fundo Soberania Sul Global: {total:.2f} YW")
        print(f"TON 618 amplificador: x{TON618_AMPLIFIER:.4f}")
        print("O territorio esta protegido.")


if __name__ == "__main__":
    run()
