"""
TDD RED — synapse_quantum_bridge.py
Bridge Claude Code ↔ Antigravity via vault JSONs compartilhados.
"""
import os
import json
import pytest
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

VAULT = "/opt/synapse_vault"
QUANTUM_WORLD = os.path.join(VAULT, "quantum_world")


def test_read_colony_status():
    """read_colony() deve retornar dict com colony_state e ton618_active."""
    from synapse_quantum_bridge import read_colony
    colony = read_colony()
    assert isinstance(colony, dict), "read_colony deve retornar dict"
    assert "colony_state" in colony, "colony_state ausente"
    assert "ton618_active" in colony, "ton618_active ausente"
    assert colony["ton618_active"] is True, "TON618 deve estar ativo"


def test_read_pheromones():
    """read_pheromones() deve retornar dict com as 5 REDOMAs."""
    from synapse_quantum_bridge import read_pheromones
    ph = read_pheromones()
    assert isinstance(ph, dict), "read_pheromones deve retornar dict"
    for r in ["REDOMA-ALPHA", "REDOMA-BETA", "REDOMA-GAMMA", "REDOMA-DELTA", "REDOMA-EPSILON"]:
        assert r in ph, f"{r} ausente em pheromones"


def test_write_agent_ping(tmp_path):
    """ping_sentinel() deve escrever linha JSON válida no log."""
    from synapse_quantum_bridge import ping_sentinel
    log_file = str(tmp_path / "test_traces.log")
    ping_sentinel("Teste TDD", task_n=0, log_path=log_file)
    with open(log_file) as f:
        lines = f.readlines()
    assert len(lines) >= 1, "Nenhuma linha escrita no log"
    data = json.loads(lines[-1].strip())
    assert data["agent"] == "CLAUDE_CODE", "Campo agent ausente ou errado"
    assert "agent_msg" in data, "Campo agent_msg ausente"
    assert "timestamp" in data, "Campo timestamp ausente"


def test_get_active_stones():
    """get_active_stones() deve retornar lista com pedras do último registro da sentinela."""
    from synapse_quantum_bridge import get_active_stones
    stones = get_active_stones()
    assert isinstance(stones, list), "get_active_stones deve retornar lista"
    assert len(stones) > 0, "Lista de pedras não pode ser vazia"


def test_handshake_protocol():
    """handshake() deve retornar bool indicando estado do agente."""
    from synapse_quantum_bridge import handshake
    result = handshake("CLAUDE_CODE")
    assert isinstance(result, bool), "handshake deve retornar bool"


def test_sovereign_fund_total():
    """get_sovereignty_fund() deve retornar float > 80_000_000."""
    from synapse_quantum_bridge import get_sovereignty_fund
    total = get_sovereignty_fund()
    assert isinstance(total, float), "get_sovereignty_fund deve retornar float"
    assert total > 80_000_000, f"Fundo soberano abaixo do esperado: {total}"
