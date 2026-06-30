"""
TDD RED — infra/terminal_rpg_banner.sh
Banner soberano do terminal Synapse Hub com 5 seções dinâmicas.
"""
import os
import subprocess
import pytest

BANNER_PATH = os.path.join(
    os.path.dirname(__file__), "..", "infra", "terminal_rpg_banner.sh"
)


@pytest.fixture(scope="module")
def banner_output():
    assert os.path.exists(BANNER_PATH), f"Banner não encontrado: {BANNER_PATH}"
    result = subprocess.run(
        ["bash", BANNER_PATH], capture_output=True, text=True, timeout=15
    )
    return result.stdout + result.stderr


def test_ascii_art_synapse(banner_output):
    """Deve conter ASCII art de SYNAPSE e HUB SOBERANO."""
    text = banner_output.upper()
    assert "SYNAPSE" in text, "SYNAPSE ausente no banner"
    assert "SOBERANO" in text or "HUB" in text, "HUB SOBERANO ausente no banner"


def test_maestro_identity(banner_output):
    """Deve conter @eniripsa e referência ao hardware ASUS TUF F16."""
    assert "eniripsa" in banner_output.lower() or "@eniripsa" in banner_output, \
        "@eniripsa ausente no banner"
    assert "ASUS" in banner_output.upper() or "TUF" in banner_output.upper() or \
           "F16" in banner_output.upper() or "BLACKWELL" in banner_output.upper() or \
           "MAESTRO" in banner_output.upper(), \
        "Identidade do hardware ausente"


def test_hardware_section(banner_output):
    """Deve conter seção de hardware: CPU, RAM, GPU."""
    text = banner_output.upper()
    assert "CPU" in text, "CPU ausente no banner"
    assert "RAM" in text or "MEM" in text, "RAM/MEM ausente no banner"
    assert "GPU" in text or "NVIDIA" in text, "GPU ausente no banner"


def test_vault_oracle_section(banner_output):
    """Deve conter seção de vault: VAULT, CLAUDE, GEMINI."""
    text = banner_output.upper()
    assert "VAULT" in text, "VAULT ausente no banner"
    assert "CLAUDE" in text, "CLAUDE ausente no banner"
    assert "GEMINI" in text, "GEMINI ausente no banner"


def test_trava_diamante_status(banner_output):
    """Deve verificar busy_poll=0 e reportar TRAVA DIAMANTE."""
    text = banner_output.upper()
    assert "DIAMANTE" in text or "BUSY_POLL" in text or "TRAVA" in text, \
        "Status da Trava Diamante ausente no banner"


def test_quantum_loot_section(banner_output):
    """Deve conter seção de quantum loot com PYM IDs ou ativos."""
    text = banner_output.upper()
    assert "LOOT" in text or "PYM" in text or "QUANTUM" in text or "VAULT" in text, \
        "Seção quantum loot ausente"


def test_exit_0():
    """Banner deve retornar exit code 0."""
    assert os.path.exists(BANNER_PATH), f"Banner não encontrado: {BANNER_PATH}"
    result = subprocess.run(["bash", BANNER_PATH], capture_output=True, timeout=15)
    assert result.returncode == 0, f"Banner retornou exit code {result.returncode}"
