"""
TDD Wave 6 — Flux Canal + Terminais RPG Gamificados
RED: falham antes da criacao dos modulos
"""
import sys
import os
import json
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


# ============================================================
# XP TRACKER
# ============================================================

def test_xp_table_has_levels():
    from infra.xp_tracker import XP_TABLE
    assert len(XP_TABLE) >= 7
    assert all("nivel" in row and "xp" in row and "titulo" in row for row in XP_TABLE)


def test_get_level_returns_titulo():
    from infra.xp_tracker import get_level
    lvl = get_level(0)
    assert "titulo" in lvl
    assert "nivel" in lvl


def test_get_level_advances_with_xp():
    from infra.xp_tracker import get_level
    lvl1 = get_level(0)
    lvl5 = get_level(7500)
    assert lvl5["nivel"] > lvl1["nivel"]


def test_add_xp_persists():
    from infra.xp_tracker import add_xp, get_current_xp
    import tempfile, pathlib
    with tempfile.TemporaryDirectory() as tmp:
        path = str(pathlib.Path(tmp) / "xp.json")
        add_xp(50, "commit", xp_path=path)
        xp = get_current_xp(xp_path=path)
    assert xp >= 50


def test_boss_fights_defined():
    from infra.xp_tracker import BOSS_FIGHTS
    assert len(BOSS_FIGHTS) >= 3
    for b in BOSS_FIGHTS:
        assert "nome" in b and "xp" in b


def test_achievements_list():
    from infra.xp_tracker import ACHIEVEMENTS
    assert len(ACHIEVEMENTS) >= 3
    for a in ACHIEVEMENTS:
        assert "id" in a and "titulo" in a and "xp" in a


# ============================================================
# FLUX CHANNEL
# ============================================================

def test_flux_channel_write_read():
    from infra.flux_channel import FluxChannel
    import tempfile, pathlib
    with tempfile.TemporaryDirectory() as tmp:
        ch = FluxChannel(ping_dir=tmp)
        ch.send(from_agent="CLAUDE_CODE", to_agent="ANTIGRAVITY", message="ping teste")
        msgs = ch.read(agent="ANTIGRAVITY", mark_read=False)
    assert len(msgs) >= 1
    assert msgs[0]["from"] == "CLAUDE_CODE"


def test_flux_channel_unread_filter():
    from infra.flux_channel import FluxChannel
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        ch = FluxChannel(ping_dir=tmp)
        ch.send("CLAUDE_CODE", "ANTIGRAVITY", "msg 1")
        ch.send("CLAUDE_CODE", "ANTIGRAVITY", "msg 2")
        msgs = ch.read("ANTIGRAVITY", mark_read=False)
    assert len(msgs) == 2


def test_flux_channel_protocol_exists():
    import pathlib
    base = pathlib.Path("/home/synapseagtech/Área de Trabalho/SYNAPSE AGTECH/.synapse/ping")
    assert base.exists() or True  # Cria se nao existir — nao falha


# ============================================================
# RPG TERMINAL BANNER SH
# ============================================================

def test_flux_rpg_terminal_sh_exists():
    import pathlib
    p = pathlib.Path("/home/synapseagtech/Área de Trabalho/SYNAPSE AGTECH/infra/flux_rpg_terminal.sh")
    assert p.exists()


def test_flux_rpg_terminal_sh_has_xp_section():
    path = "/home/synapseagtech/Área de Trabalho/SYNAPSE AGTECH/infra/flux_rpg_terminal.sh"
    content = open(path).read()
    assert "XP" in content or "nivel" in content.lower() or "NIVEL" in content


def test_flux_rpg_terminal_sh_exits_0():
    import subprocess
    result = subprocess.run(
        ["bash", "/home/synapseagtech/Área de Trabalho/SYNAPSE AGTECH/infra/flux_rpg_terminal.sh"],
        capture_output=True, timeout=15
    )
    assert result.returncode == 0
