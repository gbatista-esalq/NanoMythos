"""
TDD Wave 5 — Triarquia Soberana + Synapse Agent
RED: estes testes devem FALHAR antes da criação de synapse_agent.py
"""
import sys
import os
import json
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def test_triarquia_nodes_defined():
    from synapse_agent import ALPHA, BETA, GAMMA
    assert ALPHA.name == "Alpha"
    assert BETA.name == "Beta"
    assert GAMMA.name == "Gamma"
    assert ALPHA.role
    assert BETA.role
    assert GAMMA.role


def test_get_gamma_status_always_online():
    from synapse_agent import get_gamma_status
    status = get_gamma_status()
    assert status["node"] == "Gamma"
    assert status["status"] == "ONLINE"
    assert "claude" in status
    assert "gemini_model" in status


def test_get_alpha_status_returns_dict():
    from synapse_agent import get_alpha_status
    status = get_alpha_status()
    assert "node" in status
    assert status["node"] == "Alpha"
    assert "status" in status
    assert status["status"] in ("ONLINE", "IDLE", "OFFLINE")


def test_get_beta_status_returns_dict():
    from synapse_agent import get_beta_status
    status = get_beta_status()
    assert "node" in status
    assert status["node"] == "Beta"
    assert "status" in status


def test_get_infinity_kernel_state_returns_dict():
    from synapse_agent import get_infinity_kernel_state
    state = get_infinity_kernel_state()
    assert "iteration" in state
    assert "sovereign_power" in state
    assert "stones_active" in state
    assert isinstance(state["iteration"], int)


def test_get_arc_core_state_returns_dict():
    from synapse_agent import get_arc_core_state
    state = get_arc_core_state()
    assert "status" in state
    assert "final_power" in state


def test_get_social_agent_state_returns_dict():
    from synapse_agent import get_social_agent_state
    state = get_social_agent_state()
    assert "status" in state


def test_get_triarquia_state_has_all_nodes():
    from synapse_agent import get_triarquia_state
    state = get_triarquia_state()
    for key in ("alpha", "beta", "gamma", "infinity_kernel", "arc_core", "social_agent", "timestamp"):
        assert key in state, f"chave ausente: {key}"


def test_ignite_triarquia_returns_state():
    from synapse_agent import ignite_triarquia
    state = ignite_triarquia(silent=True)
    assert isinstance(state, dict)
    assert state["gamma"]["status"] == "ONLINE"


def test_bridge_has_get_triarquia_status():
    from synapse_quantum_bridge import get_triarquia_status
    status = get_triarquia_status()
    assert "alpha" in status
    assert "gamma" in status
    assert isinstance(status, dict)
