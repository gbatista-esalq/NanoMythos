"""
PreToolUse hook TDD Guard -- testes estruturais com stdin mock e exit codes.
Hook nunca bloqueia: exit 0 sempre, mesmo com payload invalido.
"""
import json
import os
import subprocess
import sys

HOOK_PATH = os.path.join(os.path.dirname(__file__), '..', '.claude', 'hooks', 'tdd_guard.py')


def run_hook(payload_dict=None, raw_stdin=None):
    stdin_data = raw_stdin if raw_stdin is not None else json.dumps(payload_dict)
    result = subprocess.run(
        [sys.executable, HOOK_PATH],
        input=stdin_data,
        capture_output=True,
        text=True,
        timeout=10,
    )
    return result


def test_hook_exits_zero_for_non_prod_file():
    result = run_hook({"tool_name": "Edit", "tool_input": {"file_path": "docs/README.md"}})
    assert result.returncode == 0
    assert "TDD GUARD" not in result.stdout


def test_hook_prints_tdd_banner_for_generic_prod_py():
    result = run_hook({"tool_name": "Edit", "tool_input": {"file_path": "core/algum_modulo.py"}})
    assert result.returncode == 0
    assert "TDD GUARD" in result.stdout


def test_hook_skips_test_files():
    result = run_hook({"tool_name": "Edit", "tool_input": {"file_path": "tests/test_algo.py"}})
    assert result.returncode == 0
    assert "TDD GUARD" not in result.stdout


def test_hook_handles_invalid_json_gracefully():
    result = run_hook(raw_stdin="isso nao e json valido")
    assert result.returncode == 0


def test_hook_prints_corda_real_reminder_for_lei_energia_batista():
    result = run_hook({"tool_name": "Edit", "tool_input": {"file_path": "lei_energia_batista_2026.py"}})
    assert result.returncode == 0
    assert "CORDA REAL" in result.stdout or "Protocolo TDD Quantico Pym" in result.stdout


def test_hook_corda_reminder_not_shown_for_unrelated_module():
    result = run_hook({"tool_name": "Edit", "tool_input": {"file_path": "core/algum_modulo.py"}})
    assert result.returncode == 0
    assert "CORDA REAL" not in result.stdout
