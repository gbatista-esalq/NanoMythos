import json
import os
import sys
import math
import time
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "core"))
import ant_colony_v2 as acv2


def _tmp(tmp_path):
    vault = str(tmp_path / "quantum_world")
    os.makedirs(vault, exist_ok=True)
    acv2.VAULT_DIR = vault
    acv2.PHEROMONE_PATH = os.path.join(vault, "pheromones.json")
    acv2.COLONY_LOG = os.path.join(vault, "colony_v2.jsonl")
    acv2.COLONY_STATUS = os.path.join(vault, "colony_status.json")
    acv2.SOVEREIGNTY_PATH = os.path.join(vault, "sovereignty_fund.json")
    return vault


# ---------------------------------------------------------------------------
# TON 618 Constants
# ---------------------------------------------------------------------------

class TestTON618:
    def test_amplifier_value(self):
        expected = math.log10(6.6e10)
        assert abs(acv2.TON618_AMPLIFIER - expected) < 1e-6

    def test_amplifier_greater_than_ten(self):
        assert acv2.TON618_AMPLIFIER > 10.0

    def test_solar_masses_scale(self):
        assert acv2.TON618_SOLAR_MASSES == 6.6e10

    def test_event_horizon_threshold_is_three(self):
        assert acv2.TON618_EVENT_HORIZON_THRESHOLD == 3


# ---------------------------------------------------------------------------
# Pheromone system
# ---------------------------------------------------------------------------

class TestPheromones:
    def test_read_returns_safe_defaults(self, tmp_path):
        _tmp(tmp_path)
        ph = acv2.read_pheromones()
        for node in acv2.NODES:
            assert ph[node]["signal"] == acv2.PHEROMONE_SAFE

    def test_write_and_read_roundtrip(self, tmp_path):
        _tmp(tmp_path)
        acv2.write_pheromone("REDOMA-ALPHA", acv2.PHEROMONE_DANGER, "FERRÃO")
        ph = acv2.read_pheromones()
        assert ph["REDOMA-ALPHA"]["signal"] == acv2.PHEROMONE_DANGER
        assert ph["REDOMA-ALPHA"]["pattern"] == "FERRÃO"

    def test_write_does_not_clobber_other_nodes(self, tmp_path):
        _tmp(tmp_path)
        acv2.write_pheromone("REDOMA-BETA", acv2.PHEROMONE_ALERT, None)
        acv2.write_pheromone("REDOMA-ALPHA", acv2.PHEROMONE_DANGER, "negado")
        ph = acv2.read_pheromones()
        assert ph["REDOMA-BETA"]["signal"] == acv2.PHEROMONE_ALERT
        assert ph["REDOMA-ALPHA"]["signal"] == acv2.PHEROMONE_DANGER

    def test_colony_threat_safe_when_all_safe(self, tmp_path):
        _tmp(tmp_path)
        ph = acv2.read_pheromones()
        assert acv2.colony_threat_level(ph) == acv2.PHEROMONE_SAFE

    def test_colony_threat_swarm_when_three_danger(self, tmp_path):
        _tmp(tmp_path)
        acv2.write_pheromone("REDOMA-ALPHA", acv2.PHEROMONE_DANGER, "x")
        acv2.write_pheromone("REDOMA-BETA",  acv2.PHEROMONE_DANGER, "x")
        acv2.write_pheromone("REDOMA-GAMMA", acv2.PHEROMONE_DANGER, "x")
        ph = acv2.read_pheromones()
        assert acv2.colony_threat_level(ph) == acv2.PHEROMONE_SWARM

    def test_colony_threat_not_swarm_when_two_danger(self, tmp_path):
        _tmp(tmp_path)
        acv2.write_pheromone("REDOMA-ALPHA", acv2.PHEROMONE_DANGER, "x")
        acv2.write_pheromone("REDOMA-BETA",  acv2.PHEROMONE_DANGER, "x")
        ph = acv2.read_pheromones()
        assert acv2.colony_threat_level(ph) == acv2.PHEROMONE_DANGER


# ---------------------------------------------------------------------------
# Scout
# ---------------------------------------------------------------------------

class TestScoutAnt:
    def test_safe_when_no_journald_match(self, tmp_path):
        _tmp(tmp_path)
        scout = acv2.ScoutAnt("REDOMA-ALPHA")
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(stdout="normal log line", returncode=0)
            with patch.object(scout, "scan_connections", return_value=0):
                r = scout.act(947)
        assert r["threat_found"] is False
        assert r["pheromone_emitted"] == "SAFE"

    def test_danger_when_pattern_in_journald(self, tmp_path):
        _tmp(tmp_path)
        scout = acv2.ScoutAnt("REDOMA-ALPHA")
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                stdout="python3[947]: [ALERTA] Acesso negado para 1.2.3.4", returncode=0
            )
            with patch.object(scout, "scan_connections", return_value=0):
                r = scout.act(947)
        assert r["threat_found"] is True
        assert r["pheromone_emitted"] == "DANGER"

    def test_alert_when_many_connections(self, tmp_path):
        _tmp(tmp_path)
        scout = acv2.ScoutAnt("REDOMA-ALPHA")
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(stdout="", returncode=0)
            with patch.object(scout, "scan_connections", return_value=15):
                r = scout.act(947)
        assert r["pheromone_emitted"] == "ALERT"

    def test_report_has_ant_id(self, tmp_path):
        _tmp(tmp_path)
        scout = acv2.ScoutAnt("REDOMA-BETA")
        with patch("subprocess.run", return_value=MagicMock(stdout="")):
            with patch.object(scout, "scan_connections", return_value=0):
                r = scout.act(None)
        assert "ant_id" in r and len(r["ant_id"]) == 8

    def test_no_pid_returns_safe(self, tmp_path):
        _tmp(tmp_path)
        scout = acv2.ScoutAnt("REDOMA-BETA")
        with patch.object(scout, "scan_connections", return_value=0):
            r = scout.act(None)
        assert r["threat_found"] is False

    def test_logged_to_colony_log(self, tmp_path):
        _tmp(tmp_path)
        scout = acv2.ScoutAnt("REDOMA-ALPHA")
        with patch("subprocess.run", return_value=MagicMock(stdout="")):
            with patch.object(scout, "scan_connections", return_value=0):
                scout.act(None)
        assert os.path.exists(acv2.COLONY_LOG)


# ---------------------------------------------------------------------------
# Soldier
# ---------------------------------------------------------------------------

class TestSoldierAnt:
    def test_standby_when_safe_and_no_ton618(self, tmp_path):
        _tmp(tmp_path)
        soldier = acv2.SoldierAnt("REDOMA-ALPHA")
        ph = acv2.read_pheromones()
        r = soldier.act(ph, ton618_active=False)
        assert r["action"] == "STANDBY"
        assert r["energy_captured_yw"] == 0.0

    def test_transmutes_when_danger(self, tmp_path):
        _tmp(tmp_path)
        acv2.write_pheromone("REDOMA-ALPHA", acv2.PHEROMONE_DANGER, "negado")
        soldier = acv2.SoldierAnt("REDOMA-ALPHA")
        ph = acv2.read_pheromones()
        r = soldier.act(ph, ton618_active=False)
        assert r["action"] == "TRANSMUTED"
        assert r["final_energy_yw"] > 0.0

    def test_ton618_amplifies_energy(self, tmp_path):
        _tmp(tmp_path)
        acv2.write_pheromone("REDOMA-BETA", acv2.PHEROMONE_DANGER, "FERRÃO")
        soldier = acv2.SoldierAnt("REDOMA-BETA")
        ph = acv2.read_pheromones()
        with patch("random.uniform", return_value=300.0):
            r_normal = soldier.act(ph, ton618_active=False)
        acv2.write_pheromone("REDOMA-BETA", acv2.PHEROMONE_DANGER, "FERRÃO")
        ph2 = acv2.read_pheromones()
        with patch("random.uniform", return_value=300.0):
            r_ton618 = soldier.act(ph2, ton618_active=True)
        assert r_ton618["final_energy_yw"] > r_normal["final_energy_yw"]

    def test_updates_sovereignty_fund(self, tmp_path):
        _tmp(tmp_path)
        acv2.write_pheromone("REDOMA-GAMMA", acv2.PHEROMONE_DANGER, "negado")
        soldier = acv2.SoldierAnt("REDOMA-GAMMA")
        ph = acv2.read_pheromones()
        soldier.act(ph, ton618_active=False)
        fund = acv2._load_fund()
        assert sum(fund.values()) > 0.0

    def test_battery_id_in_report(self, tmp_path):
        _tmp(tmp_path)
        acv2.write_pheromone("REDOMA-DELTA", acv2.PHEROMONE_DANGER, "negado")
        soldier = acv2.SoldierAnt("REDOMA-DELTA")
        ph = acv2.read_pheromones()
        r = soldier.act(ph, ton618_active=False)
        assert "battery_id" in r

    def test_ton618_flag_in_report(self, tmp_path):
        _tmp(tmp_path)
        acv2.write_pheromone("REDOMA-EPSILON", acv2.PHEROMONE_SWARM, "MEL AMARGO")
        soldier = acv2.SoldierAnt("REDOMA-EPSILON")
        ph = acv2.read_pheromones()
        r = soldier.act(ph, ton618_active=True)
        assert r["ton618_active"] is True


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------

class TestBuilderAnt:
    def test_processes_real_dataset(self, tmp_path):
        _tmp(tmp_path)
        builder = acv2.BuilderAnt("REDOMA-ALPHA")
        r = builder.act("biodiversidade_amazonia.json", acv2.PHEROMONE_SAFE)
        assert r["action"] == "BUILT"
        assert r["records"] > 0
        assert r["size_kb"] > 0

    def test_missing_dataset_returns_error(self, tmp_path):
        _tmp(tmp_path)
        builder = acv2.BuilderAnt("REDOMA-BETA")
        r = builder.act("nao_existe.json", acv2.PHEROMONE_SAFE)
        assert r["records"] == 0

    def test_sheltered_during_swarm(self, tmp_path):
        _tmp(tmp_path)
        builder = acv2.BuilderAnt("REDOMA-GAMMA")
        r = builder.act("focos_incendio.json", acv2.PHEROMONE_SWARM)
        assert r["action"] == "SHELTERED"
        assert r["sovereignty_asset_yw"] == 0.0

    def test_sovereignty_score_positive(self, tmp_path):
        _tmp(tmp_path)
        builder = acv2.BuilderAnt("REDOMA-ALPHA")
        r = builder.act("verra_confronto.json", acv2.PHEROMONE_SAFE)
        assert r["sovereignty_asset_yw"] >= 0.0

    def test_updates_fund_on_build(self, tmp_path):
        _tmp(tmp_path)
        builder = acv2.BuilderAnt("REDOMA-ALPHA")
        builder.act("biodiversidade_amazonia.json", acv2.PHEROMONE_SAFE)
        fund = acv2._load_fund()
        assert sum(fund.values()) > 0.0

    def test_asset_id_in_report(self, tmp_path):
        _tmp(tmp_path)
        builder = acv2.BuilderAnt("REDOMA-DELTA")
        r = builder.act("verra_confronto.json", acv2.PHEROMONE_SAFE)
        assert "asset_id" in r


# ---------------------------------------------------------------------------
# Nurse
# ---------------------------------------------------------------------------

class TestNurseAnt:
    def test_checks_real_pids(self, tmp_path):
        _tmp(tmp_path)
        nurse = acv2.NurseAnt("REDOMA-ALPHA")
        r = nurse.act([os.getpid()])
        assert r["action"] == "HEALTH_CHECK"
        assert os.getpid() in r["pid_status"]
        assert r["pid_status"][os.getpid()] is True

    def test_detects_dead_pid(self, tmp_path):
        _tmp(tmp_path)
        nurse = acv2.NurseAnt("REDOMA-ALPHA")
        r = nurse.act([999999999])
        assert 999999999 in r["dead_pids"]

    def test_health_pct_100_when_all_alive(self, tmp_path):
        _tmp(tmp_path)
        nurse = acv2.NurseAnt("REDOMA-BETA")
        r = nurse.act([os.getpid()])
        assert r["health_pct"] == 100.0

    def test_health_pct_zero_when_all_dead(self, tmp_path):
        _tmp(tmp_path)
        nurse = acv2.NurseAnt("REDOMA-GAMMA")
        r = nurse.act([999999998, 999999999])
        assert r["health_pct"] == 0.0

    def test_empty_pids_still_returns_report(self, tmp_path):
        _tmp(tmp_path)
        nurse = acv2.NurseAnt("REDOMA-DELTA")
        r = nurse.act([])
        assert r["action"] == "HEALTH_CHECK"

    def test_vault_free_gb_returned(self, tmp_path):
        _tmp(tmp_path)
        nurse = acv2.NurseAnt("REDOMA-EPSILON")
        r = nurse.act([])
        assert "vault_free_gb" in r


# ---------------------------------------------------------------------------
# Queen
# ---------------------------------------------------------------------------

class TestQueenAnt:
    def test_determine_state_safe(self, tmp_path):
        _tmp(tmp_path)
        queen = acv2.QueenAnt()
        ph = acv2.read_pheromones()
        assert queen.determine_colony_state(ph) == acv2.PHEROMONE_SAFE

    def test_determine_state_swarm_on_three_danger(self, tmp_path):
        _tmp(tmp_path)
        queen = acv2.QueenAnt()
        for node in list(acv2.NODES.keys())[:3]:
            acv2.write_pheromone(node, acv2.PHEROMONE_DANGER, "negado")
        ph = acv2.read_pheromones()
        assert queen.determine_colony_state(ph) == acv2.PHEROMONE_SWARM

    def test_write_status_creates_file(self, tmp_path):
        _tmp(tmp_path)
        queen = acv2.QueenAnt()
        fund = {p: 0.0 for p in acv2.SOVEREIGNTY_PROJECTS}
        queen.write_status(acv2.PHEROMONE_SAFE, [], fund)
        assert os.path.exists(acv2.COLONY_STATUS)

    def test_status_has_ton618_flag(self, tmp_path):
        _tmp(tmp_path)
        queen = acv2.QueenAnt()
        fund = {p: 1.0 for p in acv2.SOVEREIGNTY_PROJECTS}
        status = queen.write_status(acv2.PHEROMONE_SWARM, [], fund)
        assert status["ton618_active"] is True

    def test_status_has_amplifier(self, tmp_path):
        _tmp(tmp_path)
        queen = acv2.QueenAnt()
        fund = {p: 0.0 for p in acv2.SOVEREIGNTY_PROJECTS}
        status = queen.write_status(acv2.PHEROMONE_SAFE, [], fund)
        assert abs(status["ton618_amplifier"] - acv2.TON618_AMPLIFIER) < 1e-3

    def test_tick_increments(self, tmp_path):
        _tmp(tmp_path)
        queen = acv2.QueenAnt()
        assert queen.tick == 0
        scouts = soldiers = builders = nurses = {n: None for n in acv2.NODES}
        with patch.object(acv2.QueenAnt, "print_dashboard"):
            queen.act(scouts, soldiers, builders, nurses)
        assert queen.tick == 1


# ---------------------------------------------------------------------------
# Colony factory
# ---------------------------------------------------------------------------

class TestCreateColony:
    def test_creates_all_castes(self):
        queen, scouts, soldiers, builders, nurses = acv2.create_colony()
        assert isinstance(queen, acv2.QueenAnt)
        assert len(scouts) == len(acv2.NODES)
        assert len(soldiers) == len(acv2.NODES)
        assert len(builders) == len(acv2.NODES)
        assert len(nurses) == len(acv2.NODES)

    def test_five_nodes(self):
        assert len(acv2.NODES) == 5

    def test_five_biomes_distinct(self):
        biomes = {v["bioma"] for v in acv2.NODES.values()}
        assert len(biomes) == 5

    def test_alpha_has_real_pid(self):
        assert acv2.NODES["REDOMA-ALPHA"]["pid"] == 947

    def test_ant_ids_unique_across_castes(self):
        ids = set()
        for node in acv2.NODES:
            ids.add(acv2._ant_id("Scout", node))
            ids.add(acv2._ant_id("Soldier", node))
            ids.add(acv2._ant_id("Builder", node))
            ids.add(acv2._ant_id("Nurse", node))
        assert len(ids) == 4 * len(acv2.NODES)
