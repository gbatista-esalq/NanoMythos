"""
Video Prompt Joias Pym -- TDD Quantico aplicado ao roteiro de video.
Corda real: valores reais dos fundos soberanos em sovereignty_fund.json
(mesma fonte de Joias_do_Infinito_Soberano.md). Nao ha numero de YW
fabricado -- se o fundo nao existir no vault, o erro real propaga (RED).
Materializar: monta a cena (joia, cor, legenda, janela de tempo) so a
partir do valor real lido (GREEN).
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import video_prompt_joias_pym as vpj


def test_obter_corda_fundo_real_le_valor_do_vault(tmp_path):
    fundo_fake = tmp_path / "sovereignty_fund.json"
    fundo_fake.write_text(json.dumps({"Redoma-V2-Shield": 999.0}))
    valor = vpj.obter_corda_fundo("ESPACO", str(fundo_fake))
    assert valor == 999.0


def test_obter_corda_fundo_propaga_erro_real_se_fundo_ausente(tmp_path):
    fundo_fake = tmp_path / "sovereignty_fund.json"
    fundo_fake.write_text(json.dumps({"Outro-Fundo": 1.0}))
    try:
        vpj.obter_corda_fundo("ESPACO", str(fundo_fake))
        assert False, "deveria propagar KeyError real"
    except KeyError:
        pass


def test_obter_corda_fundo_propaga_erro_real_se_vault_ausente():
    try:
        vpj.obter_corda_fundo("ESPACO", "/caminho/inexistente/sovereignty_fund.json")
        assert False, "deveria propagar FileNotFoundError real"
    except FileNotFoundError:
        pass


def test_materializar_cena_joia_estrutura():
    cena = vpj.materializar_cena_joia("TEMPO", 12503834.6683)
    for campo in ("joia", "yw_real", "cor", "legenda", "fundo"):
        assert campo in cena
    assert cena["yw_real"] == 12503834.6683
    assert cena["fundo"] == "Obsidian-Vault-Preservation"


def test_materializar_cena_joia_legenda_curta_evita_overflow():
    cena = vpj.materializar_cena_joia("REALIDADE", 11989660.4936)
    assert len(cena["legenda"]) <= 40


def test_projetar_cena_joia_usa_protocolo_real(tmp_path):
    fundo_fake = tmp_path / "sovereignty_fund.json"
    fundo_fake.write_text(json.dumps({"Chronicles-Framework-Production": 12262297.5642}))
    cena = vpj.projetar_cena_joia("MENTE", str(fundo_fake))
    assert cena["yw_real"] == 12262297.5642
    assert cena["joia"] == "MENTE"


def test_todas_as_4_joias_pedidas_existem_no_mapa():
    for joia in ("TEMPO", "ESPACO", "REALIDADE", "MENTE"):
        assert joia in vpj.JOIA_MAP
        assert "fundo" in vpj.JOIA_MAP[joia]
        assert "cor" in vpj.JOIA_MAP[joia]


def test_projetar_video_prompt_joias_4_cenas_60s(tmp_path):
    fundo_fake = tmp_path / "sovereignty_fund.json"
    fundo_fake.write_text(json.dumps({
        "Obsidian-Vault-Preservation": 12503834.6683,
        "Redoma-V2-Shield": 12226795.0159,
        "Amazonia-Legal-DataBridge": 11989660.4936,
        "Chronicles-Framework-Production": 12262297.5642,
    }))
    cenas = vpj.projetar_video_prompt_joias(
        joias=("TEMPO", "ESPACO", "REALIDADE", "MENTE"),
        duracao_total=60.0,
        vault_path=str(fundo_fake),
    )
    assert len(cenas) == 4
    assert sum(c["duracao"] for c in cenas) == 60.0
    assert [c["joia"] for c in cenas] == ["TEMPO", "ESPACO", "REALIDADE", "MENTE"]
    assert cenas[0]["inicio"] == 0.0
    assert cenas[1]["inicio"] == 15.0
    assert cenas[2]["inicio"] == 30.0
    assert cenas[3]["inicio"] == 45.0


def test_vault_fund_path_default_aponta_para_quantum_world():
    assert vpj.VAULT_FUND_PATH.endswith("quantum_world/sovereignty_fund.json")
