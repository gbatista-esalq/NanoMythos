"""
TDD estrutural para Dossie_GYG.html — 6 cenas Three.js + fixes de renderização.
Verifica: balanco JS, modos de renderizacao, cenas, bolha pym redesenhada.
"""
import re
import pytest

HTML_PATH = "/home/synapseagtech/Área de Trabalho/Dossie_GYG.html"

@pytest.fixture(scope="module")
def html():
    with open(HTML_PATH, encoding="utf-8") as f:
        return f.read()

@pytest.fixture(scope="module")
def js(html):
    blocks = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
    return '\n'.join(blocks)


# === BALANCO E RENDERER PROTOCOL ===

def test_brace_balance(js):
    opens = js.count('{')
    closes = js.count('}')
    assert opens == closes, f"JS brace mismatch: {opens} opens vs {closes} closes"

def test_tone_mapping_exposure_present(js):
    assert 'toneMappingExposure' in js

def test_output_encoding_present(js):
    assert 'outputEncoding' in js

def test_init_guard_uses_query_selector(js):
    assert "querySelector('canvas')" in js

def test_holo_mode_uses_additive_blending(js):
    assert 'AdditiveBlending' in js

def test_diamond_mode_high_shininess(js):
    assert '1000' in js  # shininess 1000 no modo diamante


# === MODOS DE RENDERIZACAO ===

def test_set_render_mode_rebuilds_colonia(js):
    assert "activeSceneMode === 'colonia'" in js

def test_set_render_mode_rebuilds_vault(js):
    assert "activeSceneMode === 'vault'" in js

def test_four_render_modes_defined(js):
    for mode in ["'wire'", "'solid'", "'holo'", "'diamond'"]:
        assert f"activeRenderMode === {mode}" in js or \
               f'activeRenderMode === {mode}' in js


# === 6 CENAS THREE.JS ===

def test_all_six_build_functions_present(js):
    for fn in ['buildPymScene', 'buildAmazoniaScene', 'buildLangmuirScene',
               'buildNaveQuanticaScene', 'buildColoniaScene', 'buildVaultSobScene']:
        assert fn in js, f"Funcao ausente: {fn}"

def test_switch_scene_handles_all_six_modes(js):
    for mode in ['pym', 'amazonia', 'langmuir', 'nave', 'colonia', 'vault']:
        assert f"mode === '{mode}'" in js, f"switchScene nao trata modo: {mode}"

def test_six_buttons_in_html(html):
    for scene in ['pym', 'amazonia', 'langmuir', 'nave', 'colonia', 'vault']:
        assert f"switchScene('{scene}'" in html, f"Botao ausente: {scene}"


# === BOLHA PYM REDESENHADA (QUANTUM LEAP) ===

def test_pym_scene_has_node_objs(js):
    assert 'nodeObjs' in js

def test_pym_scene_has_flow_particles(js):
    assert 'flowProgress' in js

def test_pym_scene_has_cooperation_rings(js):
    assert 'cooperationRings' in js

def test_pym_scene_has_mini_bubbles(js):
    # cada no tem mini-bolha de cooperacao
    assert 'bubbleMat' in js or 'bubble' in js

def test_pym_animate_updates_node_positions(js):
    assert 'n.angle += n.speed' in js or "n.angle +=" in js

def test_pym_animate_updates_flow_particles(js):
    assert 'flowProgress' in js and 'flowPos' in js


# === OVERFLOW FIX (CANVAS NAO CORTADO) ===

def test_card_navegador_overflow_visible(html):
    assert '#card-navegador' in html and 'overflow: visible' in html

def test_canvas_breakout_full_width(html):
    assert 'canvas-breakout' in html
    assert '100vw' in html


# === MAPA QUANTICO BIODIVERSIDADE (biomap) ===

def test_biomap_build_function_present(js):
    assert 'buildBiomapScene' in js

def test_biomap_button_present(html):
    assert "switchScene('biomap'" in html

def test_biomap_switch_handled(js):
    assert "mode === 'biomap'" in js

def test_biomap_bio_species_embedded(js):
    assert 'BIO_SPECIES' in js

def test_biomap_status_colors_defined(js):
    assert 'STATUS_COLORS' in js
    assert "'CR'" in js

def test_biomap_animate_type_handled(js):
    assert "type === 'biomap'" in js

def test_biomap_species_bubbles_animated(js):
    assert 'speciesBubbles' in js

def test_biomap_edge_processor_fetch(js):
    assert 'localhost:8888' in js

def test_biomap_set_render_mode_handled(js):
    assert "activeSceneMode === 'biomap'" in js

# === LAYOUT GLOBAL (BROWSER + MOBILE) ===

def test_canvas_breakout_no_left_right_conflict(html):
    # usar calc() sem conflito left/right duplo
    assert 'calc(-50vw + 50%)' in html

def test_mobile_media_query_canvas_controls(html):
    mobile_idx = html.find('@media (max-width: 768px)')
    assert mobile_idx != -1
    mobile_section = html[mobile_idx:mobile_idx + 3000]
    assert 'canvas-controls' in mobile_section or 'quantum-canvas' in mobile_section

def test_mobile_hud_panels_hidden(html):
    assert 'scene-metrics' in html
    mobile_idx = html.rfind('@media (max-width: 768px)')
    mobile_section = html[mobile_idx:mobile_idx + 3000]
    assert '.hud-left-panel' in mobile_section or 'scene-metrics' in mobile_section

# === AMAZONIA VIVA ===

def test_amazonia_has_adequate_lighting(js):
    assert '0x336622' in js  # AmbientLight cor visivel (nao preto)

def test_amazonia_has_fireflies(js):
    assert 'fireflies' in js or 'pirilampos' in js.lower()

def test_amazonia_has_fog(js):
    assert 'FogExp2' in js
