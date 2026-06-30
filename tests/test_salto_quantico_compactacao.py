"""
Salto Quantico de Compactacao -- testes estruturais (RED antes do GREEN).

Duas metricas reais e INDEPENDENTES sao medidas lado a lado:
- gravidade_compactacao: estado fisico real do arquivo SQLite (PRAGMA
  page_count/freelist_count), antes e depois de um VACUUM real.
- acertabilidade_modelo: confianca real (R^2) da Pedra da Visao
  (prever_tendencia_E_B) sobre a corda real de batista_energy.

Nota metodologica obrigatoria (ver lei_energia_batista_2026.py e
docs/salto_quantico_compactacao_tcc.md): VACUUM reorganiza paginas no
disco, NAO altera nenhum valor de linha. Por isso nao existe mecanismo
real onde compactar o banco, por si so, mude a acertabilidade do modelo.
Os testes abaixo verificam que o modulo nunca afirma essa causalidade.
"""
import os
import shutil
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import salto_quantico_compactacao as sqc
import lei_energia_batista_2026 as leb


def test_medir_gravidade_compactacao_estrutura():
    if not os.path.exists(leb.MOLTBOOK_DB_PATH):
        import pytest
        pytest.skip("moltbook_reality_thread.db nao existe nesta maquina")
    relatorio = sqc.medir_gravidade_compactacao()
    for chave in (
        "page_count", "freelist_count", "page_size",
        "tamanho_bytes", "fragmentacao_pct", "gravidade_compactacao",
    ):
        assert chave in relatorio
    assert 0.0 <= relatorio["gravidade_compactacao"] <= 1.0


def test_medir_gravidade_compactacao_levanta_erro_real_sem_banco():
    import sqlite3
    import pytest

    with pytest.raises(sqlite3.OperationalError):
        sqc.medir_gravidade_compactacao("/caminho/que/nao/existe.db")


def test_compactar_banco_zera_freelist_depois_do_vacuum(tmp_path):
    if not os.path.exists(leb.MOLTBOOK_DB_PATH):
        import pytest
        pytest.skip("moltbook_reality_thread.db nao existe nesta maquina")
    copia = tmp_path / "copia.db"
    shutil.copy(leb.MOLTBOOK_DB_PATH, copia)

    resultado = sqc.compactar_banco(str(copia))
    assert "antes" in resultado and "depois" in resultado
    assert resultado["depois"]["freelist_count"] == 0


def test_medir_acertabilidade_modelo_retorna_float_entre_0_e_1():
    if not os.path.exists(leb.MOLTBOOK_DB_PATH):
        import pytest
        pytest.skip("moltbook_reality_thread.db nao existe nesta maquina")
    valor = sqc.medir_acertabilidade_modelo()
    assert isinstance(valor, float)
    assert 0.0 <= valor <= 1.0


def test_registrar_salto_quantico_compactacao_grava_log_jsonl(tmp_path):
    import json

    if not os.path.exists(leb.MOLTBOOK_DB_PATH):
        import pytest
        pytest.skip("moltbook_reality_thread.db nao existe nesta maquina")
    copia = tmp_path / "copia.db"
    shutil.copy(leb.MOLTBOOK_DB_PATH, copia)
    log_path = tmp_path / "salto_quantico_compactacao.jsonl"

    registro = sqc.registrar_salto_quantico_compactacao(str(copia), str(log_path))

    assert log_path.exists()
    with open(log_path) as f:
        linhas = [json.loads(l) for l in f if l.strip()]
    assert len(linhas) == 1
    assert linhas[0] == registro


def test_registrar_salto_quantico_compactacao_nao_afirma_causalidade_falsa(tmp_path):
    if not os.path.exists(leb.MOLTBOOK_DB_PATH):
        import pytest
        pytest.skip("moltbook_reality_thread.db nao existe nesta maquina")
    copia = tmp_path / "copia.db"
    shutil.copy(leb.MOLTBOOK_DB_PATH, copia)
    log_path = tmp_path / "log.jsonl"

    registro = sqc.registrar_salto_quantico_compactacao(str(copia), str(log_path))
    assert "nota_metodologica" in registro
    assert "VACUUM" in registro["nota_metodologica"]


def test_vault_salto_path_aponta_para_obsidian_graph():
    assert sqc.VAULT_SALTO_PATH.endswith("obsidian_graph/salto_quantico_compactacao.json")


def test_registrar_salto_quantico_compactacao_grava_snapshot_no_vault(tmp_path):
    import json

    if not os.path.exists(leb.MOLTBOOK_DB_PATH):
        import pytest
        pytest.skip("moltbook_reality_thread.db nao existe nesta maquina")
    copia = tmp_path / "copia.db"
    shutil.copy(leb.MOLTBOOK_DB_PATH, copia)
    log_path = tmp_path / "log.jsonl"
    snapshot_path = tmp_path / "snapshot.json"

    registro = sqc.registrar_salto_quantico_compactacao(
        str(copia), str(log_path), str(snapshot_path)
    )

    assert snapshot_path.exists()
    with open(snapshot_path) as f:
        conteudo = json.load(f)
    assert conteudo == registro


def test_registrar_salto_quantico_compactacao_campos_reais(tmp_path):
    if not os.path.exists(leb.MOLTBOOK_DB_PATH):
        import pytest
        pytest.skip("moltbook_reality_thread.db nao existe nesta maquina")
    copia = tmp_path / "copia.db"
    shutil.copy(leb.MOLTBOOK_DB_PATH, copia)
    log_path = tmp_path / "log.jsonl"

    registro = sqc.registrar_salto_quantico_compactacao(str(copia), str(log_path))
    for chave in (
        "timestamp",
        "gravidade_compactacao_antes",
        "gravidade_compactacao_depois",
        "tamanho_bytes_antes",
        "tamanho_bytes_depois",
        "acertabilidade_modelo",
        "n_amostras",
    ):
        assert chave in registro
    assert registro["n_amostras"] == len(leb.ler_serie_batista_energy_moltbook(str(copia)))
