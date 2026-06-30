"""
Test suite: Chronicles Framework animation package integrity.
Verifies HTML structure, CSS palette, JS act logic, and script doc completeness.
"""
import os
import re
import pytest

MEDIA_DIR = os.path.join(os.path.dirname(__file__), '..', 'media')
DOCS_DIR  = os.path.join(os.path.dirname(__file__), '..', 'docs')

HTML_PATH   = os.path.join(MEDIA_DIR, 'chronicles_framework_animation.html')
SCRIPT_PATH = os.path.join(DOCS_DIR,  'chronicles_framework_script.md')


@pytest.fixture(scope='module')
def html_content():
    assert os.path.exists(HTML_PATH), f"Animation file not found: {HTML_PATH}"
    with open(HTML_PATH, encoding='utf-8') as f:
        return f.read()


@pytest.fixture(scope='module')
def script_content():
    assert os.path.exists(SCRIPT_PATH), f"Script file not found: {SCRIPT_PATH}"
    with open(SCRIPT_PATH, encoding='utf-8') as f:
        return f.read()


# ── File existence ──────────────────────────────────────────────

class TestFilesExist:
    def test_html_animation_exists(self):
        assert os.path.exists(HTML_PATH)

    def test_script_md_exists(self):
        assert os.path.exists(SCRIPT_PATH)

    def test_html_not_empty(self, html_content):
        assert len(html_content) > 5000, "HTML file is suspiciously small"

    def test_script_not_empty(self, script_content):
        assert len(script_content) > 1000


# ── HTML structure ──────────────────────────────────────────────

class TestHTMLStructure:
    def test_has_canvas_element(self, html_content):
        assert '<canvas' in html_content

    def test_has_three_js_import(self, html_content):
        assert 'three.js' in html_content.lower() or 'three.min.js' in html_content

    def test_has_gsap_import(self, html_content):
        assert 'gsap' in html_content.lower()

    def test_has_outfit_font(self, html_content):
        assert 'Outfit' in html_content

    def test_has_fira_code_font(self, html_content):
        assert 'Fira Code' in html_content

    def test_has_subtitle_element(self, html_content):
        assert 'id="subtitle"' in html_content

    def test_has_progress_bar(self, html_content):
        assert 'pfill' in html_content or 'progress' in html_content

    def test_has_three_act_dots(self, html_content):
        assert 'd1' in html_content
        assert 'd2' in html_content
        assert 'd3' in html_content

    def test_has_finale_reveal(self, html_content):
        assert 'finale' in html_content

    def test_has_cover_fade(self, html_content):
        assert 'cover' in html_content


# ── Color palette (Synapse HUB identity) ───────────────────────

class TestColorPalette:
    REQUIRED_COLORS = ['#00e5ff', '#7000ff', '#ff2d78', '#ffe500', '#00ff88', '#020205']

    def test_all_brand_colors_present(self, html_content):
        for color in self.REQUIRED_COLORS:
            assert color in html_content.lower(), f"Missing brand color: {color}"

    def test_cyan_primary(self, html_content):
        assert '00e5ff' in html_content.lower()

    def test_purple_secondary(self, html_content):
        assert '7000ff' in html_content.lower()


# ── Three.js scene objects ──────────────────────────────────────

class TestThreeJSObjects:
    def test_has_star_field(self, html_content):
        assert 'Stars' in html_content or 'stars' in html_content or 'PointsMaterial' in html_content

    def test_has_network_nodes(self, html_content):
        assert 'SphereGeometry' in html_content

    def test_has_edges(self, html_content):
        assert 'LineBasicMaterial' in html_content

    def test_has_dna_helix(self, html_content):
        assert 'dna' in html_content.lower() or 'DNA' in html_content

    def test_has_entropy_cloud(self, html_content):
        assert 'entMat' in html_content or 'entropy' in html_content.lower()

    def test_has_spacetime_grid(self, html_content):
        assert 'PlaneGeometry' in html_content or 'grid' in html_content.lower()

    def test_has_quantum_orbs(self, html_content):
        assert 'orbL' in html_content and 'orbR' in html_content

    def test_has_shared_memory_node(self, html_content):
        assert 'OctahedronGeometry' in html_content or 'sharedNode' in html_content

    def test_has_pointer_beams(self, html_content):
        assert 'LineDashedMaterial' in html_content or 'beam' in html_content.lower()

    def test_has_backend_nodes(self, html_content):
        assert 'backend' in html_content.lower() or 'backendMeshes' in html_content


# ── Act transitions ────────────────────────────────────────────

class TestActLogic:
    def test_has_three_acts(self, html_content):
        assert 'startAct2' in html_content
        assert 'startAct3' in html_content

    def test_act1_starts_at_t3(self, html_content):
        # subtitle at t=3.x seconds
        assert '3.5' in html_content or "'3'" in html_content or '"3"' in html_content

    def test_act2_transition_at_40s(self, html_content):
        assert '>= 40' in html_content or '>=40' in html_content

    def test_act3_transition_at_80s(self, html_content):
        assert '>= 80' in html_content or '>=80' in html_content

    def test_has_entanglement_sync_flash(self, html_content):
        assert 'sync' in html_content or 'emissiveIntensity' in html_content

    def test_has_dna_reveal_delay(self, html_content):
        assert '22000' in html_content or 'delay:22' in html_content

    def test_has_backend_reveal_delay(self, html_content):
        assert '20000' in html_content or 'delay:20' in html_content

    def test_camera_orbits_in_act1(self, html_content):
        assert 'Math.sin' in html_content and 'camera.position' in html_content

    def test_has_restart_keybinding(self, html_content):
        assert "key === 'r'" in html_content or "key==='r'" in html_content or 'reload' in html_content

    def test_gsap_timeline_paused_then_played(self, html_content):
        assert 'paused:true' in html_content or "paused: true" in html_content
        assert 'tl.play()' in html_content


# ── Script document quality ─────────────────────────────────────

class TestNarratorScript:
    def test_has_three_acts_in_script(self, script_content):
        assert 'ATO I' in script_content
        assert 'ATO II' in script_content
        assert 'ATO III' in script_content

    def test_covers_edge_computing(self, script_content):
        assert 'Edge Computing' in script_content

    def test_covers_packet_loss(self, script_content):
        assert 'packet loss' in script_content.lower()

    def test_covers_dna_compression(self, script_content):
        assert '411' in script_content

    def test_covers_entanglement_pointer(self, script_content):
        assert 'ponteiro' in script_content.lower() or 'pointer' in script_content.lower() \
               or 'endereço de memória' in script_content.lower()

    def test_has_direction_notes(self, script_content):
        assert 'Direção' in script_content or 'direção' in script_content or 'NOTAS' in script_content

    def test_has_gregory_quant_context(self, script_content):
        assert 'Gregory' in script_content or 'físico' in script_content

    def test_approximately_two_minutes(self, script_content):
        # Rough word count — 2 min ≈ 250-350 words in narration sections
        narration_lines = [
            l.strip() for l in script_content.split('\n')
            if l.strip().startswith('>')
        ]
        words = sum(len(re.findall(r'\w+', l)) for l in narration_lines)
        assert 200 <= words <= 450, f"Script word count out of range: {words}"
