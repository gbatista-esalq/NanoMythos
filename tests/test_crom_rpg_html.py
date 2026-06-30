import pytest
import os
from bs4 import BeautifulSoup

@pytest.fixture
def html_content():
    html_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ui", "crom_rpg_dashboard.html")
    with open(html_path, 'r', encoding='utf-8') as f:
        return f.read()

def test_crom_rpg_html_structure(html_content):
    """Verifica se os elementos vitais do HUD RPG estão presentes."""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Verifica a existência dos containers vitais
    assert soup.find(id="hud-crom") is not None, "Container Principal do HUD Ausente"
    assert soup.find(id="data-sync") is not None, "Display de Sincronia Ausente"
    assert soup.find(id="data-url") is not None, "Display de URL Ausente"
    assert soup.find(id="data-title") is not None, "Display de Título Ausente"
    assert soup.find(id="data-mass") is not None, "Display de Massa Ausente"

def test_crom_rpg_html_script_fetch(html_content):
    """Verifica se a lógica de fetch está implementada."""
    soup = BeautifulSoup(html_content, 'html.parser')
    scripts = soup.find_all("script")
    has_fetch = False
    for script in scripts:
        if script.string and "fetch('crom_data.json" in script.string:
            has_fetch = True
            break
            
    assert has_fetch, "Lógica de fetch assíncrono para crom_data.json não encontrada no script."
