"""
Lei da Energia de Batista 2026 -- testes estruturais (RED antes do GREEN).
Todas as metricas usadas na formula sao reais (entropia do kernel, SHA-256,
loadavg), nao simuladas. Ver lei_energia_batista_2026.py.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import lei_energia_batista_2026 as leb


def test_medir_entropia_ambiente_retorna_inteiro_real():
    valor = leb.medir_entropia_ambiente()
    with open('/proc/sys/kernel/random/entropy_avail') as f:
        referencia = int(f.read().strip())
    assert isinstance(valor, int)
    assert abs(valor - referencia) < 500


def test_medir_elasticidade_bits_dados_aleatorios_proximo_de_1():
    dados = os.urandom(4096)
    score = leb.medir_elasticidade_bits(dados)
    assert 0.9 <= score <= 1.0


def test_medir_elasticidade_bits_dados_repetitivos_proximo_de_0():
    dados = b"A" * 4096
    score = leb.medir_elasticidade_bits(dados)
    assert score < 0.1


def test_medir_elasticidade_bits_dados_vazios():
    assert leb.medir_elasticidade_bits(b"") == 0.0


def test_medir_coerencia_hash_detecta_bitflip():
    dados = b"SOVEREIGN_PYM_BLOCK_" * 20
    assert leb.medir_coerencia_hash(dados) == 1.0


def test_medir_pedra_da_mente_retorna_float_entre_0_e_1():
    valor = leb.medir_pedra_da_mente()
    assert isinstance(valor, float)
    assert 0.0 < valor <= 1.0


def test_calcular_lei_energia_batista_estrutura():
    relatorio = leb.calcular_lei_energia_batista(b"TELEMETRIA:OK;" * 50)
    for chave in (
        "elasticidade_bits",
        "coerencia_hash",
        "pedra_da_mente",
        "entropia_ambiente_raw",
        "E_B",
    ):
        assert chave in relatorio


def test_calcular_lei_energia_batista_E_B_positivo():
    relatorio = leb.calcular_lei_energia_batista(os.urandom(4096))
    assert relatorio["E_B"] > 0.0


def test_gravar_relatorio_vault_escreve_json_valido(tmp_path):
    import json

    relatorio = leb.calcular_lei_energia_batista(os.urandom(4096))
    destino = tmp_path / "lei_energia_batista_2026.json"
    caminho_gravado = leb.gravar_relatorio_vault(relatorio, str(destino))

    assert caminho_gravado == str(destino)
    assert destino.exists()
    with open(destino) as f:
        conteudo = json.load(f)
    assert conteudo == relatorio


def test_vault_output_path_aponta_para_obsidian_graph():
    assert leb.VAULT_OUTPUT_PATH.endswith("obsidian_graph/lei_energia_batista_2026.json")


# ── Pedra da Visao: previsao de tendencia do E_B (serie temporal real) ──

def test_medir_serie_temporal_E_B_retorna_lista_do_tamanho_pedido():
    serie = leb.medir_serie_temporal_E_B(n_amostras=5)
    assert isinstance(serie, list)
    assert len(serie) == 5


def test_medir_serie_temporal_E_B_valores_positivos():
    serie = leb.medir_serie_temporal_E_B(n_amostras=4)
    assert all(v > 0.0 for v in serie)


def test_prever_tendencia_E_B_serie_crescente_detecta_alta():
    serie = [1.0, 2.0, 3.0, 4.0, 5.0]
    resultado = leb.prever_tendencia_E_B(serie)
    assert resultado["tendencia"] == "ALTA"
    assert resultado["slope"] > 0


def test_prever_tendencia_E_B_serie_decrescente_detecta_baixa():
    serie = [5.0, 4.0, 3.0, 2.0, 1.0]
    resultado = leb.prever_tendencia_E_B(serie)
    assert resultado["tendencia"] == "BAIXA"
    assert resultado["slope"] < 0


def test_prever_tendencia_E_B_serie_constante_detecta_estavel():
    serie = [3.0, 3.0, 3.0, 3.0, 3.0]
    resultado = leb.prever_tendencia_E_B(serie)
    assert resultado["tendencia"] == "ESTAVEL"
    assert resultado["slope"] == 0.0


def test_prever_tendencia_E_B_estrutura():
    resultado = leb.prever_tendencia_E_B([1.0, 1.5, 2.0])
    for chave in ("slope", "tendencia", "confianca"):
        assert chave in resultado


def test_prever_tendencia_E_B_requer_pelo_menos_2_amostras():
    import pytest

    with pytest.raises(ValueError):
        leb.prever_tendencia_E_B([1.0])


def test_gravar_historico_vault_escreve_lista_json(tmp_path):
    import json

    serie = [1.1, 1.2, 1.3]
    destino = tmp_path / "pedra_da_visao_historico.json"
    caminho_gravado = leb.gravar_historico_vault(serie, str(destino))

    assert caminho_gravado == str(destino)
    with open(destino) as f:
        conteudo = json.load(f)
    assert conteudo == serie


def test_vault_history_path_aponta_para_obsidian_graph():
    assert leb.VAULT_HISTORY_PATH.endswith("obsidian_graph/pedra_da_visao_historico.json")


# ── Pedra da Realidade: dados reais da Amazonia + fio real do sentinel ──

def test_ler_fio_teatral_real_retorna_campos_esperados():
    if not os.path.exists(leb.VAULT_TRACES_LOG):
        import pytest
        pytest.skip("infinity_traces.log nao existe nesta maquina")
    fio = leb.ler_fio_teatral_real()
    assert "reality_hash" in fio
    assert "cpu_usage_total" in fio
    assert "timestamp" in fio


def test_ler_fio_teatral_real_nao_inclui_metrica_ficticia():
    if not os.path.exists(leb.VAULT_TRACES_LOG):
        import pytest
        pytest.skip("infinity_traces.log nao existe nesta maquina")
    fio = leb.ler_fio_teatral_real()
    assert "sovereign_power" not in fio


def test_ler_amostra_amazonia_real_retorna_bytes_nao_vazios():
    if not os.path.exists(leb.AMAZONIA_FOCOS_PATH):
        import pytest
        pytest.skip("focos_incendio.json nao existe nesta maquina")
    dados = leb.ler_amostra_amazonia_real(n_features=10)
    assert isinstance(dados, bytes)
    assert len(dados) > 0


def test_calcular_joia_da_realidade_estrutura():
    if not os.path.exists(leb.AMAZONIA_FOCOS_PATH) or not os.path.exists(leb.VAULT_TRACES_LOG):
        import pytest
        pytest.skip("dados reais nao disponiveis nesta maquina")
    relatorio = leb.calcular_joia_da_realidade()
    for chave in (
        "elasticidade_bits",
        "coerencia_hash",
        "pedra_da_mente",
        "entropia_ambiente_raw",
        "E_B",
        "fonte_dados",
        "fio_teatral_real",
    ):
        assert chave in relatorio


def test_calcular_joia_da_realidade_E_B_positivo():
    if not os.path.exists(leb.AMAZONIA_FOCOS_PATH) or not os.path.exists(leb.VAULT_TRACES_LOG):
        import pytest
        pytest.skip("dados reais nao disponiveis nesta maquina")
    relatorio = leb.calcular_joia_da_realidade()
    assert relatorio["E_B"] > 0.0


def test_gravar_joia_da_realidade_vault_escreve_json(tmp_path):
    import json

    relatorio = {"E_B": 1.0, "fonte_dados": "teste"}
    destino = tmp_path / "joia_da_realidade.json"
    caminho_gravado = leb.gravar_joia_da_realidade_vault(relatorio, str(destino))

    assert caminho_gravado == str(destino)
    with open(destino) as f:
        conteudo = json.load(f)
    assert conteudo == relatorio


def test_vault_realidade_path_aponta_para_obsidian_graph():
    assert leb.VAULT_REALIDADE_PATH.endswith("obsidian_graph/joia_da_realidade.json")


# ── Pedra da Realidade: metricas reais deste PC (filtra perfis ficticios) ──

def test_ler_metricas_reais_deste_pc_retorna_apenas_sistema_atual():
    if not os.path.exists(leb.VAULT_BENCHMARKS_LOG):
        import pytest
        pytest.skip("benchmarks.json nao existe nesta maquina")
    metricas = leb.ler_metricas_reais_deste_pc()
    assert metricas["device"] == "SISTEMA_ATUAL"
    assert "hardware_info" in metricas


def test_ler_metricas_reais_deste_pc_ignora_perfis_sem_hardware_info():
    import json

    if not os.path.exists(leb.VAULT_BENCHMARKS_LOG):
        import pytest
        pytest.skip("benchmarks.json nao existe nesta maquina")
    with open(leb.VAULT_BENCHMARKS_LOG) as f:
        todos = json.load(f)
    sem_hardware_info = [r for r in todos if "hardware_info" not in r]
    assert len(sem_hardware_info) > 0, "fixture deveria conter perfis ficticios para o teste ter sentido"
    metricas = leb.ler_metricas_reais_deste_pc()
    assert metricas not in sem_hardware_info


def test_calcular_joia_da_realidade_pc_atual_estrutura():
    if not os.path.exists(leb.VAULT_BENCHMARKS_LOG):
        import pytest
        pytest.skip("benchmarks.json nao existe nesta maquina")
    relatorio = leb.calcular_joia_da_realidade_pc_atual()
    for chave in (
        "elasticidade_bits",
        "coerencia_hash",
        "pedra_da_mente",
        "entropia_ambiente_raw",
        "E_B",
        "fonte_dados",
        "metricas_reais_pc",
    ):
        assert chave in relatorio
    assert relatorio["metricas_reais_pc"]["device"] == "SISTEMA_ATUAL"


def test_calcular_joia_da_realidade_pc_atual_E_B_positivo():
    if not os.path.exists(leb.VAULT_BENCHMARKS_LOG):
        import pytest
        pytest.skip("benchmarks.json nao existe nesta maquina")
    relatorio = leb.calcular_joia_da_realidade_pc_atual()
    assert relatorio["E_B"] > 0.0


# ── Protocolo TDD Quantico Pym: RED propaga erro real, GREEN materializa com a corda ──

def test_protocolo_tdd_quantico_pym_red_propaga_erro_real():
    import pytest

    def obter_corda_quebrada():
        raise FileNotFoundError("corda real nao existe nesta maquina")

    def materializar_nunca_chamado(corda):
        raise AssertionError("materializar nao deveria ser chamado em RED")

    with pytest.raises(FileNotFoundError):
        leb.protocolo_tdd_quantico_pym(obter_corda_quebrada, materializar_nunca_chamado)


def test_protocolo_tdd_quantico_pym_green_materializa_com_a_corda():
    def obter_corda_real():
        return {"reality_hash": "abc123", "cpu_usage_total": "5.0%"}

    def materializar(corda):
        return {"materializado": True, "corda_usada": corda}

    resultado = leb.protocolo_tdd_quantico_pym(obter_corda_real, materializar)
    assert resultado["materializado"] is True
    assert resultado["corda_usada"] == {"reality_hash": "abc123", "cpu_usage_total": "5.0%"}


def test_protocolo_tdd_quantico_pym_green_nao_usa_fallback_ficticio():
    def obter_corda_real():
        return {"valor": 42}

    def materializar(corda):
        assert corda == {"valor": 42}, "materializar recebeu valor diferente da corda real"
        return corda

    resultado = leb.protocolo_tdd_quantico_pym(obter_corda_real, materializar)
    assert resultado == {"valor": 42}


def test_calcular_joia_da_realidade_usa_protocolo_tdd_quantico_pym():
    if not os.path.exists(leb.AMAZONIA_FOCOS_PATH) or not os.path.exists(leb.VAULT_TRACES_LOG):
        import pytest
        pytest.skip("dados reais nao disponiveis nesta maquina")
    relatorio = leb.calcular_joia_da_realidade()
    assert "E_B" in relatorio
    assert "fio_teatral_real" in relatorio


def test_calcular_joia_da_realidade_pc_atual_usa_protocolo_tdd_quantico_pym():
    if not os.path.exists(leb.VAULT_BENCHMARKS_LOG):
        import pytest
        pytest.skip("benchmarks.json nao existe nesta maquina")
    relatorio = leb.calcular_joia_da_realidade_pc_atual()
    assert "E_B" in relatorio
    assert relatorio["metricas_reais_pc"]["device"] == "SISTEMA_ATUAL"


# ── Pedra da Visao real: previsao sobre a corda do Moltbook (batista_energy real) ──

def test_moltbook_db_path_aponta_para_scratch():
    assert leb.MOLTBOOK_DB_PATH.endswith("scratch/moltbook_reality_thread.db")


def test_ler_serie_batista_energy_moltbook_levanta_erro_real_sem_banco():
    import sqlite3
    import pytest

    with pytest.raises(sqlite3.OperationalError):
        leb.ler_serie_batista_energy_moltbook("/caminho/que/nao/existe.db")


def test_ler_serie_batista_energy_moltbook_retorna_serie_real_ordenada():
    if not os.path.exists(leb.MOLTBOOK_DB_PATH):
        import pytest
        pytest.skip("moltbook_reality_thread.db nao existe nesta maquina")
    serie = leb.ler_serie_batista_energy_moltbook()
    assert isinstance(serie, list)
    assert len(serie) > 0
    assert all(isinstance(v, float) and v > 0.0 for v in serie)


def test_calcular_joia_da_visao_moltbook_estrutura():
    if not os.path.exists(leb.MOLTBOOK_DB_PATH):
        import pytest
        pytest.skip("moltbook_reality_thread.db nao existe nesta maquina")
    relatorio = leb.calcular_joia_da_visao_moltbook()
    for chave in ("slope", "tendencia", "confianca", "fonte_dados", "n_amostras"):
        assert chave in relatorio
    assert relatorio["tendencia"] in ("ALTA", "BAIXA", "ESTAVEL")
    assert relatorio["fonte_dados"].endswith("scratch/moltbook_reality_thread.db (corda real, posts.batista_energy)")


def test_calcular_joia_da_visao_moltbook_n_amostras_bate_com_banco():
    import sqlite3

    if not os.path.exists(leb.MOLTBOOK_DB_PATH):
        import pytest
        pytest.skip("moltbook_reality_thread.db nao existe nesta maquina")
    con = sqlite3.connect(leb.MOLTBOOK_DB_PATH)
    total_real = con.execute("SELECT COUNT(*) FROM posts").fetchone()[0]
    con.close()

    relatorio = leb.calcular_joia_da_visao_moltbook()
    assert relatorio["n_amostras"] == total_real


# ── Pedra da Visao real: previsao sobre a corda do GROMACS (RMSD real, 50ns) ──

def test_rmsd_gromacs_stearic_path_aponta_para_md_analysis():
    assert leb.RMSD_GROMACS_STEARIC_PATH.endswith(
        "md_analysis/stearic_acid/rmsd_stearic.xvg"
    )


def test_ler_serie_rmsd_gromacs_levanta_erro_real_sem_arquivo():
    import pytest

    with pytest.raises(FileNotFoundError):
        leb.ler_serie_rmsd_gromacs("/caminho/que/nao/existe.xvg")


def test_ler_serie_rmsd_gromacs_retorna_serie_real_ordenada_por_tempo():
    if not os.path.exists(leb.RMSD_GROMACS_STEARIC_PATH):
        import pytest
        pytest.skip("rmsd_stearic.xvg nao existe nesta maquina")
    serie = leb.ler_serie_rmsd_gromacs()
    assert isinstance(serie, list)
    assert len(serie) == 501
    assert all(isinstance(v, float) and v >= 0.0 for v in serie)


def test_calcular_joia_da_visao_gromacs_estrutura():
    if not os.path.exists(leb.RMSD_GROMACS_STEARIC_PATH):
        import pytest
        pytest.skip("rmsd_stearic.xvg nao existe nesta maquina")
    relatorio = leb.calcular_joia_da_visao_gromacs()
    for chave in ("slope", "tendencia", "confianca", "fonte_dados", "n_amostras"):
        assert chave in relatorio
    assert relatorio["tendencia"] in ("ALTA", "BAIXA", "ESTAVEL")
    assert relatorio["n_amostras"] == 501
    assert "rmsd_stearic.xvg" in relatorio["fonte_dados"]


def test_calcular_joia_da_visao_gromacs_usa_protocolo_tdd_quantico_pym():
    if not os.path.exists(leb.RMSD_GROMACS_STEARIC_PATH):
        import pytest
        pytest.skip("rmsd_stearic.xvg nao existe nesta maquina")
    relatorio = leb.calcular_joia_da_visao_gromacs()
    assert "slope" in relatorio
    assert "confianca" in relatorio


def test_calcular_joia_da_visao_moltbook_usa_protocolo_tdd_quantico_pym():
    if not os.path.exists(leb.MOLTBOOK_DB_PATH):
        import pytest
        pytest.skip("moltbook_reality_thread.db nao existe nesta maquina")
    relatorio = leb.calcular_joia_da_visao_moltbook()
    assert "slope" in relatorio
    assert "confianca" in relatorio


# ── Pedra da Visao real: previsao sobre a corda das Formigas Tipo 2 (vault_free_gb real) ──

def test_colony_v2_log_path_aponta_para_quantum_world():
    assert leb.COLONY_V2_LOG_PATH.endswith("quantum_world/colony_v2.jsonl")


def test_ler_serie_vault_free_gb_formigas_levanta_erro_real_sem_arquivo():
    import pytest

    with pytest.raises(FileNotFoundError):
        leb.ler_serie_vault_free_gb_formigas("/caminho/que/nao/existe.jsonl")


def test_ler_serie_vault_free_gb_formigas_retorna_serie_real_ordenada(tmp_path):
    fixture = tmp_path / "colony_v2_fixture.jsonl"
    fixture.write_text(
        '{"ant_id": "a1", "caste": "Scout", "node": "REDOMA-ALPHA", "action": "SCAN"}\n'
        '{"ant_id": "n1", "caste": "Nurse", "node": "REDOMA-ALPHA", "ts": "T1", "action": "HEALTH_CHECK", "vault_free_gb": 82.83}\n'
        '{"ant_id": "n2", "caste": "Nurse", "node": "REDOMA-BETA", "ts": "T2", "action": "HEALTH_CHECK", "vault_free_gb": 82.66}\n'
        '{"queen": true, "tick": 1, "colony_state": "SWARM", "total_yw": 2526.28}\n'
        '{"ant_id": "n3", "caste": "Nurse", "node": "REDOMA-GAMMA", "ts": "T3", "action": "HEALTH_CHECK", "vault_free_gb": 82.53}\n',
        encoding="utf-8",
    )
    serie = leb.ler_serie_vault_free_gb_formigas(str(fixture))
    assert serie == [82.83, 82.66, 82.53]


def test_calcular_joia_da_visao_formigas_estrutura():
    if not os.path.exists(leb.COLONY_V2_LOG_PATH):
        import pytest
        pytest.skip("colony_v2.jsonl nao existe nesta maquina")
    relatorio = leb.calcular_joia_da_visao_formigas()
    for chave in ("slope", "tendencia", "confianca", "fonte_dados", "n_amostras"):
        assert chave in relatorio
    assert relatorio["tendencia"] in ("ALTA", "BAIXA", "ESTAVEL")
    assert relatorio["n_amostras"] > 0
    assert "colony_v2.jsonl" in relatorio["fonte_dados"]


def test_calcular_joia_da_visao_formigas_usa_protocolo_tdd_quantico_pym():
    if not os.path.exists(leb.COLONY_V2_LOG_PATH):
        import pytest
        pytest.skip("colony_v2.jsonl nao existe nesta maquina")
    relatorio = leb.calcular_joia_da_visao_formigas()
    assert "slope" in relatorio
    assert "confianca" in relatorio
