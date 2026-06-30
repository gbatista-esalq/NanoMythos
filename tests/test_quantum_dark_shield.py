import json
import os
import sys
import time
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "core"))
import quantum_dark_shield as qds


def _temp_vault(tmp_path):
    vault = str(tmp_path / "quantum_world")
    os.makedirs(vault, exist_ok=True)
    qds.VAULT_DIR = vault
    qds.DARK_SHIELD_PATH = os.path.join(vault, "dark_shield.json")
    qds.ENTANGLEMENT_LOG = os.path.join(vault, "entanglement_log.jsonl")
    qds.SOVEREIGNTY_PATH = os.path.join(vault, "sovereignty_fund.json")


class TestShieldInit:
    def test_load_shield_creates_defaults(self, tmp_path):
        _temp_vault(tmp_path)
        shield = qds._load_shield()
        assert shield["status"] == "ACTIVE"
        assert shield["total_attacks_absorbed"] == 0
        assert "nodes_entangled" in shield

    def test_all_nodes_entangled_in_default(self, tmp_path):
        _temp_vault(tmp_path)
        shield = qds._load_shield()
        for node in qds.REDOMA_NODES:
            assert node in shield["nodes_entangled"]

    def test_save_and_load_shield(self, tmp_path):
        _temp_vault(tmp_path)
        shield = qds._load_shield()
        shield["pym_field_strength"] = 42.0
        qds._save_shield(shield)
        loaded = qds._load_shield()
        assert loaded["pym_field_strength"] == 42.0

    def test_last_update_refreshed_on_save(self, tmp_path):
        _temp_vault(tmp_path)
        shield = qds._load_shield()
        before = shield.get("last_update", "")
        time.sleep(0.01)
        qds._save_shield(shield)
        loaded = qds._load_shield()
        assert loaded["last_update"] >= before


class TestPymTransmute:
    def test_returns_required_fields(self, tmp_path):
        _temp_vault(tmp_path)
        result = qds._pym_transmute(100.0, "REDOMA-ALPHA")
        for field in ["pym_id", "molecule", "source_node", "raw_energy_yw",
                      "net_energy_yw", "dark_matter_yw", "compression_ratio", "project"]:
            assert field in result

    def test_dark_matter_is_multiplied(self, tmp_path):
        _temp_vault(tmp_path)
        result = qds._pym_transmute(100.0, "REDOMA-ALPHA")
        expected = round(100.0 * qds.DARK_MATTER_MULTIPLIER, 4)
        assert abs(result["dark_matter_yw"] - expected) < 0.01

    def test_net_energy_has_hawking_loss(self, tmp_path):
        _temp_vault(tmp_path)
        result = qds._pym_transmute(100.0, "REDOMA-ALPHA")
        assert result["net_energy_yw"] < result["raw_energy_yw"]

    def test_molecule_is_valid_pym(self, tmp_path):
        _temp_vault(tmp_path)
        result = qds._pym_transmute(50.0, "REDOMA-BETA")
        assert result["molecule"] in qds.PYM_MOLECULES

    def test_project_is_valid(self, tmp_path):
        _temp_vault(tmp_path)
        result = qds._pym_transmute(50.0, "REDOMA-GAMMA")
        assert result["project"] in qds.SOVEREIGNTY_PROJECTS


class TestAbsorbAttack:
    def test_updates_shield_attack_count(self, tmp_path):
        _temp_vault(tmp_path)
        qds._absorb_attack("negado", "REDOMA-ALPHA", "1.2.3.4")
        shield = qds._load_shield()
        assert shield["total_attacks_absorbed"] == 1

    def test_increments_pym_field(self, tmp_path):
        _temp_vault(tmp_path)
        qds._absorb_attack("FERRÃO", "REDOMA-ALPHA", "5.5.5.5")
        shield = qds._load_shield()
        assert shield["pym_field_strength"] > 0.0

    def test_dark_matter_reserve_grows(self, tmp_path):
        _temp_vault(tmp_path)
        qds._absorb_attack("MEL AMARGO", "REDOMA-BETA", "9.9.9.9")
        shield = qds._load_shield()
        assert shield["dark_matter_reserve_yw"] > 0.0

    def test_fund_updated(self, tmp_path):
        _temp_vault(tmp_path)
        qds._absorb_attack("negado", "REDOMA-ALPHA", "1.1.1.1")
        fund = qds._load_fund()
        assert sum(fund.values()) > 0.0

    def test_entanglement_log_written(self, tmp_path):
        _temp_vault(tmp_path)
        qds._absorb_attack("FERRÃO", "REDOMA-GAMMA", "2.2.2.2")
        with open(qds.ENTANGLEMENT_LOG) as f:
            entry = json.loads(f.readline())
        assert entry["source_node"] == "REDOMA-GAMMA"
        assert entry["threat_level"] == "MEDIUM"

    def test_shield_layers_calculated(self, tmp_path):
        _temp_vault(tmp_path)
        for _ in range(10):
            qds._absorb_attack("MEL AMARGO", "REDOMA-ALPHA", "1.1.1.1")
        shield = qds._load_shield()
        assert shield["shield_layers"] >= 1

    def test_multiple_nodes_accumulate_correctly(self, tmp_path):
        _temp_vault(tmp_path)
        for node in list(qds.REDOMA_NODES.keys())[:3]:
            qds._absorb_attack("negado", node, "10.0.0.1")
        shield = qds._load_shield()
        assert shield["total_attacks_absorbed"] == 3

    def test_log_has_shield_layers_after(self, tmp_path):
        _temp_vault(tmp_path)
        log, _, _ = qds._absorb_attack("negado", "REDOMA-DELTA", "3.3.3.3")
        assert "shield_layers_after" in log
        assert "total_fund_yw" in log


class TestNodes:
    def test_five_nodes_defined(self):
        assert len(qds.REDOMA_NODES) == 5

    def test_each_node_has_biome(self):
        for name, node in qds.REDOMA_NODES.items():
            assert "bioma" in node, f"Bioma ausente em {name}"

    def test_each_node_has_estado(self):
        for name, node in qds.REDOMA_NODES.items():
            assert "estado" in node

    def test_all_five_biomes_distinct(self):
        biomes = {n["bioma"] for n in qds.REDOMA_NODES.values()}
        assert len(biomes) == 5

    def test_alpha_has_real_pid(self):
        assert qds.REDOMA_NODES["REDOMA-ALPHA"]["pid"] is not None

    def test_dark_matter_multiplier_is_significant(self):
        assert qds.DARK_MATTER_MULTIPLIER > 1.0

    def test_five_pym_molecules(self):
        assert len(qds.PYM_MOLECULES) == 5
