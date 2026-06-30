"""
Test suite: record_ultra.py
"""
import pytest
from pathlib import Path

MEDIA = Path(__file__).parent.parent / 'media'
SRC   = MEDIA / 'record_ultra.py'
MP4   = MEDIA / 'chronicles_ultra_final.mp4'


@pytest.fixture(scope='module')
def src():
    return SRC.read_text(encoding='utf-8')


class TestFileExists:
    def test_exists(self):
        assert SRC.exists()


class TestStructure:
    def test_html_target(self, src):
        assert 'chronicles_ultra.html' in src

    def test_duration_120s(self, src):
        assert 'DURATION_MS' in src
        assert '120000' in src

    def test_output_mp4_name(self, src):
        assert 'chronicles_ultra_final.mp4' in src

    def test_webm_intermediate(self, src):
        assert 'ultra_raw.webm' in src

    def test_playwright_used(self, src):
        assert 'playwright' in src

    def test_ffmpeg_conversion(self, src):
        assert 'ffmpeg' in src and 'libx264' in src

    def test_1920x1080(self, src):
        assert '1920' in src and '1080' in src

    def test_no_hardcoded_key(self, src):
        assert 'AIzaSy' not in src

    def test_asyncio_run(self, src):
        assert 'asyncio.run' in src

    def test_crf_quality(self, src):
        assert 'crf' in src


class TestMP4:
    def test_mp4_exists_or_skip(self):
        if not MP4.exists():
            pytest.skip('MP4 nao gravado ainda')
        assert MP4.stat().st_size > 2_000_000, 'MP4 muito pequeno'
