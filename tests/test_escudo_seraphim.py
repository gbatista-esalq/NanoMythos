import pytest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.farol_myrmex_tdd import TDDQuanticoPym
from core.chave_metrica_pym import gerar_chave_metrica_pym

def test_farol_myrmex_assinatura_mind_stone():
    """Valida a assertiva matemática do tamanho do hash da Mind Stone."""
    validador = TDDQuanticoPym("https://soundcloud.com/fake-url")
    assert len(validador.assinatura_mind_stone) == 64
    assert validador.test_protocolo_eniripsa() is True

def test_farol_myrmex_condicao_aleph_um():
    """Valida a flutuação estocástica para evitar detecção (anti-bot / anti-captcha)."""
    validador = TDDQuanticoPym("https://soundcloud.com/fake-url")
    assert validador.test_condicao_aleph_um() is True

def test_chave_metrica_pym_geracao():
    """Verifica se a chave métrica gerada possui a estrutura matemática esperada e é criptograficamente segura."""
    resultado = gerar_chave_metrica_pym()
    
    assert "chave" in resultado, "A chave não foi gerada."
    assert "E_B" in resultado, "A Energia de Batista (E_B) está ausente."
    assert "timestamp" in resultado, "O timestamp de ancoragem está ausente."
    
    # A chave deve ser um recorte de 16 caracteres do SHA-256
    assert len(resultado["chave"]) == 16
    assert isinstance(resultado["E_B"], float)
    
def test_chaves_sao_unicas():
    """Teste de entropia: Duas chamadas seguidas devem gerar chaves estocásticas diferentes."""
    chave_1 = gerar_chave_metrica_pym()["chave"]
    chave_2 = gerar_chave_metrica_pym()["chave"]
    
    assert chave_1 != chave_2, "Colapso Quântico! O gerador está previsível (falha na entropia)."
