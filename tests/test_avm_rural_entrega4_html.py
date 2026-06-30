"""
TDD Red: AVM_Rural_EntregaFinal_Demoday.html
Entrega Final / Demoday — Pitch 5 slides aprimorado + info formulario.
Campos exigidos: Resumo 250 chars, OKRs, Link Projeto Final, Link Pitch,
Confirmacao integrantes, CSAT (1-5), NPS (0-10).
"""
import os
import re

HTML_PATH = os.path.join(
    os.path.dirname(__file__), "..",
    "AVM_Rural_EntregaFinal_Demoday.html"
)


def read_html():
    with open(HTML_PATH, encoding="utf-8") as f:
        return f.read()


def test_file_exists():
    assert os.path.exists(HTML_PATH), "AVM_Rural_EntregaFinal_Demoday.html nao existe"


def test_valid_doctype():
    html = read_html()
    assert "<!DOCTYPE html>" in html or "<!doctype html>" in html


def test_has_sebrae_brand():
    html = read_html()
    assert "SEBRAE" in html or "Sebrae" in html


def test_has_demoday():
    html = read_html()
    assert "Demoday" in html or "demoday" in html or "Demo Day" in html or "Entrega Final" in html, \
        "Demoday / Entrega Final nao identificado"


def test_has_5_slides():
    html = read_html()
    count = len(re.findall(r'id="slide-\d+"', html))
    assert count >= 5, f"Esperado >= 5 slides, encontrado {count}"


def test_has_slide_capa():
    html = read_html()
    assert "AVM Rural" in html, "Nome AVM Rural (capa) nao encontrado"


def test_has_slide_problema():
    html = read_html()
    assert "problema" in html.lower() or "dor" in html.lower(), "Slide Problema nao encontrado"


def test_has_slide_solucao():
    html = read_html()
    assert "solu" in html.lower(), "Slide Solucao nao encontrado"


def test_has_slide_mercado():
    html = read_html()
    assert "TAM" in html and "SAM" in html and "SOM" in html, "Slide Mercado TAM/SAM/SOM nao encontrado"


def test_has_slide_modelo():
    html = read_html()
    assert "modelo" in html.lower() and "neg" in html.lower(), "Slide Modelo de Negocio nao encontrado"


def test_has_cac_ltv():
    html = read_html()
    assert ("1.200" in html or "1200" in html) and ("14.000" in html or "14000" in html), \
        "CAC R$1.200 e LTV R$14.000 nao encontrados"


def test_has_ltv_cac_ratio():
    html = read_html()
    assert "11.7" in html or "11,7" in html, "LTV/CAC 11.7x nao encontrado"


def test_has_seed_valuation():
    html = read_html()
    assert "500" in html and ("Seed" in html or "seed" in html), "Rodada Seed nao encontrada"


def test_has_okrs():
    html = read_html()
    assert "OKR" in html, "OKRs nao encontrados"


def test_has_rrm():
    html = read_html()
    assert "25.000" in html or "25000" in html or "RRM" in html, "RRM R$25k nao encontrado"


def test_has_confirmacao_integrantes():
    html = read_html()
    assert "Gabriel Batista" in html or "integrante" in html.lower() or "certificado" in html.lower(), \
        "Confirmacao de integrantes nao encontrada"


def test_has_nps_ou_csat():
    html = read_html()
    assert "NPS" in html or "CSAT" in html or "satisfa" in html.lower(), \
        "NPS ou CSAT nao mencionados"


def test_has_resumo_executivo():
    html = read_html()
    assert "Resumo" in html or "250" in html, "Resumo Executivo para formulario nao encontrado"


def test_has_email_contato():
    html = read_html()
    assert "gabrielbatista" in html or "negocios" in html


def test_has_precificacao():
    html = read_html()
    assert "490" in html and "990" in html and "2.500" in html, "Tiers de precificacao nao encontrados"


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
