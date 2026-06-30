"""
TDD RED — ton618_colony_watcher.py
Watcher em tempo real da colônia TON618 / sentinela infinita.
"""
import os
import json
import pytest
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

TRACES_LOG = "/opt/synapse_vault/infinity_traces.log"


def test_watcher_reads_log():
    """get_last_lines() deve retornar lista de dicts parseados do log."""
    from ton618_colony_watcher import get_last_lines
    lines = get_last_lines(n=5)
    assert isinstance(lines, list), "get_last_lines deve retornar lista"
    assert len(lines) > 0, "Log da sentinela está vazio"
    for entry in lines:
        assert isinstance(entry, dict), "Cada entrada deve ser dict JSON"


def test_alert_on_redoma_alpha():
    """check_redoma_alerts() deve detectar REDOMA-ALPHA como ALERT nos pheromones."""
    from ton618_colony_watcher import check_redoma_alerts
    alerts = check_redoma_alerts()
    assert isinstance(alerts, list), "check_redoma_alerts deve retornar lista"
    # REDOMA-ALPHA tem signal=1 (ALERT) no pheromones.json atual
    assert len(alerts) >= 1, "REDOMA-ALPHA deveria estar em ALERT"


def test_dead_pids_extracted():
    """extract_dead_pids() deve extrair PIDs do pattern de REDOMA-ALPHA."""
    from ton618_colony_watcher import extract_dead_pids
    pids = extract_dead_pids()
    assert isinstance(pids, list), "extract_dead_pids deve retornar lista"


def test_watch_returns_iterations():
    """get_last_iteration() deve retornar int > 0."""
    from ton618_colony_watcher import get_last_iteration
    it = get_last_iteration()
    assert isinstance(it, int), "get_last_iteration deve retornar int"
    assert it > 0, "Iteração deve ser positiva"


def test_colony_state_parsed():
    """get_colony_state() deve retornar string de estado da colônia."""
    from ton618_colony_watcher import get_colony_state
    state = get_colony_state()
    assert isinstance(state, str), "get_colony_state deve retornar str"
    assert len(state) > 0, "Colony state vazio"
