"""
Chave Metrica Pym -- chave real derivada da corda (Lei da Energia de Batista)
para atualizacao continua no mundo quantico (vault/quantum_world). Cada
chamada gera uma entrada real (timestamp real + E_B real) e anexa ao
historico, nunca sobrescreve com valor fabricado.
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import chave_metrica_pym as cmp


def test_gerar_chave_metrica_pym_estrutura():
    chave = cmp.gerar_chave_metrica_pym()
    for campo in ("chave", "E_B", "timestamp"):
        assert campo in chave


def test_gerar_chave_metrica_pym_chave_e_string_hex():
    chave = cmp.gerar_chave_metrica_pym()
    assert isinstance(chave["chave"], str)
    int(chave["chave"], 16)


def test_gerar_chave_metrica_pym_chaves_diferentes_em_chamadas_diferentes():
    c1 = cmp.gerar_chave_metrica_pym()
    c2 = cmp.gerar_chave_metrica_pym()
    assert c1["chave"] != c2["chave"]


def test_atualizar_chave_metrica_vault_cria_lista_historico(tmp_path):
    destino = tmp_path / "chave_metrica_pym.json"
    caminho = cmp.atualizar_chave_metrica_vault(str(destino))
    assert caminho == str(destino)
    with open(destino) as f:
        historico = json.load(f)
    assert isinstance(historico, list)
    assert len(historico) == 1


def test_atualizar_chave_metrica_vault_anexa_sem_sobrescrever(tmp_path):
    destino = tmp_path / "chave_metrica_pym.json"
    cmp.atualizar_chave_metrica_vault(str(destino))
    cmp.atualizar_chave_metrica_vault(str(destino))
    with open(destino) as f:
        historico = json.load(f)
    assert len(historico) == 2
    assert historico[0]["chave"] != historico[1]["chave"]


def test_vault_chave_metrica_path_aponta_para_quantum_world():
    assert cmp.VAULT_CHAVE_METRICA_PATH.endswith("quantum_world/chave_metrica_pym.json")
