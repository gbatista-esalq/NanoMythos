"""
Test suite: gemini_mp4_spot_check.py
"""
import pytest
from pathlib import Path

MEDIA = Path(__file__).parent.parent / 'media'
SRC   = MEDIA / 'gemini_mp4_spot_check.py'
MP4   = MEDIA / 'chronicles_kurzgesagt_final.mp4'


@pytest.fixture(scope='module')
def src():
    return SRC.read_text(encoding='utf-8')


class TestSpotCheck:
    def test_file_exists(self):
        assert SRC.exists()

    def test_uses_gemini_flash_lite(self, src):
        assert 'gemini-2.5-flash-lite' in src

    def test_twenty_timestamps(self, src):
        assert 'N_CHECK = 20' in src

    def test_reads_key_from_vault(self, src):
        assert '/opt/synapse_vault/.env' in src

    def test_no_hardcoded_key(self, src):
        assert 'AIzaSy' not in src

    def test_five_metrics(self, src):
        for m in ('iv', 'd', 'm', 'c', 'tf'):
            assert f'avg("{m}")' in src or f"avg('{m}')" in src

    def test_grade_fn_defined(self, src):
        assert 'def grade' in src

    def test_bar_fn_defined(self, src):
        assert 'def bar' in src

    def test_ffmpeg_extract(self, src):
        assert 'ffmpeg' in src and 'extract_frame' in src

    def test_overall_computed(self, src):
        assert 'overall' in src

    def test_mp4_path_defined(self, src):
        assert 'chronicles_kurzgesagt_final.mp4' in src


class TestMP4:
    def test_mp4_exists_or_skip(self):
        if not MP4.exists():
            pytest.skip('MP4 nao gravado ainda')
        assert MP4.stat().st_size > 10_000_000, 'MP4 muito pequeno'
