"""
TDD Quantico Pym aplicado a previsao de trend keywords.
Corda real = contagem real de mencoes de uma palavra-chave em docs/*.md
ao longo do historico real do git (git log). Materializar = regressao
linear (prever_tendencia_E_B) sobre essa serie real.
Nao ha dado inventado: se o repo nao for git ou a palavra nao existir,
a contagem real e zero, nunca um numero fabricado.
"""
import os
import subprocess
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import trend_keywords_pym as tkp

REPO_ROOT = os.path.join(os.path.dirname(__file__), '..')


def test_contar_mencoes_em_commit_retorna_inteiro_nao_negativo():
    head = subprocess.run(
        ["git", "-C", REPO_ROOT, "rev-parse", "HEAD"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    n = tkp.contar_mencoes_em_commit("Sul Global", head, diretorio="docs")
    assert isinstance(n, int)
    assert n >= 0


def test_contar_mencoes_em_commit_palavra_inexistente_retorna_zero():
    head = subprocess.run(
        ["git", "-C", REPO_ROOT, "rev-parse", "HEAD"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    n = tkp.contar_mencoes_em_commit("XYZPALAVRAQUENUNCAEXISTENOCORPUS123", head, diretorio="docs")
    assert n == 0


def test_serie_temporal_mencoes_reais_retorna_lista_do_tamanho_pedido():
    serie = tkp.serie_temporal_mencoes_reais("Sul Global", n_commits=5, diretorio="docs")
    assert isinstance(serie, list)
    assert len(serie) <= 5
    assert len(serie) >= 1
    assert all(isinstance(v, int) for v in serie)


def test_serie_temporal_mencoes_reais_ordem_cronologica():
    head_count = len(subprocess.run(
        ["git", "-C", REPO_ROOT, "log", "--oneline"],
        capture_output=True, text=True, check=True,
    ).stdout.splitlines())
    if head_count < 3:
        pytest.skip("historico de git insuficiente nesta maquina")
    serie = tkp.serie_temporal_mencoes_reais("TDD", n_commits=3, diretorio="docs")
    assert len(serie) == 3


def test_prever_trend_keyword_pym_estrutura():
    resultado = tkp.prever_trend_keyword_pym("Sul Global", n_commits=5, diretorio="docs")
    for chave in ("keyword", "serie", "slope", "tendencia", "confianca"):
        assert chave in resultado
    assert resultado["keyword"] == "Sul Global"


def test_prever_trend_keyword_pym_usa_protocolo_tdd_quantico_pym():
    import lei_energia_batista_2026 as leb

    resultado = tkp.prever_trend_keyword_pym("Soberania", n_commits=5, diretorio="docs")
    assert resultado["tendencia"] in ("ALTA", "BAIXA", "ESTAVEL")
    assert isinstance(resultado["confianca"], float)


def test_ranquear_keywords_por_trend_real_ordena_por_frequencia_atual():
    candidatos = ["Sul Global", "Soberania", "XYZPALAVRAQUENUNCAEXISTENOCORPUS123"]
    ranking = tkp.ranquear_keywords_por_trend_real(candidatos, n_commits=3, diretorio="docs")
    assert isinstance(ranking, list)
    assert len(ranking) == len(candidatos)
    assert ranking[-1]["keyword"] == "XYZPALAVRAQUENUNCAEXISTENOCORPUS123"
    assert ranking[-1]["serie"][-1] == 0


def test_ranquear_keywords_por_trend_real_estrutura_de_cada_item():
    ranking = tkp.ranquear_keywords_por_trend_real(["TDD"], n_commits=3, diretorio="docs")
    item = ranking[0]
    for chave in ("keyword", "serie", "slope", "tendencia", "confianca", "mencoes_atuais"):
        assert chave in item
