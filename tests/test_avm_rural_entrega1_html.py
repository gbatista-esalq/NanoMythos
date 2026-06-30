"""
TDD Red: AVM_Rural_Entrega1_CustomerDiscovery.html
1a Entrega Parcial — Persona, Mapa da Empatia, Proposta de Valor.
"""
import os
import re

HTML_PATH = os.path.join(
    os.path.dirname(__file__), "..",
    "AVM_Rural_Entrega1_CustomerDiscovery.html"
)


def read_html():
    with open(HTML_PATH, encoding="utf-8") as f:
        return f.read()


def test_file_exists():
    assert os.path.exists(HTML_PATH), "AVM_Rural_Entrega1_CustomerDiscovery.html nao existe"


def test_valid_doctype():
    html = read_html()
    assert "<!DOCTYPE html>" in html or "<!doctype html>" in html


def test_has_sebrae_brand():
    html = read_html()
    assert "SEBRAE" in html or "Sebrae" in html, "Marca SEBRAE nao encontrada"


def test_has_win_jovem():
    html = read_html()
    assert "Win Jovem" in html or "WinJovem" in html, "Win Jovem nao encontrado"


def test_has_entrega1_header():
    html = read_html()
    assert "1" in html and ("Entrega" in html or "entrega" in html), "Identificacao 1a Entrega nao encontrada"


def test_has_avm_rural():
    html = read_html()
    assert "AVM Rural" in html, "Nome AVM Rural nao encontrado"


def test_has_persona_section():
    html = read_html()
    assert "persona" in html.lower() or "cliente" in html.lower() or "Rodrigo" in html, "Secao Persona nao encontrada"


def test_has_mapa_empatia():
    html = read_html()
    assert "empatia" in html.lower() or "Empatia" in html, "Mapa da Empatia nao encontrado"


def test_has_pensa_sente():
    html = read_html()
    assert "pensa" in html.lower() or "sente" in html.lower(), "Quadrante Pensa/Sente nao encontrado"


def test_has_dores():
    html = read_html()
    assert "dor" in html.lower() or "dores" in html.lower(), "Quadrante Dores nao encontrado"


def test_has_ganhos():
    html = read_html()
    assert "ganho" in html.lower() or "ganhos" in html.lower(), "Quadrante Ganhos nao encontrado"


def test_has_dor_validada():
    html = read_html()
    assert "fragmenta" in html.lower() or "inefici" in html.lower() or "sobrecarga" in html.lower(), \
        "Dor validada (fragmentacao/ineficiencia) nao encontrada"


def test_has_proposta_valor():
    html = read_html()
    assert "proposta" in html.lower() and "valor" in html.lower(), "Proposta de Valor nao encontrada"


def test_has_customer_discovery():
    html = read_html()
    assert "customer" in html.lower() or "descoberta" in html.lower() or "discovery" in html.lower(), \
        "Customer Discovery nao mencionado"


def test_has_founder_info():
    html = read_html()
    assert "Gabriel" in html or "Batista" in html, "Founder Gabriel Batista nao encontrado"


def test_has_perfil_tech():
    html = read_html()
    assert "Tech" in html or "tech" in html, "Perfil Tech nao encontrado"


def test_has_email_contato():
    html = read_html()
    assert "gabrielbatista" in html or "negocios" in html, "Email de contato nao encontrado"


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
