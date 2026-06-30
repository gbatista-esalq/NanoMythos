"""
TDD Red: AVM_Rural_Entrega3_BusinessPlan.html
3a Entrega Parcial — Business Plan 8 secoes + Resumo 250 chars + OKRs.
Campos exigidos pelo formulario: Resumo Executivo (250 chars), OKRs 6 meses,
Link Canvas Business Plan, Link Pitch Final.
"""
import os
import re

HTML_PATH = os.path.join(
    os.path.dirname(__file__), "..",
    "AVM_Rural_Entrega3_BusinessPlan.html"
)


def read_html():
    with open(HTML_PATH, encoding="utf-8") as f:
        return f.read()


def test_file_exists():
    assert os.path.exists(HTML_PATH), "AVM_Rural_Entrega3_BusinessPlan.html nao existe"


def test_valid_doctype():
    html = read_html()
    assert "<!DOCTYPE html>" in html or "<!doctype html>" in html


def test_has_sebrae_brand():
    html = read_html()
    assert "SEBRAE" in html or "Sebrae" in html


def test_has_win_jovem():
    html = read_html()
    assert "Win Jovem" in html or "WinJovem" in html


def test_has_capa_obrigatoria():
    html = read_html()
    assert "Business Plan" in html, "Titulo obrigatorio 'Business Plan' nao encontrado na capa"


def test_has_titulo_completo():
    html = read_html()
    assert "Projeto Startup Win Jovem Sebrae" in html or "Win Jovem Sebrae" in html, \
        "Titulo completo SEBRAE nao encontrado"


def test_has_sumario_executivo():
    html = read_html()
    assert "Sumario Executivo" in html or "Sumário Executivo" in html, "Secao 1 Sumario Executivo nao encontrada"


def test_has_problema_proposta():
    html = read_html()
    assert "Problema" in html and ("Proposta" in html or "Valor" in html), \
        "Secao 2 Problema/Proposta de Valor nao encontrada"


def test_has_analise_mercado():
    html = read_html()
    assert "Analise" in html or "Análise" in html or "Mercado" in html, "Secao 3 Analise de Mercado nao encontrada"


def test_has_modelo_negocio():
    html = read_html()
    assert "Modelo" in html and ("Neg" in html), "Secao 4 Modelo de Negocio nao encontrada"


def test_has_solucao_mvp():
    html = read_html()
    assert ("Solu" in html or "solucao" in html.lower()) and "MVP" in html, "Secao 5 Solucao/MVP nao encontrada"


def test_has_marketing_vendas():
    html = read_html()
    assert "Marketing" in html and "Vendas" in html, "Secao 6 Marketing/Vendas nao encontrada"


def test_has_okrs_section():
    html = read_html()
    assert "OKR" in html, "Secao 7 OKRs nao encontrada"


def test_has_captacao_recursos():
    html = read_html()
    assert "Capta" in html or "Recursos" in html, "Secao 8 Captacao de Recursos nao encontrada"


def test_has_resumo_250chars():
    html = read_html()
    assert "250" in html or "Resumo Executivo" in html or "Resumo" in html, \
        "Box Resumo Executivo 250 chars nao encontrado"


def test_has_cac():
    html = read_html()
    assert "1.200" in html or "1200" in html, "CAC R$1.200 nao encontrado"


def test_has_ltv():
    html = read_html()
    assert "14.000" in html or "14000" in html, "LTV R$14.000 nao encontrado"


def test_has_seed():
    html = read_html()
    assert "500" in html and ("Seed" in html or "seed" in html), "Rodada Seed R$500K nao encontrada"


def test_has_valuation():
    html = read_html()
    assert "2M" in html or "2.000.000" in html or "2 M" in html, "Valuation R$2M nao encontrado"


def test_has_tam_sam_som():
    html = read_html()
    assert "TAM" in html and "SAM" in html and "SOM" in html, "TAM/SAM/SOM nao encontrado"


def test_has_perfil_tech():
    html = read_html()
    assert "Tech" in html, "Perfil Tech nao encontrado na capa"


def test_has_data_junho():
    html = read_html()
    assert "Junho" in html or "junho" in html or "2026" in html, "Data (Junho/2026) nao encontrada"


def test_no_relative_img_src():
    html = read_html()
    imgs = re.findall(r'<img[^>]+src="([^"]+)"', html)
    for src in imgs:
        assert src.startswith("data:") or src.startswith("http"), \
            f"Imagem com caminho relativo: {src}"


def test_sem_em_dash():
    html = read_html()
    body = re.sub(r'<script.*?</script>', '', html, flags=re.DOTALL)
    body = re.sub(r'<style.*?</style>', '', body, flags=re.DOTALL)
    assert "—" not in body, "Em-dash encontrado no texto HTML"
