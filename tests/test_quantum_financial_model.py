import json
import os
import sys
import math

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "core"))
import quantum_financial_model as qfm


def _temp_vault(tmp_path):
    vault = str(tmp_path / "quantum_world")
    os.makedirs(vault, exist_ok=True)
    qfm.VAULT_DIR      = vault
    qfm.FINANCIAL_PATH = os.path.join(vault, "financial_risk_model.json")
    qfm.RISK_LOG_PATH  = os.path.join(vault, "split_payment_risk.jsonl")


class TestZenoEffect:
    def test_collapse_zero_when_no_float(self):
        assert qfm.quantum_zeno_collapse(0, 30) == 0.0

    def test_collapse_increases_with_float_days(self):
        p1 = qfm.quantum_zeno_collapse(30, 30)
        p2 = qfm.quantum_zeno_collapse(60, 30)
        assert p2 > p1

    def test_collapse_higher_with_frequent_measurement(self):
        p_pre  = qfm.quantum_zeno_collapse(42, 30)
        p_post = qfm.quantum_zeno_collapse(42, 1)
        assert p_post > p_pre

    def test_amplification_pos_greater_than_one(self):
        amp = qfm.zeno_amplification(42)
        assert amp > 1.0

    def test_amplification_shorter_float_higher_ratio(self):
        # Float menor => pre-Zeno ainda nao saturado => razao pos/pre maior
        a30 = qfm.zeno_amplification(30)
        a45 = qfm.zeno_amplification(45)
        assert a30 >= a45

    def test_collapse_bounded_0_1(self):
        for days in [1, 10, 30, 42, 100]:
            p = qfm.quantum_zeno_collapse(days, 1)
            assert 0.0 <= p <= 1.0


class TestHamiltonian:
    def test_returns_4x4(self):
        H = qfm.build_hamiltonian(False, 38, True)
        assert len(H) == 4
        for row in H:
            assert len(row) == 4

    def test_falencia_row_is_absorbing(self):
        H = qfm.build_hamiltonian(True, 42, True)
        assert H[3] == [0.0, 0.0, 0.0, 1.0]

    def test_split_payment_increases_deterioration(self):
        H_no  = qfm.build_hamiltonian(False, 42, False)
        H_yes = qfm.build_hamiltonian(True,  42, False)
        # Transicao SOLVENTE -> ALERTA deve ser maior com Split Payment
        assert H_yes[0][1] > H_no[0][1]

    def test_sovereignty_reduces_risk(self):
        H_no_sov  = qfm.build_hamiltonian(True, 42, False)
        H_with_sov = qfm.build_hamiltonian(True, 42, True)
        assert H_with_sov[0][1] <= H_no_sov[0][1]

    def test_rows_sum_to_one(self):
        for sp in (True, False):
            for sov in (True, False):
                H = qfm.build_hamiltonian(sp, 38, sov)
                for i, row in enumerate(H):
                    assert abs(sum(row) - 1.0) < 1e-9, f"Linha {i} nao soma 1 (sp={sp},sov={sov}): {row}"

    def test_no_negative_values(self):
        H = qfm.build_hamiltonian(True, 45, True)
        for row in H:
            for v in row:
                assert v >= 0.0


class TestEvolveState:
    def test_output_length_4(self):
        H    = qfm.build_hamiltonian(False, 38)
        probs = qfm.evolve_state([0.7, 0.25, 0.04, 0.01], H, steps=12)
        assert len(probs) == 4

    def test_sums_to_one(self):
        H    = qfm.build_hamiltonian(True, 42)
        probs = qfm.evolve_state([0.7, 0.25, 0.04, 0.01], H, steps=12)
        assert abs(sum(probs) - 1.0) < 1e-5

    def test_all_nonnegative(self):
        H    = qfm.build_hamiltonian(True, 42)
        probs = qfm.evolve_state([0.7, 0.25, 0.04, 0.01], H, steps=12)
        assert all(p >= 0.0 for p in probs)

    def test_absorbing_state_grows(self):
        H    = qfm.build_hamiltonian(True, 42, False)
        probs = qfm.evolve_state([0.7, 0.25, 0.04, 0.01], H, steps=24)
        assert probs[qfm.STATE_FALENCIA] >= 0.01

    def test_split_payment_increases_falencia(self):
        H_no  = qfm.build_hamiltonian(False, 42)
        H_yes = qfm.build_hamiltonian(True,  42, False)
        p_no  = qfm.evolve_state([0.7, 0.25, 0.04, 0.01], H_no,  steps=12)
        p_yes = qfm.evolve_state([0.7, 0.25, 0.04, 0.01], H_yes, steps=12)
        insolvency_no  = p_no[2]  + p_no[3]
        insolvency_yes = p_yes[2] + p_yes[3]
        assert insolvency_yes >= insolvency_no

    def test_zero_steps_returns_initial(self):
        H     = qfm.build_hamiltonian(False, 38)
        init  = [0.7, 0.25, 0.04, 0.01]
        probs = qfm.evolve_state(init, H, steps=0)
        for a, b in zip(probs, init):
            assert abs(a - b) < 1e-9


class TestRiskMetrics:
    def test_returns_required_fields(self, tmp_path):
        _temp_vault(tmp_path)
        m = qfm.calculate_risk_metrics("MOONDO-Biotech-Bioreator", True, True)
        required = [
            "sector", "bioma", "split_payment_active", "sovereignty_active",
            "float_days_lost", "ibs_cbs_rate", "zeno_collapse_pre",
            "zeno_collapse_post", "zeno_amplification", "final_state",
            "p_insolvency", "capital_at_risk_m_brl", "float_cost_m_brl",
            "sovereignty_score", "slippery_slope_risk",
        ]
        for f in required:
            assert f in m, f"Campo ausente: {f}"

    def test_p_insolvency_bounded(self, tmp_path):
        _temp_vault(tmp_path)
        m = qfm.calculate_risk_metrics("MOONDO-Biotech-Bioreator", True, True)
        assert 0.0 <= m["p_insolvency"] <= 1.0

    def test_capital_at_risk_positive(self, tmp_path):
        _temp_vault(tmp_path)
        m = qfm.calculate_risk_metrics("MOONDO-Biotech-Bioreator", True, False)
        assert m["capital_at_risk_m_brl"] > 0.0

    def test_sovereignty_reduces_insolvency_risk(self, tmp_path):
        _temp_vault(tmp_path)
        m_no  = qfm.calculate_risk_metrics("MOONDO-Biotech-Bioreator", True, False)
        m_yes = qfm.calculate_risk_metrics("MOONDO-Biotech-Bioreator", True, True)
        assert m_yes["p_insolvency"] <= m_no["p_insolvency"]

    def test_split_payment_increases_risk(self, tmp_path):
        _temp_vault(tmp_path)
        m_pre = qfm.calculate_risk_metrics("MOONDO-Biotech-Bioreator", False, True)
        m_pos = qfm.calculate_risk_metrics("MOONDO-Biotech-Bioreator", True,  True)
        assert m_pos["p_insolvency"] >= m_pre["p_insolvency"]

    def test_final_state_has_four_labels(self, tmp_path):
        _temp_vault(tmp_path)
        m = qfm.calculate_risk_metrics("MOONDO-Biotech-Bioreator", True, True)
        for label in qfm.STATE_LABELS:
            assert label in m["final_state"]

    def test_final_state_sums_to_one(self, tmp_path):
        _temp_vault(tmp_path)
        m = qfm.calculate_risk_metrics("MOONDO-Biotech-Bioreator", True, True)
        total = sum(m["final_state"].values())
        assert abs(total - 1.0) < 1e-4

    def test_slippery_slope_bounded(self, tmp_path):
        _temp_vault(tmp_path)
        m = qfm.calculate_risk_metrics("MOONDO-Biotech-Bioreator", True, True)
        assert 0.0 <= m["slippery_slope_risk"] <= qfm.SLIPPERY_SLOPE_PROB

    def test_all_sectors_computable(self, tmp_path):
        _temp_vault(tmp_path)
        for sector in qfm.AGRO_SECTORS:
            m = qfm.calculate_risk_metrics(sector, True, True)
            assert m["p_insolvency"] >= 0.0


class TestFullAnalysis:
    def test_creates_financial_risk_file(self, tmp_path):
        _temp_vault(tmp_path)
        qfm.run_full_analysis(save=True)
        assert os.path.exists(qfm.FINANCIAL_PATH)

    def test_creates_risk_log(self, tmp_path):
        _temp_vault(tmp_path)
        qfm.run_full_analysis(save=True)
        assert os.path.exists(qfm.RISK_LOG_PATH)

    def test_summary_has_required_keys(self, tmp_path):
        _temp_vault(tmp_path)
        s = qfm.run_full_analysis(save=False)
        for key in ["sectors_analyzed", "total_capital_at_risk_m_brl",
                    "total_float_cost_m_brl", "capital_protected_by_sovereignty_m",
                    "quantum_zeno_effect_confirmed", "results"]:
            assert key in s

    def test_sectors_analyzed_equals_agro_sectors(self, tmp_path):
        _temp_vault(tmp_path)
        s = qfm.run_full_analysis(save=False)
        assert s["sectors_analyzed"] == len(qfm.AGRO_SECTORS)

    def test_sovereignty_always_reduces_total_risk(self, tmp_path):
        _temp_vault(tmp_path)
        s = qfm.run_full_analysis(save=False)
        assert s["capital_protected_by_sovereignty_m"] > 0.0

    def test_results_have_three_scenarios(self, tmp_path):
        _temp_vault(tmp_path)
        s = qfm.run_full_analysis(save=False)
        for sector_data in s["results"].values():
            assert "pre_split_payment" in sector_data
            assert "pos_split_payment_sem_soberania" in sector_data
            assert "pos_split_payment_com_soberania" in sector_data

    def test_json_is_valid_after_save(self, tmp_path):
        _temp_vault(tmp_path)
        qfm.run_full_analysis(save=True)
        with open(qfm.FINANCIAL_PATH) as f:
            data = json.load(f)
        assert data["quantum_zeno_effect_confirmed"] is True

    def test_log_entry_is_valid_jsonl(self, tmp_path):
        _temp_vault(tmp_path)
        qfm.run_full_analysis(save=True)
        with open(qfm.RISK_LOG_PATH) as f:
            entry = json.loads(f.readline())
        assert "total_risk_m" in entry
        assert "sovereignty_saved_m" in entry


class TestConstants:
    def test_ibs_cbs_rate_range(self):
        assert 0.20 <= qfm.IBS_CBS_RATE <= 0.35

    def test_slippery_slope_matches_literature(self):
        assert qfm.SLIPPERY_SLOPE_PROB == 0.75

    def test_sovereignty_shield_positive(self):
        assert 0.0 < qfm.SOVEREIGNTY_SHIELD_FACTOR < 1.0

    def test_four_sectors_defined(self):
        assert len(qfm.AGRO_SECTORS) == 4

    def test_moondo_present(self):
        assert any("MOONDO" in s for s in qfm.AGRO_SECTORS)

    def test_four_state_labels(self):
        assert len(qfm.STATE_LABELS) == 4

    def test_float_days_agro_matches_sector(self):
        assert qfm.AGRO_SECTORS["MOONDO-Biotech-Bioreator"]["float_days"] == 42
