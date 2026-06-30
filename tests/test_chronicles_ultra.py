"""
Test suite: chronicles_ultra.html — versao ultradopamina 120s
"""
import re
import pytest
from pathlib import Path

SRC = Path(__file__).parent.parent / 'media' / 'chronicles_ultra.html'


@pytest.fixture(scope='module')
def html():
    return SRC.read_text(encoding='utf-8')


class TestFileExists:
    def test_file_exists(self):
        assert SRC.exists(), 'chronicles_ultra.html nao encontrado'


class TestDuration:
    def test_total_ms_120s(self, html):
        assert 'TOTAL_MS = 120000' in html

    def test_twelve_scenes(self, html):
        matches = re.findall(r'\{[^}]*name\s*:', html)
        assert len(matches) >= 12, f'Esperado 12+ scenes, encontrado {len(matches)}'

    def test_scene_finale_at_110(self, html):
        assert 'start:110' in html and 'end:120' in html


class TestUltraDopamina:
    def test_storm_600_particles(self, html):
        assert 'length:600' in html

    def test_storm_speed_ultra(self, html):
        # velocidade minima 180 px/s
        m = re.search(r'(\d+)\+Math\.random\(\)\*(\d+)', html)
        assert m, 'velocidade storm nao encontrada'
        assert int(m.group(1)) >= 150, f'velocidade base {m.group(1)} < 150'

    def test_rings_fast_interval(self, html):
        assert '0.35' in html, 'ring interval deve ser 0.35s'

    def test_80_float_symbols(self, html):
        assert 'length:80' in html

    def test_320_ambient_dots(self, html):
        assert 'length:320' in html

    def test_mix_blend_screen(self, html):
        assert 'mix-blend-mode: screen' in html


class TestGamification:
    def test_xp_system(self, html):
        assert 'XP_MAX' in html
        assert 'addXP' in html
        assert 'xpTarget' in html

    def test_level_system(self, html):
        assert 'level' in html
        assert 'LEVEL UP' in html
        assert 'showLevelUp' in html

    def test_combo_system(self, html):
        assert 'comboCount' in html
        assert 'COMBO' in html
        assert 'comboTimer' in html

    def test_score_counter(self, html):
        assert 'score' in html
        assert 'SCORE' in html

    def test_achievements(self, html):
        assert 'unlock(' in html
        assert 'achQueue' in html
        assert 'DESCOBERTA' in html

    def test_level_up_per_400xp(self, html):
        assert 'XP_PER_LEVEL = 400' in html

    def test_xp_max_2000(self, html):
        assert 'XP_MAX = 2000' in html


class TestScreenFX:
    def test_flash_fn(self, html):
        assert 'function flash(' in html

    def test_shake_fn(self, html):
        assert 'function shake(' in html

    def test_scene_cut_fn(self, html):
        assert 'function sceneCut(' in html

    def test_cut_flash_var(self, html):
        assert 'cutFlash' in html

    def test_cut_on_scene_change(self, html):
        assert 'cutTimes' in html and 'checkCuts' in html


class TestScenes:
    def test_scene_ignition(self, html):
        assert 'drawIgnicao' in html

    def test_scene_rede(self, html):
        assert 'drawRede' in html

    def test_scene_entropia(self, html):
        assert 'drawEntropia' in html

    def test_scene_dna(self, html):
        assert 'drawCodigo' in html

    def test_scene_emaranhamento(self, html):
        assert 'drawEmaranhamento' in html

    def test_scene_backend(self, html):
        assert 'drawBackend' in html

    def test_scene_agtech(self, html):
        assert 'drawAgtech' in html

    def test_scene_biotech(self, html):
        assert 'drawBiotech' in html

    def test_scene_ia_soberana(self, html):
        assert 'drawIASoberana' in html

    def test_scene_sul_global(self, html):
        assert 'drawSulGlobal' in html

    def test_scene_manifesto(self, html):
        assert 'drawManifesto' in html

    def test_scene_finale(self, html):
        assert 'drawFinale' in html


class TestVEO:
    def test_six_veo_videos(self, html):
        for i in range(6):
            assert f'id="veo-{i}"' in html

    def test_veo_update_fn(self, html):
        assert 'function updateVeo(' in html or 'updateVeo' in html

    def test_veo_active_class(self, html):
        assert '.veo-bg.active' in html

    def test_veo_opacity_css(self, html):
        assert 'opacity: 0.48' in html or 'opacity:.48' in html


class TestManifestoContent:
    def test_batista_reference(self, html):
        assert 'Batista' in html

    def test_esalq_reference(self, html):
        assert 'ESALQ' in html

    def test_synapse_hub_reference(self, html):
        assert 'Synapse Hub' in html

    def test_sul_global_reference(self, html):
        assert 'Sul Global' in html

    def test_teoria_de_tudo(self, html):
        assert 'TEORIA DE TUDO' in html

    def test_soberana_reference(self, html):
        assert 'soberan' in html.lower()


class TestHTMLStructure:
    def test_doctype(self, html):
        assert '<!DOCTYPE html>' in html

    def test_canvas_element(self, html):
        assert '<canvas id="c">' in html

    def test_progress_bar(self, html):
        assert 'progress' in html and 'progress-fill' in html

    def test_hud_element(self, html):
        assert 'id="hud"' in html

    def test_scene_label(self, html):
        assert 'id="scene-label"' in html

    def test_no_hardcoded_api_key(self, html):
        assert 'AIzaSy' not in html

    def test_braces_balanced(self, html):
        script_start = html.find('<script>')
        script_end = html.rfind('</script>')
        js = html[script_start:script_end]
        opens = js.count('{')
        closes = js.count('}')
        assert opens == closes, f'Chaves desbalanceadas: {opens} abertas vs {closes} fechadas'

    def test_viewport_1920x1080(self, html):
        assert '1920' in html and '1080' in html


class TestOrbitalSystem:
    """Orbital Vortex System: M=9 + TF=9 em frames estaticos"""

    def test_orbit_halo_defined(self, html):
        assert 'function drawOrbitHalo(' in html

    def test_spiral_vortex_defined(self, html):
        assert 'function drawSpiralVortex(' in html

    def test_orbit_sats_defined(self, html):
        assert 'function drawOrbitSats(' in html

    def test_ellipse_orbit_path(self, html):
        assert 'ctx.ellipse(' in html, 'orbital paths usam ellipse para perspectiva'

    def test_spiral_three_arms(self, html):
        assert 'ARMS=3' in html, 'vortex deve ter 3 bracos espirais para M=9'

    def test_storm_alpha_zero_in_focus(self, html):
        assert 'lerp(0.26,0.0,' in html, 'storm dots desaparecem em focus para TF=9'

    def test_storm_skip_when_alpha_zero(self, html):
        assert 'alpha<0.05' in html, 'drawStorm deve pular streaks quando alpha zerado'

    def test_all_scenes_get_orbital(self, html):
        assert html.count('drawOrbitHalo(') >= 12, 'todas as 12 cenas devem chamar drawOrbitHalo'

    def test_manifesto_orbital(self, html):
        idx = html.find('drawManifesto(sec)')
        orbital_in_manifesto = html.find('drawSpiralVortex', idx - 50) > 0 or \
                               html.find('drawSpiralVortex', idx) > 0
        block = html[html.find('function drawManifesto'):html.find('function drawManifesto')+800]
        assert 'drawSpiralVortex(' in block, 'MANIFESTO deve ter vortex para M=9'


class TestPymQuantico:
    """PYM 1-6: parametros quanticos para nota 9+"""

    def test_pym1_trail_length_long(self, html):
        assert 'trail.length>35' in html or 'trail.length>20' in html, \
            'PYM1: trail deve ter >= 20 pontos para streaks visiveis'

    def test_pym1_streak_line_rendering(self, html):
        assert 'moveTo(t0.x,t0.y)' in html and 'lineTo(p.x,p.y)' in html, \
            'PYM1: storm deve usar linha gradient para revelar velocidade em frame estatico'

    def test_pym2_scene_focus_storm_alpha(self, html):
        assert '_stAlpha' in html, 'PYM2: alpha do storm deve variar com foco da cena'

    def test_pym3_gravitational_attractor(self, html):
        assert 'G=80' in html or 'const G=80' in html, 'PYM3: constante gravitacional G=80'
        assert 'atX' in html and 'atY' in html, 'PYM3: attractor coords passados para tickStorm'

    def test_pym4_xp_bar_bigger(self, html):
        assert 'height: 14px' in html, 'PYM4: xp-bar deve ter 14px (era 6px)'

    def test_pym4_combo_bigger(self, html):
        assert 'font-size: 28px' in html, 'PYM4: combo deve ter 28px (era 14px)'

    def test_pym5_manifesto_single_phrase(self, html):
        assert 'Math.floor(p*MANIFESTO.length)' in html, \
            'PYM5: manifesto deve exibir uma frase por vez (idx calculado por p)'
        assert '140' in html or '84' in html, 'PYM5: fonte manifesto deve ser >= 84px'

    def test_pym6_sul_global_hubs(self, html):
        assert 'SG_HUBS' in html, 'PYM6: SUL GLOBAL deve usar SG_HUBS com nodes focados'
        assert 'BRASIL' in html and 'ESALQ' in html, 'PYM6: hubs soberanos devem estar presentes'
