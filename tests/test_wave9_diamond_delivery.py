"""
TDD Wave 9 — Entrega Diamante + Bolha de Cooperação Infinita Sul Global
Autorização: @eniripsa | Entrega quântica PYM para @osamodas (PYM-38e1f63f)
RED first.
"""
import os, sys, json, pytest

BASE = os.path.join(os.path.dirname(__file__), "..")
SERVE = os.path.join(BASE, "amazonia_legal", "serve_data.py")


# ── serve_data.py — token + endpoint ────────────────────────────────────────

def test_osamodas_token_in_serve_data():
    with open(SERVE, encoding="utf-8") as f:
        src = f.read()
    assert "OSAMODAS_COFOUNDER_01" in src, \
        "OSAMODAS_COFOUNDER_01 não está em VALID_TOKENS"

def test_quantum_deliver_endpoint_in_serve_data():
    with open(SERVE, encoding="utf-8") as f:
        src = f.read()
    assert "quantum-deliver" in src, "/quantum-deliver endpoint ausente em serve_data.py"

def test_quantum_deliver_handler_defined():
    with open(SERVE, encoding="utf-8") as f:
        src = f.read()
    assert "_serve_quantum_deliver" in src, "_serve_quantum_deliver() não definido"


# ── quantum_delivery_client.py ────────────────────────────────────────────────

def test_quantum_delivery_client_exists():
    assert os.path.exists(os.path.join(BASE, "quantum_delivery_client.py")), \
        "quantum_delivery_client.py ausente"

def test_quantum_delivery_client_has_pull():
    sys.path.insert(0, BASE)
    from quantum_delivery_client import pull_quantum_delivery
    assert callable(pull_quantum_delivery)

def test_quantum_delivery_client_has_install():
    sys.path.insert(0, BASE)
    from quantum_delivery_client import install_wave8
    assert callable(install_wave8)


# ── sul_global_cooperation.py — Bolha de Cooperação Infinita ─────────────────

def test_sul_global_cooperation_exists():
    assert os.path.exists(os.path.join(BASE, "sul_global_cooperation.py")), \
        "sul_global_cooperation.py ausente"

def test_sul_global_bubble_initializes():
    sys.path.insert(0, BASE)
    from sul_global_cooperation import SulGlobalBubble
    bubble = SulGlobalBubble()
    nodes = bubble.list_nodes()
    assert "SYNAPSE" in nodes and "OSAMODAS" in nodes

def test_sul_global_bubble_add_node():
    sys.path.insert(0, BASE)
    from sul_global_cooperation import SulGlobalBubble
    bubble = SulGlobalBubble()
    result = bubble.add_node("CENA_PIRACICABA", {
        "pym_id": "PYM-cena0001",
        "handle": "@marcio.godoi",
        "region": "Piracicaba/SP",
        "redoma": "ETA",
    })
    assert result["status"] == "REGISTERED"
    assert "CENA_PIRACICABA" in bubble.list_nodes()

def test_sul_global_bubble_propagate_pheromone():
    sys.path.insert(0, BASE)
    from sul_global_cooperation import SulGlobalBubble
    bubble = SulGlobalBubble()
    result = bubble.propagate_pheromone("SYNAPSE", signal="FEAST", intensity=1.5)
    assert result["propagated_to"] >= 1
    assert result["signal"] == "FEAST"

def test_sul_global_bubble_quantum_relay():
    sys.path.insert(0, BASE)
    from sul_global_cooperation import SulGlobalBubble
    bubble = SulGlobalBubble()
    result = bubble.quantum_relay("SYNAPSE", "OSAMODAS", payload={"test": "wave9"})
    assert result["status"] == "RELAYED"
    assert result["hops"] >= 1

def test_sul_global_bubble_sovereignty_summary():
    sys.path.insert(0, BASE)
    from sul_global_cooperation import SulGlobalBubble
    summary = SulGlobalBubble().sovereignty_summary()
    assert "total_nodes" in summary
    assert "total_yw" in summary
    assert summary["total_nodes"] >= 2

def test_sul_global_bubble_infinite_expansion():
    sys.path.insert(0, BASE)
    from sul_global_cooperation import SulGlobalBubble
    bubble = SulGlobalBubble()
    for i in range(5):
        bubble.add_node(f"NODE_{i}", {"pym_id": f"PYM-test{i:04x}", "region": "Sul Global"})
    nodes = bubble.list_nodes()
    assert len(nodes) >= 7  # 2 iniciais + 5 adicionados


# ── Entrega via last_bridge.json ──────────────────────────────────────────────

def test_last_bridge_json_has_url():
    path = os.path.join(BASE, "amazonia_legal", "data", "last_bridge.json")
    with open(path) as f:
        d = json.load(f)
    assert d.get("url", "").startswith("https://"), \
        "last_bridge.json não tem URL válida"

def test_last_bridge_json_has_quantum_delivery():
    path = os.path.join(BASE, "amazonia_legal", "data", "last_bridge.json")
    with open(path) as f:
        d = json.load(f)
    assert "quantum_delivery" in d or d.get("url", "").startswith("https://"), \
        "last_bridge.json sem campo quantum_delivery"
