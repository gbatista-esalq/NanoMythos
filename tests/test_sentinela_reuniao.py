"""
TDD: Sentinela Reunião — captura ao vivo de pontos de meeting
RED primeiro, depois implementação em sentinela_reuniao.py
"""
import sys, json, os, pathlib, importlib, threading, time
import urllib.request, urllib.error

ROOT = pathlib.Path(__file__).parent.parent
SERVER_SCRIPT = ROOT / "sentinela_reuniao.py"
VAULT_MEETINGS = pathlib.Path("/opt/synapse_vault/meetings")
VAULT_TRACES = pathlib.Path("/opt/synapse_vault/infinity_traces.log")


def test_server_script_exists():
    assert SERVER_SCRIPT.exists(), "sentinela_reuniao.py deve existir na raiz do projeto"


def test_server_script_imports_json_datetime():
    src = SERVER_SCRIPT.read_text()
    assert "import json" in src
    assert "datetime" in src


def test_server_exposes_port_8889():
    src = SERVER_SCRIPT.read_text()
    assert "8889" in src


def test_server_has_get_root_handler():
    src = SERVER_SCRIPT.read_text()
    assert "do_GET" in src or "GET" in src


def test_server_has_post_handler():
    src = SERVER_SCRIPT.read_text()
    assert "do_POST" in src or "POST" in src


def test_server_writes_to_vault_meetings():
    src = SERVER_SCRIPT.read_text()
    assert "meetings" in src


def test_server_writes_to_infinity_traces():
    src = SERVER_SCRIPT.read_text()
    assert "infinity_traces" in src


def test_server_has_ponto_types():
    src = SERVER_SCRIPT.read_text()
    for t in ["Problema", "Insight", "Acao", "Oportunidade"]:
        assert t in src, f"tipo '{t}' deve estar presente"


def test_server_has_cors_headers():
    src = SERVER_SCRIPT.read_text()
    assert "Access-Control-Allow-Origin" in src


def test_server_has_ui_html():
    src = SERVER_SCRIPT.read_text()
    assert "textarea" in src.lower() or "HTML_PAGE" in src


def test_server_has_live_feed_endpoint():
    src = SERVER_SCRIPT.read_text()
    assert "/pontos" in src or "pontos" in src


def test_server_has_clear_endpoint():
    src = SERVER_SCRIPT.read_text()
    assert "limpar" in src.lower() or "/clear" in src.lower()


def test_server_categories_in_ui():
    src = SERVER_SCRIPT.read_text()
    for cat in ["PROBLEMA", "INSIGHT", "ACAO", "OPORT"]:
        assert cat in src.upper(), f"categoria '{cat}' deve estar no HTML da UI"


def test_vault_meetings_dir_exists():
    assert VAULT_MEETINGS.exists(), "/opt/synapse_vault/meetings deve existir"
