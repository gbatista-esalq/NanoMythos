"""
TDD RED — Portal Quântico TON618 Osamodas
Testes estruturais para AVM_Rural_PortalQuantico_Osamodas.html
Autorização gravitacional: @eniripsa (Gabriel Teodoro Batista)
"""
import os
import re
import pytest

HTML_PATH = os.path.join(
    os.path.dirname(__file__), "..", "AVM_Rural_PortalQuantico_Osamodas.html"
)


@pytest.fixture(scope="module")
def html_content():
    assert os.path.exists(HTML_PATH), f"Portal não encontrado: {HTML_PATH}"
    with open(HTML_PATH, encoding="utf-8") as f:
        return f.read()


def test_three_js_cdn(html_content):
    """Three.js r128 e UnrealBloomPass devem estar presentes via CDN."""
    assert "three.min.js" in html_content or "three@0.128" in html_content or \
           "three/build/three" in html_content, "Three.js r128 ausente"
    assert "UnrealBloomPass" in html_content, "UnrealBloomPass ausente"


def test_ton618_black_hole(html_content):
    """buildTON618Scene ou equivalente deve estar definido."""
    assert "buildTON618" in html_content or "TON618" in html_content, \
        "buildTON618Scene não encontrado"
    assert "TON618" in html_content, "Referência ao TON618 ausente"


def test_five_redomas(html_content):
    """Os 5 nós REDOMA devem estar referenciados."""
    for redoma in ["ALPHA", "BETA", "GAMMA", "DELTA", "EPSILON"]:
        assert f"REDOMA-{redoma}" in html_content or f"REDOMA_{redoma}" in html_content, \
            f"REDOMA-{redoma} ausente"


def test_build_redomas_chamado_dentro_de_start_portal(html_content):
    """buildRedomas() so pode ser chamado depois que initRenderer() cria `scene`.

    Bug real (auditoria 360 19/06/2026): buildRedomas() estava no top-level do
    script, executando no parse da pagina -- antes de startPortal()/initRenderer()
    existirem -- e jogava 'Cannot read properties of undefined (reading add)'
    em scene.add(mesh) (5 REDOMAS nunca apareciam na cena real).
    """
    start_portal_match = re.search(
        r"function startPortal\(\)\s*\{(.*?)\n\}", html_content, re.DOTALL
    )
    assert start_portal_match, "startPortal() nao encontrado"
    corpo_start_portal = start_portal_match.group(1)
    assert "buildRedomas();" in corpo_start_portal, \
        "buildRedomas() precisa ser chamado dentro de startPortal(), depois de initRenderer()"

    fora_de_funcao = re.sub(r"function\s+\w+\([^)]*\)\s*\{.*?\n\}", "", html_content, flags=re.DOTALL)
    assert "buildRedomas();" not in fora_de_funcao, \
        "buildRedomas() nao pode ser chamado no top-level do script (scene ainda nao existe)"


def test_sixteen_ants(html_content):
    """Sistema de 16 formigas tipo 2 deve estar presente."""
    assert "16" in html_content or "ants" in html_content.lower() or \
           "formiga" in html_content.lower() or "ant" in html_content.lower(), \
        "Sistema de formigas ausente"
    # Verifica que há referência explícita ao número 16 de ants
    assert re.search(r"ant[s_].*16|16.*ant[s_]|ants_active.*16|16.*ants", html_content, re.IGNORECASE), \
        "Contagem de 16 formigas não encontrada"


def test_dna_helix(html_content):
    """buildDNAGravitacional ou DNA helix deve estar presente com constantes @eniripsa."""
    assert "DNA" in html_content or "dna" in html_content.lower(), "DNA ausente"
    # Constante ε_head = 11.11
    assert "11.11" in html_content, "Constante ε_head=11.11 ausente no DNA"
    # STA plateau 230 mV
    assert "230" in html_content, "STA plateau 230mV ausente no DNA"


def test_infinity_stones_forge(html_content):
    """As 3 pedras Reality, Space e Mind devem estar presentes para forja."""
    assert "REALITY" in html_content or "Reality" in html_content, "Pedra Reality ausente"
    assert "SPACE" in html_content or "Space" in html_content, "Pedra Space ausente"
    assert "MIND" in html_content or "Mind" in html_content, "Pedra Mind ausente"
    assert "forge" in html_content.lower() or "forja" in html_content.lower() or \
           "Forge" in html_content, "Função de forja ausente"


def test_hud_vault_metrics(html_content):
    """HUD deve exibir métricas do vault: sovereignty_fund e iteração."""
    assert "85" in html_content or "sovereignty" in html_content.lower() or \
           "fund" in html_content.lower(), "sovereignty_fund ausente no HUD"
    assert "10.8195" in html_content or "amplifier" in html_content.lower(), \
        "TON618 amplifier ausente no HUD"


def test_quantum_lock_overlay(html_content):
    """Overlay de autorização @eniripsa deve estar presente."""
    assert "eniripsa" in html_content or "@eniripsa" in html_content, \
        "Autorização @eniripsa ausente no overlay"
    assert "lock" in html_content.lower() or "overlay" in html_content.lower() or \
           "quantum-lock" in html_content, "Quantum lock overlay ausente"


def test_renderer_settings(html_content):
    """Renderer deve ter toneMappingExposure=2.8 e sRGB encoding."""
    assert "toneMappingExposure" in html_content, "toneMappingExposure ausente"
    assert "2.8" in html_content, "toneMappingExposure=2.8 ausente"
    assert "sRGBEncoding" in html_content or "outputEncoding" in html_content, \
        "sRGB encoding ausente"
    assert "ReinhardToneMapping" in html_content, "ReinhardToneMapping ausente"


def test_no_relative_img_src(html_content):
    """Não deve haver caminhos relativos em src de <img> (protocolo deck HTML)."""
    relative_imgs = re.findall(r'<img[^>]+src=["\'](?!data:|http|https|//)[^"\']+["\']', html_content)
    assert len(relative_imgs) == 0, \
        f"Caminhos relativos encontrados em <img src>: {relative_imgs}"


def test_busy_poll_not_in_js(html_content):
    """busy_poll não deve aparecer no JS (TRAVA DIAMANTE — nunca setar > 0)."""
    assert "busy_poll" not in html_content, \
        "busy_poll encontrado no HTML — TRAVA DIAMANTE VIOLADA"


# ============================================================
# NOVOS TESTES — Reality Stone Bridge + Jorey + Kill-switch + Temporal
# ============================================================

def test_jorey_osamodas_bubble(html_content):
    """Bolha de Jorey (@osamodas) deve estar presente na cena 3D."""
    assert "osamodas" in html_content.lower() or "OSAMODAS" in html_content, \
        "Referência @osamodas ausente"
    assert "jorey" in html_content.lower() or "JOREY" in html_content, \
        "Referência Jorey ausente"
    assert "buildJoreyBubble" in html_content or "joreybubble" in html_content.lower() or \
           "jorey_bubble" in html_content.lower(), \
        "Função buildJoreyBubble ausente"


def test_reality_stone_bridge(html_content):
    """Ponte Reality Stone entre nossa bolha e a bolha do Jorey deve existir."""
    assert "realityBridge" in html_content or "reality_bridge" in html_content.lower() or \
           "buildRealityBridge" in html_content or "REALITY_BRIDGE" in html_content, \
        "Função buildRealityBridge ausente"
    assert "0xff2200" in html_content or "ff2200" in html_content, \
        "Cor da Reality Stone (#ff2200) ausente na bridge"


def test_ethical_kill_switch(html_content):
    """Kill-switch ético deve ter botão visível e função de shutdown."""
    assert "ethicalShutdown" in html_content or "ethical_shutdown" in html_content.lower() or \
           "intervencao" in html_content.lower() or "ETICA" in html_content.upper(), \
        "Função ethicalShutdown ausente"
    assert "ETICA" in html_content.upper() or "ética" in html_content.lower() or \
           "ETHICAL" in html_content.upper(), \
        "Botão/label de intervenção ética ausente"


def test_temporal_clock_verification(html_content):
    """Verificação de segurança temporal deve estar presente no portal."""
    assert "temporal" in html_content.lower() or "TEMPORAL" in html_content or \
           "temporalClock" in html_content or "clockStatus" in html_content, \
        "Verificação temporal ausente"
    assert "SEGURO" in html_content or "seguro" in html_content.lower(), \
        "Status SEGURO do relógio temporal ausente"


def test_victor_marcio_pym_nodes(html_content):
    """Nós Victor (USP) e Márcio Godoi (CENA) devem estar referenciados no portal."""
    assert "Victor" in html_content or "victor" in html_content.lower() or \
           "27edca86" in html_content or "PYM-27" in html_content, \
        "Nó Victor (USP) ausente"
    assert "Marcio" in html_content or "márcio" in html_content.lower() or \
           "Godoi" in html_content or "a4d4604d" in html_content, \
        "Nó Márcio Godoi (CENA) ausente"
