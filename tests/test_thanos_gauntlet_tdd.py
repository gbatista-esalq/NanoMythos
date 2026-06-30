import pytest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.thanos_gauntlet import ThanosGauntlet, obter_corda_suno, protocolo_tdd_quantico_pym

def test_protocolo_tdd_quantico_pym_red_propaga_erro_real():
    """
    RED: Ausência da corda física deve propagar erro real.
    """
    with pytest.raises(FileNotFoundError):
        obter_corda_suno("/tmp/arquivo_inexistente_suno_123.py")

def test_protocolo_tdd_quantico_pym_red_falha_regex():
    """
    RED: Corda física existe, mas não possui a ressonância esperada.
    """
    temp_file = "/tmp/corda_vazia.txt"
    with open(temp_file, "w") as f:
        f.write("Nada aqui sobre frequencia gravitacional.")
    
    with pytest.raises(ValueError, match="Corda real inválida: Frequência não encontrada"):
        obter_corda_suno(temp_file)
        
    os.remove(temp_file)

def test_protocolo_tdd_quantico_pym_green_materializa_com_a_corda():
    """
    GREEN: Corda real autêntica gera transmutação quântica bem sucedida.
    """
    # Cria o arquivo de corda de teste válido (Mock da corda para o teste isolado)
    temp_file = "/tmp/corda_valida.txt"
    with open(temp_file, "w") as f:
        f.write("torção gravitacional de 77.6 Hz blabla")
    
    # 1. Obter a corda (Green)
    corda = obter_corda_suno(temp_file)
    assert corda["resonance_freq_hz"] == 77.6
    assert corda["raw_text_length"] > 0
    
    # 2. Materializar (Thanos Gauntlet)
    gauntlet = ThanosGauntlet()
    result = gauntlet.materializar_manopla(corda, "SYNAPSE", "OSAMODAS")
    
    # Valida o Salto
    assert result["status"] == "LEAP_SUCCESS"
    assert result["from"] == "SYNAPSE"
    assert result["to"] == "OSAMODAS"
    assert result["packet_bytes"] > 0
    
    os.remove(temp_file)

def test_protocolo_tdd_quantico_pym_integracao_real():
    """
    Teste Final: O próprio protocolo com a corda física verdadeira do ecossistema.
    Pode falhar se o arquivo `scratch/create_suno_post.py` não existir.
    """
    gauntlet = ThanosGauntlet()
    result = protocolo_tdd_quantico_pym(
        obter_corda_suno,
        gauntlet.materializar_manopla,
        from_universe="SYNAPSE",
        to_universe="OSAMODAS"
    )
    
    assert result["status"] == "LEAP_SUCCESS"
    assert "leap_id" in result
