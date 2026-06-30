"""
TDD Red: AVM_Rural_Entrega2_Canvas_Mercado.html
2a Entrega Parcial — Canvas 9 blocos, TAM/SAM/SOM, analise competitiva.
"""
import os
import re

HTML_PATH = os.path.join(
    os.path.dirname(__file__), "..",
    "AVM_Rural_Entrega2_Canvas_Mercado.html"
)


def read_html():
    with open(HTML_PATH, encoding="utf-8") as f:
        return f.read()


def test_file_exists():
    assert os.path.exists(HTML_PATH), "AVM_Rural_Entrega2_Canvas_Mercado.html nao existe"


def test_valid_doctype():
    html = read_html()
    assert "<!DOCTYPE html>" in html or "<!doctype html>" in html


def test_has_sebrae_brand():
    html = read_html()
    assert "SEBRAE" in html or "Sebrae" in html


def test_has_win_jovem():
    html = read_html()
    assert "Win Jovem" in html or "WinJovem" in html


def test_has_entrega2_header():
    html = read_html()
    assert "2" in html and ("Entrega" in html or "entrega" in html), "Identificacao 2a Entrega nao encontrada"


def test_has_avm_rural():
    html = read_html()
    assert "AVM Rural" in html


def test_has_canvas_section():
    html = read_html()
    assert "Canvas" in html or "canvas" in html, "Secao Canvas nao encontrada"


def test_has_segmentos_clientes():
    html = read_html()
    assert "Segmento" in html or "segmento" in html or "clientes" in html.lower(), \
        "Bloco Segmentos de Clientes nao encontrado"


def test_has_proposta_valor_bloco():
    html = read_html()
    assert "Proposta" in html and "Valor" in html, "Bloco Proposta de Valor nao encontrado"


def test_has_fontes_receita():
    html = read_html()
    assert "Receita" in html or "receita" in html, "Bloco Fontes de Receita nao encontrado"


def test_has_parcerias():
    html = read_html()
    assert "Parceria" in html or "parceria" in html, "Bloco Parcerias nao encontrado"


def test_has_estrutura_custos():
    html = read_html()
    assert "Custo" in html or "custo" in html, "Bloco Estrutura de Custos nao encontrado"


def test_has_tam():
    html = read_html()
    assert "TAM" in html and ("12" in html or "12bi" in html.lower()), "TAM R$12bi nao encontrado"


def test_has_sam():
    html = read_html()
    assert "SAM" in html and ("1,8" in html or "1.8" in html), "SAM R$1,8bi nao encontrado"


def test_has_som():
    html = read_html()
    assert "SOM" in html and ("18" in html), "SOM R$18M nao encontrado"


def test_has_analise_competitiva():
    html = read_html()
    assert "concorrent" in html.lower() or "competit" in html.lower() or "TOTVS" in html or "Aegro" in html, \
        "Analise competitiva nao encontrada"


def test_has_precificacao():
    html = read_html()
    assert "490" in html and "990" in html, "Precificacao (R$490 / R$990) nao encontrada"


def test_has_founder_info():
    html = read_html()
    assert "Gabriel" in html or "Batista" in html


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
