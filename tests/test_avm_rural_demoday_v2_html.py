import pytest
import os
import re

HTML_PATH = os.path.join(
    os.path.dirname(__file__), '..',
    'AVM_Rural_EntregaFinal_Demoday_v2.html'
)

@pytest.fixture
def html():
    if not os.path.exists(HTML_PATH):
        return ''
    with open(HTML_PATH, 'r', encoding='utf-8') as f:
        return f.read()

def test_file_exists():
    assert os.path.exists(HTML_PATH), 'AVM_Rural_EntregaFinal_Demoday_v2.html nao encontrado'

def test_valid_doctype(html):
    assert html.strip().startswith('<!DOCTYPE html>'), 'DOCTYPE ausente'

def test_has_sebrae_brand(html):
    assert 'SEBRAE' in html or 'Sebrae' in html

def test_has_demoday(html):
    assert 'Demoday' in html or 'demoday' in html

def test_has_6_slides(html):
    ids = re.findall(r'id=["\']slide-\d+["\']', html)
    assert len(ids) >= 6, f'Esperado 6+ slides, encontrado {len(ids)}'

def test_has_slide_1(html):
    assert 'id="slide-1"' in html

def test_has_slide_6(html):
    assert 'id="slide-6"' in html

def test_has_bg_canvas(html):
    assert '<canvas' in html, 'Canvas para animacao ausente'

def test_has_pipe_fapesp(html):
    assert 'PIPE' in html and 'FAPESP' in html, 'Secao PIPE FAPESP ausente'

def test_has_bolsa_equipe(html):
    assert 'bolsa' in html.lower() or 'Bolsa' in html, 'Informacao de bolsa ausente'

def test_has_esalq_usp(html):
    assert 'ESALQ' in html and 'USP' in html, 'Parceria ESALQ-USP ausente'

def test_has_cac_ltv(html):
    assert '1.200' in html, 'CAC R$1.200 ausente'
    assert '14.000' in html, 'LTV R$14.000 ausente'

def test_has_ltv_cac_ratio(html):
    assert '11.7' in html, 'Ratio LTV/CAC 11.7x ausente'

def test_has_seed_valuation(html):
    assert '500K' in html or '500.000' in html, 'Seed R$500K ausente'
    assert '2M' in html or '2.000.000' in html or '2 M' in html, 'Valuation R$2M ausente'

def test_has_okrs(html):
    assert 'OKR' in html, 'OKRs ausentes'

def test_has_rrm(html):
    assert '25' in html and ('RRM' in html or 'rrm' in html.lower()), 'RRM alvo ausente'

def test_has_precificacao(html):
    assert '490' in html, 'Tier R$490 ausente'
    assert '990' in html, 'Tier R$990 ausente'
    assert '2.500' in html, 'Tier R$2.500 ausente'

def test_has_tam_sam_som(html):
    assert 'TAM' in html and 'SAM' in html and 'SOM' in html

def test_has_founder_info(html):
    assert 'Gabriel Batista' in html

def test_has_email_contato(html):
    assert 'negocios.gabrielbatista@gmail.com' in html

def test_has_nps_csat(html):
    assert 'NPS' in html, 'Campo NPS ausente'
    assert 'CSAT' in html or 'satisfa' in html.lower(), 'Campo CSAT ausente'

def test_has_confirmacao_integrantes(html):
    assert 'integrante' in html.lower(), 'Confirmacao de integrantes ausente'

def test_has_sidebar_nav(html):
    assert 'sidebar' in html, 'Sidebar de navegacao ausente'

def test_has_jarvis(html):
    assert 'J.A.R.V.I.S' in html or 'JARVIS' in html, 'J.A.R.V.I.S. ausente'

def test_no_relative_img_src(html):
    bad = re.findall(r'<img[^>]+src=["\'](?!data:|http|https|//)[^"\']+["\']', html)
    assert len(bad) == 0, f'Imagens com src relativo: {bad}'

def test_sem_em_dash(html):
    assert '—' not in html, 'Em-dash (—) encontrado no HTML'
