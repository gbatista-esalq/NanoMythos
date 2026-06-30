import json
import os
import sys
import time
import tempfile
import importlib
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "core"))
import quantum_battery_transmutator as qbt


def _temp_vault(tmp_path):
    vault = str(tmp_path / "quantum_world")
    os.makedirs(vault, exist_ok=True)
    qbt.VAULT_DIR = vault
    qbt.BATTERY_PATH = os.path.join(vault, "batteries.json")
    qbt.AUDIT_PATH = os.path.join(vault, "transmutation_audit.json")
    qbt.SOVEREIGNTY_PATH = os.path.join(vault, "sovereignty_fund.json")
    return vault


class TestEnsureDirs:
    def test_creates_vault_dir(self, tmp_path):
        vault = str(tmp_path / "new_world")
        qbt.VAULT_DIR = vault
        qbt.BATTERY_PATH = os.path.join(vault, "batteries.json")
        qbt.AUDIT_PATH = os.path.join(vault, "transmutation_audit.json")
        qbt.SOVEREIGNTY_PATH = os.path.join(vault, "sovereignty_fund.json")
        qbt._ensure_dirs()
        assert os.path.isdir(vault)


class TestSovereigntyFund:
    def test_load_returns_zeros_on_missing(self, tmp_path):
        _temp_vault(tmp_path)
        fund = qbt._load_sovereignty()
        assert all(v == 0.0 for v in fund.values())
        assert len(fund) == len(qbt.SOVEREIGNTY_PROJECTS)

    def test_save_and_load_roundtrip(self, tmp_path):
        _temp_vault(tmp_path)
        fund = {p: 99.9 for p in qbt.SOVEREIGNTY_PROJECTS}
        qbt._save_sovereignty(fund)
        loaded = qbt._load_sovereignty()
        assert loaded == fund

    def test_all_projects_present(self, tmp_path):
        _temp_vault(tmp_path)
        fund = qbt._load_sovereignty()
        for project in qbt.SOVEREIGNTY_PROJECTS:
            assert project in fund


class TestChargeBattery:
    def test_cell_has_required_fields(self, tmp_path):
        _temp_vault(tmp_path)
        cell = qbt._charge_battery("negado", "1.2.3.4", "raw line")
        required = [
            "battery_id", "charged_at", "source_vector", "source_ip",
            "label", "raw_charge_yw", "hawking_loss_yw", "net_energy_yw",
            "allocated_to", "status", "axiom",
        ]
        for field in required:
            assert field in cell, f"Campo ausente: {field}"

    def test_net_energy_less_than_raw(self, tmp_path):
        _temp_vault(tmp_path)
        cell = qbt._charge_battery("negado", "1.2.3.4", "")
        assert cell["net_energy_yw"] < cell["raw_charge_yw"]

    def test_hawking_loss_is_2_percent(self, tmp_path):
        _temp_vault(tmp_path)
        cell = qbt._charge_battery("negado", "1.2.3.4", "")
        expected_loss = round(cell["raw_charge_yw"] * qbt.HAWKING_LOSS, 4)
        assert abs(cell["hawking_loss_yw"] - expected_loss) < 0.01

    def test_status_is_charged(self, tmp_path):
        _temp_vault(tmp_path)
        cell = qbt._charge_battery("FERRÃO", "10.0.0.1", "")
        assert cell["status"] == "CHARGED"

    def test_battery_appended_to_file(self, tmp_path):
        _temp_vault(tmp_path)
        qbt._charge_battery("negado", "1.1.1.1", "")
        qbt._charge_battery("FERRÃO", "2.2.2.2", "")
        with open(qbt.BATTERY_PATH) as f:
            lines = [l for l in f if l.strip()]
        assert len(lines) == 2

    def test_audit_appended(self, tmp_path):
        _temp_vault(tmp_path)
        qbt._charge_battery("MEL AMARGO", "9.9.9.9", "")
        with open(qbt.AUDIT_PATH) as f:
            entry = json.loads(f.readline())
        assert entry["status"] == "TRANSMUTED"
        assert "output_energy_yw" in entry

    def test_sovereignty_fund_updated(self, tmp_path):
        _temp_vault(tmp_path)
        cell = qbt._charge_battery("FERRÃO", "5.5.5.5", "")
        fund = qbt._load_sovereignty()
        assert fund[cell["allocated_to"]] > 0.0

    def test_honeypot_charge_higher_than_denied(self, tmp_path):
        _temp_vault(tmp_path)
        with patch("random.uniform", side_effect=lambda lo, hi: hi):
            cell_denied = qbt._charge_battery("negado", "1.1.1.1", "")
            cell_honeypot = qbt._charge_battery("MEL AMARGO", "2.2.2.2", "")
        assert cell_honeypot["raw_charge_yw"] > cell_denied["raw_charge_yw"]

    def test_battery_id_is_16_chars(self, tmp_path):
        _temp_vault(tmp_path)
        cell = qbt._charge_battery("negado", "1.2.3.4", "")
        assert len(cell["battery_id"]) == 16

    def test_mel_amargo_variant_works(self, tmp_path):
        _temp_vault(tmp_path)
        cell = qbt._charge_battery("MEL_AMARGO", "3.3.3.3", "")
        assert cell["label"] == "ATACANTE_SUGADO"

    def test_multiple_charges_accumulate_fund(self, tmp_path):
        _temp_vault(tmp_path)
        for _ in range(5):
            qbt._charge_battery("negado", "1.1.1.1", "")
        fund = qbt._load_sovereignty()
        assert sum(fund.values()) > 0.0

    def test_allocated_project_is_valid(self, tmp_path):
        _temp_vault(tmp_path)
        cell = qbt._charge_battery("FERRÃO", "7.7.7.7", "")
        assert cell["allocated_to"] in qbt.SOVEREIGNTY_PROJECTS


class TestExtractIP:
    def test_extracts_ipv4(self):
        line = "python3[947]: [ALERTA] Acesso negado para 203.0.113.42 (Tentativa 3)"
        assert qbt._extract_ip(line) == "203.0.113.42"

    def test_returns_unknown_on_no_ip(self):
        assert qbt._extract_ip("linha sem IP") == "UNKNOWN"

    def test_extracts_first_ip_in_line(self):
        line = "IP 10.0.0.1 and 10.0.0.2 detected"
        assert qbt._extract_ip(line) == "10.0.0.1"


class TestAttackVectors:
    def test_all_keys_have_required_fields(self):
        for key, v in qbt.ATTACK_VECTORS.items():
            assert "name" in v
            assert "charge_range" in v
            assert "label" in v
            lo, hi = v["charge_range"]
            assert hi > lo > 0

    def test_ferrão_stronger_than_negado(self):
        lo_f, hi_f = qbt.ATTACK_VECTORS["FERRÃO"]["charge_range"]
        lo_n, hi_n = qbt.ATTACK_VECTORS["negado"]["charge_range"]
        assert lo_f > hi_n or hi_f > hi_n

    def test_honeypot_strongest(self):
        lo_h, hi_h = qbt.ATTACK_VECTORS["MEL AMARGO"]["charge_range"]
        lo_f, hi_f = qbt.ATTACK_VECTORS["FERRÃO"]["charge_range"]
        assert lo_h > lo_f


class TestSovereigntyProjects:
    def test_has_at_least_five_projects(self):
        assert len(qbt.SOVEREIGNTY_PROJECTS) >= 5

    def test_moondo_present(self):
        assert any("MOONDO" in p for p in qbt.SOVEREIGNTY_PROJECTS)

    def test_amazonia_present(self):
        assert any("Amazonia" in p or "Redoma" in p for p in qbt.SOVEREIGNTY_PROJECTS)
