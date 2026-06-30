"""
Test suite: Chronicles Manim scene integrity.
Verifies Python structure, helper functions, act methods, and subtitle logic.
"""
import ast
import os
import re
import sys
import pytest

MEDIA_DIR = os.path.join(os.path.dirname(__file__), '..', 'media')
MANIM_PATH = os.path.join(MEDIA_DIR, 'chronicles_manim.py')


@pytest.fixture(scope='module')
def source():
    assert os.path.exists(MANIM_PATH), f"Not found: {MANIM_PATH}"
    with open(MANIM_PATH, encoding='utf-8') as f:
        return f.read()


@pytest.fixture(scope='module')
def tree(source):
    return ast.parse(source)


# ── File integrity ──────────────────────────────────────────────

class TestFileIntegrity:
    def test_file_exists(self):
        assert os.path.exists(MANIM_PATH)

    def test_valid_python_syntax(self, source):
        try:
            ast.parse(source)
        except SyntaxError as e:
            pytest.fail(f"SyntaxError in chronicles_manim.py: {e}")

    def test_file_not_empty(self, source):
        assert len(source) > 3000


# ── Color palette constants ─────────────────────────────────────

class TestPalette:
    COLORS = {
        'CYAN':    '#00e5ff',
        'PURPLE':  '#7000ff',
        'MAGENTA': '#ff2d78',
        'YELLOW':  '#ffe500',
        'GREEN':   '#00ff88',
    }

    def test_all_palette_colors_defined(self, source):
        for name, hex_val in self.COLORS.items():
            assert name in source, f"Missing palette constant: {name}"
            assert hex_val in source.lower(), f"Missing hex value: {hex_val}"

    def test_background_color_set(self, source):
        assert 'background_color' in source
        assert '#020205' in source.lower() or 'BG' in source


# ── Helper functions ────────────────────────────────────────────

class TestHelperFunctions:
    def test_glow_dot_defined(self, source):
        assert 'def glow_dot(' in source

    def test_glow_orb_defined(self, source):
        assert 'def glow_orb(' in source

    def test_glow_dot_has_three_layers(self, source):
        dot_block = source[source.index('def glow_dot('):]
        dot_block = dot_block[:dot_block.index('\ndef ')]
        assert dot_block.count('Circle(') >= 3

    def test_glow_orb_has_four_layers(self, source):
        # glow_dot (3) + glow_orb (4) = at least 7 Circle() calls in helper section
        helper_end = source.index('class ChroniclesScene')
        helper_section = source[:helper_end]
        assert helper_section.count('Circle(') >= 7

    def test_glow_dot_uses_vgroup(self, source):
        assert 'VGroup' in source[source.index('def glow_dot('):source.index('def glow_orb(')]


# ── Scene class structure ───────────────────────────────────────

class TestSceneClass:
    REQUIRED_METHODS = [
        'construct', 'intro', 'act1_network', 'act2_entropy',
        'act3_entanglement', 'finale',
        '_act_label', '_subtitle', '_subtitle_hl', '_subtitle_mixed',
        '_build_dna', '_build_spacetime_grid',
    ]

    def test_chronicles_scene_class_exists(self, source):
        assert 'class ChroniclesScene(Scene):' in source

    def test_construct_calls_all_acts(self, source):
        assert 'self.intro()' in source
        assert 'self.act1_network()' in source
        assert 'self.act2_entropy()' in source
        assert 'self.act3_entanglement()' in source
        assert 'self.finale()' in source

    @pytest.mark.parametrize("method", REQUIRED_METHODS)
    def test_method_exists(self, source, method):
        assert f'def {method}(' in source, f"Missing method: {method}"


# ── Act content correctness ─────────────────────────────────────

class TestActContent:
    def test_intro_has_parametric_string(self, source):
        assert 'ParametricFunction' in source

    def test_act1_has_network_nodes(self, source):
        assert 'glow_dot(' in source
        assert 'node_data' in source

    def test_act1_has_edges(self, source):
        assert 'LineBasicMaterial' in source or 'Line(' in source

    def test_act1_has_outer_ring(self, source):
        assert 'ring' in source and 'Circle(' in source

    def test_act2_has_entropy_particles(self, source):
        assert 'n_particles' in source or 'particles' in source

    def test_act2_has_dna_helix(self, source):
        assert '_build_dna' in source
        assert 'VMobject' in source

    def test_act2_dna_has_two_strands(self, source):
        dna_block = source[source.index('def _build_dna('):]
        dna_block = dna_block[:dna_block.index('\n    def ')]
        assert 'strand1' in dna_block and 'strand2' in dna_block

    def test_act2_has_411_counter(self, source):
        assert '411' in source

    def test_act3_has_glow_orbs(self, source):
        assert 'glow_orb(' in source
        assert 'orb_L' in source and 'orb_R' in source

    def test_act3_has_flash_sync(self, source):
        assert 'Flash(' in source

    def test_act3_has_shared_memory_node(self, source):
        assert 'RegularPolygon' in source or 'shared' in source

    def test_act3_has_dashed_beams(self, source):
        assert 'DashedLine(' in source

    def test_act3_has_backend_nodes(self, source):
        assert 'backend' in source
        assert 'Square(' in source

    def test_finale_has_credits(self, source):
        assert 'ESALQ' in source or 'Synapse Hub' in source


# ── Subtitle logic ──────────────────────────────────────────────

class TestSubtitleLogic:
    def test_subtitle_has_rounded_rect_bg(self, source):
        assert 'RoundedRectangle' in source

    def test_subtitle_hl_arranges_texts(self, source):
        assert 'arrange(RIGHT' in source

    def test_subtitle_mixed_correct_tuple_order(self, source):
        # Must unpack (before, after, hl_color, _) NOT (before, after, _, hl_color)
        assert 'before, after, hl_color, _' in source

    def test_subtitle_positioned_at_bottom(self, source):
        assert 'to_edge(DOWN' in source

    def test_accent_restored_in_entanglement_sub(self, source):
        assert 'fantasmagórica' in source or 'fantasmagorica' in source
        assert 'distância' in source or 'distancia' in source


# ── DNA helix ───────────────────────────────────────────────────

class TestDNAHelix:
    def test_dna_has_rungs(self, source):
        assert 'rungs' in source

    def test_dna_has_correct_strand_colors(self, source):
        dna_block = source[source.index('def _build_dna('):]
        dna_block = dna_block[:dna_block.index('\n    def ')]
        assert 'CYAN' in dna_block
        assert 'MAGENTA' in dna_block
        assert 'YELLOW' in dna_block

    def test_dna_is_parametric_helix(self, source):
        assert 'np.cos(' in source or 'cos(' in source

    def test_dna_returns_vgroup(self, source):
        dna_block = source[source.index('def _build_dna('):]
        dna_block = dna_block[:dna_block.index('\n    def ')]
        assert 'return VGroup' in dna_block


# ── Spacetime grid ──────────────────────────────────────────────

class TestSpacetimeGrid:
    def test_grid_has_horizontal_lines(self, source):
        grid_block = source[source.index('def _build_spacetime_grid('):]
        grid_block = grid_block[:grid_block.index('\n    def ')]
        assert 'Line(' in grid_block

    def test_grid_uses_purple(self, source):
        grid_block = source[source.index('def _build_spacetime_grid('):]
        grid_block = grid_block[:grid_block.index('\n    def ')]
        assert 'PURPLE' in grid_block

    def test_grid_returns_vgroup(self, source):
        grid_block = source[source.index('def _build_spacetime_grid('):]
        grid_block = grid_block[:grid_block.index('\n    def ')]
        assert 'return grid' in grid_block
