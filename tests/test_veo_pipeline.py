"""
Test suite: gen_veo_clips.py + embed_veo_clips.py + chronicles HTML v2.
"""
import pytest
from pathlib import Path

MEDIA = Path(__file__).parent.parent / 'media'
GEN  = MEDIA / 'gen_veo_clips.py'
EMBD = MEDIA / 'embed_veo_clips.py'
HTML = MEDIA / 'chronicles_kurzgesagt.html'
CLIPS_DIR = MEDIA / 'veo_clips'

SCENE_FILES = [
    'scene_0_intro.mp4',
    'scene_1_act1.mp4',
    'scene_2_act2.mp4',
    'scene_3_act3.mp4',
    'scene_4_act4.mp4',
    'scene_5_finale.mp4',
]


@pytest.fixture(scope='module')
def gen_src():
    return GEN.read_text(encoding='utf-8')

@pytest.fixture(scope='module')
def embd_src():
    return EMBD.read_text(encoding='utf-8')

@pytest.fixture(scope='module')
def html_src():
    return HTML.read_text(encoding='utf-8')


# ── gen_veo_clips.py ──────────────────────────────────────────────

class TestGenVeoClips:
    def test_file_exists(self):
        assert GEN.exists()

    def test_uses_veo31(self, gen_src):
        assert 'veo-3.1-generate-preview' in gen_src

    def test_six_clips_defined(self, gen_src):
        assert gen_src.count("'file'") >= 6

    def test_no_person_generation(self, gen_src):
        assert 'dont_allow' not in gen_src

    def test_api_key_from_vault(self, gen_src):
        assert '/opt/synapse_vault/.env' in gen_src

    def test_no_hardcoded_key(self, gen_src):
        assert 'AIzaSy' not in gen_src

    def test_poll_operation_fn(self, gen_src):
        assert 'def poll_operation' in gen_src

    def test_download_uses_files_api(self, gen_src):
        assert 'client.files.download' in gen_src

    def test_file_id_extraction(self, gen_src):
        assert 'file_id' in gen_src and 'files/' in gen_src

    def test_six_scene_names(self, gen_src):
        for name in ('intro', 'act1_network', 'act2_entropy', 'act3_entanglement', 'act4_backend', 'finale'):
            assert name in gen_src, f'Scene {name} not found'


# ── embed_veo_clips.py ────────────────────────────────────────────

class TestEmbedVeoClips:
    def test_file_exists(self):
        assert EMBD.exists()

    def test_six_scene_map(self, embd_src):
        assert embd_src.count("'scene':") >= 6 or embd_src.count("'scene_") >= 6

    def test_injects_video_elements(self, embd_src):
        assert 'veo-bg' in embd_src and '<video' in embd_src

    def test_css_opacity_transition(self, embd_src):
        assert 'opacity' in embd_src and 'transition' in embd_src

    def test_update_veo_background_fn(self, embd_src):
        assert 'updateVeoBackground' in embd_src

    def test_loop_muted(self, embd_src):
        assert 'loop' in embd_src and 'muted' in embd_src

    def test_zindex_canvas_on_top(self, embd_src):
        assert 'z-index: 1' in embd_src or 'z-index:1' in embd_src


# ── chronicles_kurzgesagt.html v2 (canvas enhancements) ──────────

class TestHTMLCanvasV2:
    def test_file_exists(self):
        assert HTML.exists()

    def test_cosmic_storm(self, html_src):
        assert 'tickStorm' in html_src and 'drawStorm' in html_src

    def test_storm_count_300(self, html_src):
        assert 'length:300' in html_src

    def test_warp_rings(self, html_src):
        assert 'tickRings' in html_src and 'drawRings' in html_src

    def test_floating_symbols(self, html_src):
        assert 'tickSymbols' in html_src and 'drawSymbols' in html_src

    def test_camera_breath(self, html_src):
        assert 'camScale' in html_src

    def test_camera_scale_in_render(self, html_src):
        assert 'ctx.scale(camScale' in html_src

    def test_orbital_particles_act3(self, html_src):
        assert 'Orbital particles' in html_src or 'syncT*3.4' in html_src

    def test_wave_interference_act3(self, html_src):
        assert 'Wave interference' in html_src or 'wave=' in html_src.lower()

    def test_denser_matrix_rain_act4(self, html_src):
        assert 'Hex data streams' in html_src or 'hexChars' in html_src

    def test_galactic_rings_finale(self, html_src):
        assert 'galactic rings' in html_src.lower() or 'galColors' in html_src

    def test_intro_vortex(self, html_src):
        assert 'Rotating vortex' in html_src or 'vSpd' in html_src

    def test_ambient_240_dots(self, html_src):
        assert 'length:240' in html_src

    def test_balanced_braces(self, html_src):
        assert html_src.count('{') == html_src.count('}')

    def test_total_ms_unchanged(self, html_src):
        assert 'TOTAL_MS = 482000' in html_src

    def test_scenes_six(self, html_src):
        assert html_src.count("name:") >= 6 or html_src.count("'name'") >= 6


# ── VEO clips (skipped until generated) ──────────────────────────

class TestVeoClips:
    def test_clips_dir_exists(self):
        assert CLIPS_DIR.exists()

    @pytest.mark.parametrize('fname', SCENE_FILES)
    def test_clip_present(self, fname):
        p = CLIPS_DIR / fname
        if not p.exists():
            pytest.skip(f'{fname} not yet generated')
        assert p.stat().st_size > 1_000_000, f'{fname} too small ({p.stat().st_size} bytes)'

    def test_all_six_clips_complete(self):
        present = [CLIPS_DIR / f for f in SCENE_FILES if (CLIPS_DIR / f).exists()]
        if len(present) < 6:
            pytest.skip(f'Only {len(present)}/6 clips generated')
        assert len(present) == 6
