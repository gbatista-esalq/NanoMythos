"""
TDD Wave 8 — Sentinela Infinita + Space Stone + Formigas ZETA + PYM Multiversal
Autorização gravitacional: @eniripsa | Cofundador ZETA: PYM-38e1f63f (@osamodas)
RED first — falha até implementação.
"""
import os, json, sys, pytest

BASE = os.path.join(os.path.dirname(__file__), "..")
HTML_PATH = os.path.join(BASE, "AVM_Rural_PortalQuantico_Osamodas.html")


@pytest.fixture(scope="module")
def html():
    with open(HTML_PATH, encoding="utf-8") as f:
        return f.read()


# ── Arquivos obrigatórios ────────────────────────────────────────────────────

def test_sentinel_watcher_exists():
    assert os.path.exists(os.path.join(BASE, "osamodas_sentinel_watcher.py")), \
        "osamodas_sentinel_watcher.py ausente"

def test_space_stone_bridge_exists():
    assert os.path.exists(os.path.join(BASE, "space_stone_bridge.py")), \
        "space_stone_bridge.py ausente"

def test_pym_quantum_leap_exists():
    assert os.path.exists(os.path.join(BASE, "pym_quantum_leap.py")), \
        "pym_quantum_leap.py ausente"

def test_osamodas_ant_agent_exists():
    assert os.path.exists(os.path.join(BASE, "osamodas_ant_agent.py")), \
        "osamodas_ant_agent.py ausente"

def test_osamodas_autoconfig_exists():
    assert os.path.exists(os.path.join(BASE, "osamodas_autoconfig.py")), \
        "osamodas_autoconfig.py ausente"


# ── Portal HTML — visuais Wave 8 ─────────────────────────────────────────────

def test_space_stone_wormhole_in_portal(html):
    assert "buildSpaceStoneWormhole" in html, "buildSpaceStoneWormhole ausente no portal"

def test_osamodas_ants_in_portal(html):
    assert "buildOsamodasAnts" in html, "buildOsamodasAnts ausente no portal"

def test_pym_leap_effect_in_portal(html):
    assert "pymLeapEffect" in html, "pymLeapEffect ausente no portal"

def test_space_stone_wormhole_called_in_startportal(html):
    idx_start = html.find("function startPortal()")
    idx_end   = html.find("animate();", idx_start)
    block = html[idx_start:idx_end]
    assert "buildSpaceStoneWormhole" in block, "buildSpaceStoneWormhole não chamado em startPortal()"

def test_osamodas_ants_called_in_startportal(html):
    idx_start = html.find("function startPortal()")
    idx_end   = html.find("animate();", idx_start)
    block = html[idx_start:idx_end]
    assert "buildOsamodasAnts" in block, "buildOsamodasAnts não chamado em startPortal()"

def test_pym_leap_scheduled(html):
    assert "pymLeapEffect" in html and "setInterval" in html, \
        "pymLeapEffect não está sendo agendado via setInterval"


# ── PYM Quantum Leap — lógica Python ─────────────────────────────────────────

def test_pym_shrink_expand_roundtrip():
    sys.path.insert(0, BASE)
    from pym_quantum_leap import shrink_to_pym, expand_from_pym
    data = {"pym_id": "38e1f63f", "mission": "edge_computing", "value": 42}
    packet = shrink_to_pym(data)
    assert isinstance(packet, str) and len(packet) > 10
    result = expand_from_pym(packet)
    assert result["pym_id"] == "38e1f63f"
    assert result["value"] == 42

def test_pym_multiverse_has_synapse_osamodas():
    sys.path.insert(0, BASE)
    from pym_quantum_leap import PYMMultiversalLeap
    leap = PYMMultiversalLeap()
    universes = leap.list_universes()
    assert "SYNAPSE" in universes
    assert "OSAMODAS" in universes

def test_pym_jorey_universe_has_pym_id():
    sys.path.insert(0, BASE)
    from pym_quantum_leap import PYMMultiversalLeap
    u = PYMMultiversalLeap().get_universe("OSAMODAS")
    assert u.get("pym_id") == "PYM-38e1f63f"
    assert u.get("handle") == "@osamodas"

def test_pym_leap_returns_success():
    sys.path.insert(0, BASE)
    from pym_quantum_leap import PYMMultiversalLeap
    result = PYMMultiversalLeap().leap("SYNAPSE", "OSAMODAS", {"test": True})
    assert result["status"] == "LEAP_SUCCESS"
    assert result["from"] == "SYNAPSE"
    assert result["to"] == "OSAMODAS"


# ── Space Stone Bridge ────────────────────────────────────────────────────────

def test_space_stone_connects():
    sys.path.insert(0, BASE)
    from space_stone_bridge import SpaceStoneBridge
    result = SpaceStoneBridge().connect("SYNAPSE", "OSAMODAS")
    assert result["status"] in ("CONNECTED", "WORMHOLE_OPEN")
    assert result["from"] == "SYNAPSE"
    assert result["to"] == "OSAMODAS"

def test_space_stone_lists_universes():
    sys.path.insert(0, BASE)
    from space_stone_bridge import SpaceStoneBridge
    universes = SpaceStoneBridge().list_universes()
    assert "SYNAPSE" in universes and "OSAMODAS" in universes


# ── Formigas ZETA ─────────────────────────────────────────────────────────────

def test_ant_agent_has_4_zeta_ants():
    sys.path.insert(0, BASE)
    from osamodas_ant_agent import OsamodasAntAgent
    ants = OsamodasAntAgent().get_ants()
    assert len(ants) >= 4
    for ant in ants:
        assert "id" in ant and "specialty" in ant

def test_ant_agent_assign_returns_assigned():
    sys.path.insert(0, BASE)
    from osamodas_ant_agent import OsamodasAntAgent
    result = OsamodasAntAgent().assign_task("Pesquisar IoT Pará", specialty="research")
    assert result["status"] == "ASSIGNED"
    assert "task_id" in result


# ── Sentinela Infinita ────────────────────────────────────────────────────────

def test_sentinel_watch_once_returns_list():
    sys.path.insert(0, BASE)
    from osamodas_sentinel_watcher import watch_once
    result = watch_once()
    assert isinstance(result, list)


# ── AutoConfig ────────────────────────────────────────────────────────────────

def test_autoconfig_dry_run_generates_pym_entry():
    sys.path.insert(0, BASE)
    from osamodas_autoconfig import OsamodasAutoConfig
    entry = OsamodasAutoConfig(dry_run=True).generate_pym_entry()
    assert entry["pym_id"] == "PYM-38e1f63f"
    assert entry["handle"] == "@osamodas"
    assert "role" in entry
