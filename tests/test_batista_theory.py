"""
Test suite: Teoria de Tudo de Batista — Kurzgesagt video production.
Covers HTML animation, audio generator, and Playwright recorder.
"""
import ast
import os
import re
import subprocess
import pytest

MEDIA_DIR = os.path.join(os.path.dirname(__file__), '..', 'media')
HTML_PATH = os.path.join(MEDIA_DIR, 'chronicles_kurzgesagt.html')
AUDIO_GEN = os.path.join(MEDIA_DIR, 'gen_batista_audio.py')
RECORDER   = os.path.join(MEDIA_DIR, 'record_kurzgesagt.py')
AUDIO_FILE = os.path.join(MEDIA_DIR, 'batista_narration.mp3')
FINAL_MP4  = os.path.join(MEDIA_DIR, 'batista_theory_final.mp4')


@pytest.fixture(scope='module')
def html():
    assert os.path.exists(HTML_PATH)
    with open(HTML_PATH, encoding='utf-8') as f:
        return f.read()


@pytest.fixture(scope='module')
def gen_src():
    assert os.path.exists(AUDIO_GEN)
    with open(AUDIO_GEN, encoding='utf-8') as f:
        return f.read()


@pytest.fixture(scope='module')
def rec_src():
    assert os.path.exists(RECORDER)
    with open(RECORDER, encoding='utf-8') as f:
        return f.read()


# ── HTML file integrity ─────────────────────────────────────────

class TestHTMLFile:
    def test_file_exists(self):
        assert os.path.exists(HTML_PATH)

    def test_file_not_empty(self, html):
        assert len(html) > 5000

    def test_canvas_element(self, html):
        assert '<canvas' in html

    def test_has_nunito_font(self, html):
        assert 'Nunito' in html

    def test_progress_bar(self, html):
        assert 'progress-bar' in html


# ── HTML palette ────────────────────────────────────────────────

class TestHTMLPalette:
    COLORS = {
        'CYAN': '#00e5ff',
        'PURPLE': '#7000ff',
        'MAGENTA': '#ff2d78',
        'YELLOW': '#ffe500',
        'GREEN': '#00ff88',
    }

    def test_all_palette_colors_defined(self, html):
        for name, val in self.COLORS.items():
            assert val in html.lower(), f"Missing color: {name} ({val})"

    def test_background_color(self, html):
        assert '#080c14' in html.lower() or '#0a0e' in html.lower()


# ── HTML scenes ─────────────────────────────────────────────────

class TestHTMLScenes:
    SCENE_FUNCTIONS = [
        'drawIntro', 'drawAct1', 'drawAct2', 'drawAct3', 'drawAct4', 'drawFinale'
    ]

    @pytest.mark.parametrize("fn", SCENE_FUNCTIONS)
    def test_scene_function_defined(self, html, fn):
        assert f'function {fn}(' in html, f"Missing: {fn}"

    def test_scenes_array_has_6_entries(self, html):
        m = re.search(r'const SCENES\s*=\s*\[(.*?)\];', html, re.DOTALL)
        assert m, "SCENES array not found"
        count = m.group(1).count('name:')
        assert count == 6, f"Expected 6 scenes, got {count}"

    def test_total_duration_7_to_9_minutes(self, html):
        m = re.search(r'TOTAL_MS\s*=\s*(\d+)', html)
        assert m, "TOTAL_MS not found"
        ms = int(m.group(1))
        assert 390000 <= ms <= 550000, f"Duration out of range: {ms}ms"

    def test_render_loop_uses_raf(self, html):
        assert 'requestAnimationFrame(render)' in html

    def test_main_loop_calls_all_scenes(self, html):
        for fn in self.SCENE_FUNCTIONS:
            assert f'{fn}(' in html


# ── HTML content (Batista branding) ────────────────────────────

class TestHTMLContent:
    def test_jung_quote_present(self, html):
        assert 'Jung' in html

    def test_batista_name(self, html):
        assert 'Batista' in html or 'BATISTA' in html

    def test_chronicles_framework(self, html):
        assert 'Chronicles Framework' in html

    def test_esalq_credential(self, html):
        assert 'ESALQ' in html

    def test_edge_computing_label(self, html):
        assert 'Edge Computing' in html or 'EDGE COMPUTING' in html

    def test_packet_loss_concept(self, html):
        assert 'packet loss' in html.lower() or 'PACKET LOSS' in html

    def test_dna_render_function(self, html):
        assert 'drawDNA(' in html

    def test_411_ratio(self, html):
        assert '411' in html

    def test_shared_memory_concept(self, html):
        assert 'MEM' in html or 'memória' in html.lower() or 'memoria' in html.lower()

    def test_backend_scene(self, html):
        assert 'BACKEND' in html or 'backend' in html

    def test_synapse_hub_credit(self, html):
        assert 'Synapse Hub' in html


# ── Audio generator ─────────────────────────────────────────────

class TestAudioGenerator:
    def test_file_exists(self):
        assert os.path.exists(AUDIO_GEN)

    def test_valid_python(self, gen_src):
        try:
            ast.parse(gen_src)
        except SyntaxError as e:
            pytest.fail(f"SyntaxError: {e}")

    def test_uses_edge_tts(self, gen_src):
        assert 'edge_tts' in gen_src

    def test_antonio_neural_voice(self, gen_src):
        assert 'AntonioNeural' in gen_src

    def test_has_generate_function(self, gen_src):
        assert 'async def generate_audio(' in gen_src

    def test_has_merge_function(self, gen_src):
        assert 'def merge_audio_video(' in gen_src

    def test_narration_constant_exists(self, gen_src):
        assert 'NARRATION' in gen_src

    def test_narration_has_jung(self, gen_src):
        assert 'Jung' in gen_src

    def test_narration_has_batista(self, gen_src):
        assert 'Batista' in gen_src or 'batista' in gen_src

    def test_narration_has_chronicles(self, gen_src):
        assert 'Chronicles Framework' in gen_src

    def test_narration_word_count(self, gen_src):
        m = re.search(r'NARRATION\s*=\s*"""(.*?)"""', gen_src, re.DOTALL)
        assert m, "NARRATION not found"
        words = len(re.findall(r'\w+', m.group(1)))
        assert 400 <= words <= 900, f"Word count out of range: {words}"

    def test_slower_rate_for_philosophical_tone(self, gen_src):
        assert 'rate=' in gen_src
        m = re.search(r'rate=["\'](-\d+%)["\']', gen_src)
        assert m, "rate not found"
        rate_pct = int(m.group(1).replace('%', ''))
        assert rate_pct <= -10, f"Rate should slow down narration: {rate_pct}%"

    def test_uses_ffmpeg_merge(self, gen_src):
        assert 'ffmpeg' in gen_src

    def test_applies_audio_fade(self, gen_src):
        assert 'afade' in gen_src

    def test_uses_standard_sample_rate(self, gen_src):
        assert '44100' in gen_src

    def test_faststart_for_compatibility(self, gen_src):
        assert 'faststart' in gen_src


# ── Playwright recorder ─────────────────────────────────────────

class TestRecorder:
    def test_file_exists(self):
        assert os.path.exists(RECORDER)

    def test_valid_python(self, rec_src):
        try:
            ast.parse(rec_src)
        except SyntaxError as e:
            pytest.fail(f"SyntaxError: {e}")

    def test_uses_playwright(self, rec_src):
        assert 'playwright' in rec_src

    def test_viewport_1920x1080(self, rec_src):
        assert '1920' in rec_src and '1080' in rec_src

    def test_duration_matches_animation(self, rec_src):
        m = re.search(r'DURATION_MS\s*=\s*(\d+)', rec_src)
        assert m, "DURATION_MS not found"
        ms = int(m.group(1))
        assert 390000 <= ms <= 550000, f"Recorder duration out of range: {ms}ms"


# ── Generated audio file ─────────────────────────────────────────

class TestGeneratedAudio:
    def test_audio_file_exists(self):
        if not os.path.exists(AUDIO_FILE):
            pytest.skip("Run gen_batista_audio.py --audio-only first")
        assert os.path.exists(AUDIO_FILE)

    def test_audio_not_empty(self):
        if not os.path.exists(AUDIO_FILE):
            pytest.skip("Audio not generated")
        assert os.path.getsize(AUDIO_FILE) > 100_000

    def test_audio_duration_5_to_8_min(self):
        if not os.path.exists(AUDIO_FILE):
            pytest.skip("Audio not generated")
        result = subprocess.run(
            ['ffprobe', '-v', 'quiet', '-show_entries', 'format=duration',
             '-of', 'default=noprint_wrappers=1:nokey=1', AUDIO_FILE],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            pytest.skip("ffprobe not available")
        dur = float(result.stdout.strip())
        assert 270 <= dur <= 500, f"Duration unexpected: {dur}s"


# ── Final merged video ───────────────────────────────────────────

class TestFinalVideo:
    def test_final_mp4_exists(self):
        if not os.path.exists(FINAL_MP4):
            pytest.skip("Run full pipeline first")

    def test_final_has_video_stream(self):
        if not os.path.exists(FINAL_MP4):
            pytest.skip("Final MP4 not generated")
        r = subprocess.run(
            ['ffprobe', '-v', 'quiet', '-show_entries', 'stream=codec_type',
             '-of', 'default=noprint_wrappers=1:nokey=1', FINAL_MP4],
            capture_output=True, text=True
        )
        assert 'video' in r.stdout

    def test_final_has_audio_stream(self):
        if not os.path.exists(FINAL_MP4):
            pytest.skip("Final MP4 not generated")
        r = subprocess.run(
            ['ffprobe', '-v', 'quiet', '-show_entries', 'stream=codec_type',
             '-of', 'default=noprint_wrappers=1:nokey=1', FINAL_MP4],
            capture_output=True, text=True
        )
        assert 'audio' in r.stdout

    def test_final_is_1080p(self):
        if not os.path.exists(FINAL_MP4):
            pytest.skip("Final MP4 not generated")
        r = subprocess.run(
            ['ffprobe', '-v', 'quiet', '-show_entries', 'stream=width,height',
             '-of', 'default=noprint_wrappers=1:nokey=1', FINAL_MP4],
            capture_output=True, text=True
        )
        assert '1920' in r.stdout and '1080' in r.stdout
