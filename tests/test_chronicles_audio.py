"""
Test suite: Chronicles audio generator and final MP4 integrity.
Verifies narration content, audio file, and final video merge.
"""
import os
import re
import sys
import ast
import subprocess
import pytest

MEDIA_DIR = os.path.join(os.path.dirname(__file__), '..', 'media')
AUDIO_GEN  = os.path.join(MEDIA_DIR, 'gen_chronicles_audio.py')
AUDIO_FILE = os.path.join(MEDIA_DIR, 'chronicles_narration.mp3')
FINAL_MP4  = os.path.join(MEDIA_DIR, 'chronicles_final.mp4')


@pytest.fixture(scope='module')
def gen_source():
    assert os.path.exists(AUDIO_GEN), f"Not found: {AUDIO_GEN}"
    with open(AUDIO_GEN, encoding='utf-8') as f:
        return f.read()


# ── Generator file integrity ────────────────────────────────────

class TestGeneratorFile:
    def test_file_exists(self):
        assert os.path.exists(AUDIO_GEN)

    def test_valid_python_syntax(self, gen_source):
        try:
            ast.parse(gen_source)
        except SyntaxError as e:
            pytest.fail(f"SyntaxError in gen_chronicles_audio.py: {e}")

    def test_has_generate_audio_function(self, gen_source):
        assert 'def generate_audio(' in gen_source

    def test_has_merge_function(self, gen_source):
        assert 'def merge_audio_video(' in gen_source

    def test_uses_gtts(self, gen_source):
        assert 'gTTS' in gen_source

    def test_uses_ffmpeg_for_merge(self, gen_source):
        assert 'ffmpeg' in gen_source

    def test_applies_atempo_for_sync(self, gen_source):
        assert 'atempo' in gen_source

    def test_applies_audio_fade_out(self, gen_source):
        assert 'afade' in gen_source or 'fade' in gen_source.lower()

    def test_uses_shortest_flag(self, gen_source):
        assert '-shortest' in gen_source

    def test_uses_standard_sample_rate(self, gen_source):
        assert '44100' in gen_source

    def test_uses_faststart_flag(self, gen_source):
        assert 'faststart' in gen_source


# ── Narration content ───────────────────────────────────────────

class TestNarrationContent:
    def _extract_narration(self, gen_source):
        m = re.search(r'NARRATION\s*=\s*"""(.*?)"""', gen_source, re.DOTALL)
        assert m, "NARRATION constant not found"
        return m.group(1).strip()

    def test_narration_constant_exists(self, gen_source):
        assert 'NARRATION' in gen_source

    def test_narration_covers_act1_edge_computing(self, gen_source):
        narration = self._extract_narration(gen_source)
        assert 'Edge Computing' in narration or 'computações' in narration

    def test_narration_covers_act2_entropy(self, gen_source):
        narration = self._extract_narration(gen_source)
        assert 'packet loss' in narration.lower() or 'entropia' in narration.lower()

    def test_narration_covers_act2_dna(self, gen_source):
        narration = self._extract_narration(gen_source)
        assert '411' in narration

    def test_narration_covers_act3_entanglement(self, gen_source):
        narration = self._extract_narration(gen_source)
        text_lower = narration.lower()
        assert 'emaranhamento' in text_lower or 'fantasmagórica' in text_lower \
               or 'fantasmagorica' in text_lower

    def test_narration_covers_backend_reveal(self, gen_source):
        narration = self._extract_narration(gen_source)
        assert 'backend' in narration.lower() or 'código-fonte' in narration.lower()

    def test_narration_covers_finale(self, gen_source):
        narration = self._extract_narration(gen_source)
        assert 'Chronicles Framework' in narration

    def test_narration_word_count_reasonable(self, gen_source):
        narration = self._extract_narration(gen_source)
        words = len(re.findall(r'\w+', narration))
        assert 100 <= words <= 400, f"Narration word count out of range: {words}"


# ── Generated audio file ────────────────────────────────────────

class TestAudioFile:
    def test_audio_file_exists(self):
        assert os.path.exists(AUDIO_FILE), \
            "chronicles_narration.mp3 not found — run gen_chronicles_audio.py --audio-only"

    def test_audio_file_not_empty(self):
        size = os.path.getsize(AUDIO_FILE)
        assert size > 50_000, f"Audio file too small: {size} bytes"

    def test_audio_duration_reasonable(self):
        if not os.path.exists(AUDIO_FILE):
            pytest.skip("Audio file not generated")
        result = subprocess.run(
            ['ffprobe', '-v', 'quiet', '-show_entries', 'format=duration',
             '-of', 'default=noprint_wrappers=1:nokey=1', AUDIO_FILE],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            pytest.skip("ffprobe not available")
        duration = float(result.stdout.strip())
        assert 60 <= duration <= 300, f"Audio duration unexpected: {duration}s"


# ── Final merged MP4 ────────────────────────────────────────────

class TestFinalVideo:
    def test_final_mp4_exists(self):
        assert os.path.exists(FINAL_MP4), \
            "chronicles_final.mp4 not found — run gen_chronicles_audio.py"

    def test_final_mp4_not_empty(self):
        if not os.path.exists(FINAL_MP4):
            pytest.skip("Final MP4 not generated")
        size = os.path.getsize(FINAL_MP4)
        assert size > 1_000_000, f"Final MP4 too small: {size} bytes"

    def test_final_mp4_has_video_stream(self):
        if not os.path.exists(FINAL_MP4):
            pytest.skip("Final MP4 not generated")
        result = subprocess.run(
            ['ffprobe', '-v', 'quiet', '-show_entries', 'stream=codec_type',
             '-of', 'default=noprint_wrappers=1:nokey=1', FINAL_MP4],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            pytest.skip("ffprobe not available")
        assert 'video' in result.stdout

    def test_final_mp4_has_audio_stream(self):
        if not os.path.exists(FINAL_MP4):
            pytest.skip("Final MP4 not generated")
        result = subprocess.run(
            ['ffprobe', '-v', 'quiet', '-show_entries', 'stream=codec_type',
             '-of', 'default=noprint_wrappers=1:nokey=1', FINAL_MP4],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            pytest.skip("ffprobe not available")
        assert 'audio' in result.stdout

    def test_final_mp4_is_1080p(self):
        if not os.path.exists(FINAL_MP4):
            pytest.skip("Final MP4 not generated")
        result = subprocess.run(
            ['ffprobe', '-v', 'quiet', '-show_entries', 'stream=width,height',
             '-of', 'default=noprint_wrappers=1:nokey=1', FINAL_MP4],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            pytest.skip("ffprobe not available")
        assert '1920' in result.stdout
        assert '1080' in result.stdout

    def test_final_mp4_duration_matches_video(self):
        if not os.path.exists(FINAL_MP4):
            pytest.skip("Final MP4 not generated")
        result = subprocess.run(
            ['ffprobe', '-v', 'quiet', '-show_entries', 'format=duration',
             '-of', 'default=noprint_wrappers=1:nokey=1', FINAL_MP4],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            pytest.skip("ffprobe not available")
        duration = float(result.stdout.strip())
        assert 80 <= duration <= 120, f"Final duration unexpected: {duration}s"
