"""
TDD RED — quantum_terminal_share.py
Compartilhamento de terminal entre Claude Code e Antigravity via buffer JSON + lock atômico.
"""
import os
import json
import tempfile
import pytest
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def test_write_shared_buffer(tmp_path):
    """write_output() deve gravar entrada no buffer JSON."""
    from quantum_terminal_share import write_output
    buf_path = str(tmp_path / "buf.json")
    write_output("CLAUDE_CODE", "Teste Wave 2", buf_path=buf_path)
    with open(buf_path) as f:
        data = json.load(f)
    assert isinstance(data, list), "Buffer deve ser lista JSON"
    assert len(data) >= 1, "Buffer vazio após write"
    assert data[-1]["agent"] == "CLAUDE_CODE"
    assert data[-1]["content"] == "Teste Wave 2"


def test_read_shared_buffer(tmp_path):
    """read_output() deve retornar entradas do buffer, opcionalmente filtradas por agente."""
    from quantum_terminal_share import write_output, read_output
    buf_path = str(tmp_path / "buf2.json")
    write_output("CLAUDE_CODE", "msg A", buf_path=buf_path)
    write_output("ANTIGRAVITY", "msg B", buf_path=buf_path)
    all_entries = read_output(buf_path=buf_path)
    assert len(all_entries) == 2, "Deveria ter 2 entradas"
    claude_only = read_output(agent="CLAUDE_CODE", buf_path=buf_path)
    assert all(e["agent"] == "CLAUDE_CODE" for e in claude_only), "Filtro por agente falhou"


def test_lock_mechanism(tmp_path):
    """TerminalLock deve ser context manager utilizável."""
    from quantum_terminal_share import TerminalLock
    lock_path = str(tmp_path / "test.lock")
    with TerminalLock(lock_path=lock_path):
        assert os.path.exists(lock_path), "Arquivo de lock deve existir durante o bloco"
    # Após sair do contexto, lock pode ser liberado (arquivo removido ou não, depende da impl)


def test_terminal_sync_json(tmp_path):
    """Cada entrada no buffer deve ter campos: agent, content, timestamp."""
    from quantum_terminal_share import write_output, read_output
    buf_path = str(tmp_path / "buf3.json")
    write_output("CLAUDE_CODE", "formato teste", buf_path=buf_path)
    entries = read_output(buf_path=buf_path)
    entry = entries[-1]
    assert "agent" in entry, "Campo agent ausente"
    assert "content" in entry, "Campo content ausente"
    assert "timestamp" in entry, "Campo timestamp ausente"
