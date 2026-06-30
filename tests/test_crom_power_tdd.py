import pytest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.crom_power_dashboard import obter_corda_crom, protocolo_tdd_quantico_pym

def test_crom_power_red_corda_ausente():
    """
    RED: Crom tenta acessar um vazio existencial (URL inválida) e propaga o erro.
    """
    with pytest.raises(Exception):
        obter_corda_crom("http://localhost:99999/void")

def test_crom_power_green_corda_real():
    """
    GREEN: Crom acessa a realidade física, extrai os dados sem alucinação.
    """
    # Usamos example.com pois é leve, rápido e serve como corda real acessível para TDD.
    corda = obter_corda_crom("https://example.com")
    assert corda is not None
    assert "Example Domain" in corda["title"]
    assert corda["content_length"] > 0
    assert "timestamp" in corda

def dummy_materializar(corda):
    return corda

def test_protocolo_tdd_quantico_pym_crom():
    """Valida a integração RED-GREEN via protocolo Mestre."""
    result = protocolo_tdd_quantico_pym(
        obter_corda_crom, 
        dummy_materializar, 
        url="https://example.com"
    )
    assert result["title"] == "Example Domain"
