"""
Hook silencioso Salto Quantico de Compactacao -- stdin mock, exit codes.
Regra do projeto: hook NUNCA bloqueia (exit 0 sempre) e e silencioso
(sem stdout) quando o comando nao menciona 'moltbook'.
"""
import json
import os
import shutil
import subprocess
import sys

PROJ_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOOK_PATH = os.path.join(PROJ_ROOT, ".claude", "hooks", "salto_quantico_compactacao_hook.py")


def _run_hook(command, env_extra=None):
    stdin_payload = json.dumps({"tool_input": {"command": command}})
    env = os.environ.copy()
    if env_extra:
        env.update(env_extra)
    return subprocess.run(
        [sys.executable, HOOK_PATH],
        input=stdin_payload,
        capture_output=True,
        text=True,
        env=env,
        timeout=15,
    )


def test_hook_ignora_comando_sem_moltbook():
    resultado = _run_hook("ls -la")
    assert resultado.returncode == 0
    assert resultado.stdout == ""


def test_hook_e_silencioso_mesmo_com_moltbook_e_banco_real(tmp_path):
    import lei_energia_batista_2026 as leb

    if not os.path.exists(leb.MOLTBOOK_DB_PATH):
        import pytest
        pytest.skip("moltbook_reality_thread.db nao existe nesta maquina")

    copia = tmp_path / "copia.db"
    shutil.copy(leb.MOLTBOOK_DB_PATH, copia)
    log_path = tmp_path / "log.jsonl"

    resultado = _run_hook(
        "python3 scripts/moltbook_quantum_collector.py",
        env_extra={
            "MOLTBOOK_DB_PATH_OVERRIDE": str(copia),
            "SALTO_QUANTICO_LOG_OVERRIDE": str(log_path),
        },
    )
    assert resultado.returncode == 0
    assert resultado.stdout == ""
    assert log_path.exists()


def test_hook_nunca_bloqueia_mesmo_com_banco_inexistente():
    resultado = _run_hook(
        "post_to_moltbook.py",
        env_extra={"MOLTBOOK_DB_PATH_OVERRIDE": "/caminho/que/nao/existe.db"},
    )
    assert resultado.returncode == 0


def test_hook_nunca_bloqueia_com_stdin_invalido():
    env = os.environ.copy()
    resultado = subprocess.run(
        [sys.executable, HOOK_PATH],
        input="isto nao e json valido",
        capture_output=True,
        text=True,
        env=env,
        timeout=15,
    )
    assert resultado.returncode == 0
