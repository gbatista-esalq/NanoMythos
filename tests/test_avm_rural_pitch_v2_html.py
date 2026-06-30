"""
TDD Red: AVM_Rural_CNH_Agro_Pitch_v2.html
Verifica metricas atualizadas WinJovem + estrutura do pitch.
"""
import os
import re

HTML_PATH = os.path.join(
    os.path.dirname(__file__), "..",
    "AVM_Rural_CNH_Agro_Pitch_v2.html"
)


def read_html():
    with open(HTML_PATH, encoding="utf-8") as f:
        return f.read()


def test_file_exists():
    assert os.path.exists(HTML_PATH), "AVM_Rural_CNH_Agro_Pitch_v2.html nao existe"


def test_valid_doctype():
    html = read_html()
    assert "<!DOCTYPE html>" in html or "<!doctype html>" in html


def test_has_5_slides():
    html = read_html()
    count = len(re.findall(r'id="slide-\d+"', html))
    assert count >= 5, f"Esperado >= 5 slides, encontrado {count}"


# --- Metricas WinJovem ---

def test_cac_presente():
    html = read_html()
    assert "1.200" in html or "1200" in html, "CAC R$1.200 nao encontrado"


def test_ltv_presente():
    html = read_html()
    assert "14.000" in html or "14000" in html, "LTV R$14.000 nao encontrado"


def test_ltv_cac_ratio():
    html = read_html()
    assert "11.7" in html or "11,7" in html, "LTV/CAC 11.7x nao encontrado"


def test_rrm_mensal():
    html = read_html()
    assert "25.000" in html or "25000" in html, "RRM R$25.000/mes nao encontrado"


def test_rodada_seed():
    html = read_html()
    assert "500" in html and ("Seed" in html or "seed" in html), "Rodada Seed R$500K nao encontrada"


def test_valuation_premoney():
    html = read_html()
    assert "2M" in html or "2.000.000" in html or "2 M" in html, "Valuation R$2M nao encontrado"


def test_tam():
    html = read_html()
    assert "12" in html and ("bi" in html.lower() or "TAM" in html), "TAM R$12bi nao encontrado"


def test_sam():
    html = read_html()
    assert "1,8" in html or "1.8" in html, "SAM R$1,8bi nao encontrado"


def test_som():
    html = read_html()
    assert "18 M" in html or "18M" in html or "R$ 18" in html, "SOM R$18M nao encontrado"


def test_precificacao_basico():
    html = read_html()
    assert "490" in html, "Tier Basico R$490/mes nao encontrado"


def test_precificacao_profissional():
    html = read_html()
    assert "990" in html, "Tier Profissional R$990/mes nao encontrado"


def test_precificacao_enterprise():
    html = read_html()
    assert "2.500" in html or "2500" in html, "Tier Enterprise R$2.500/mes nao encontrado"


# --- Estrutura do pitch ---

def test_slide_capa():
    html = read_html()
    assert "AVM Rural" in html, "Nome AVM Rural nao encontrado"


def test_slide_problema():
    html = read_html()
    assert "problema" in html.lower() or "dor" in html.lower(), "Slide Problema nao encontrado"


def test_slide_solucao():
    html = read_html()
    assert "solu" in html.lower(), "Slide Solucao nao encontrado"


def test_slide_mercado():
    html = read_html()
    assert "TAM" in html and "SAM" in html and "SOM" in html, "Slide Mercado com TAM/SAM/SOM nao encontrado"


def test_slide_modelo_negocio():
    html = read_html()
    assert "modelo" in html.lower() and "negoc" in html.lower(), "Slide Modelo de Negocio nao encontrado"


def test_contato_email():
    html = read_html()
    assert "gabrielbatista" in html or "negocios" in html, "Email de contato nao encontrado"


def test_founder_market_fit():
    html = read_html()
    assert "Founder" in html or "founder" in html, "Founder-Market Fit nao mencionado"


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
