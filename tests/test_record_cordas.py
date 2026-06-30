"""TDD — record_cordas.py: grava chronicles_cordas.html e merge audio."""
from pathlib import Path

MEDIA  = Path(__file__).parent.parent / "media"
SCRIPT = MEDIA / "record_cordas.py"


def test_script_exists():
    assert SCRIPT.exists()


def test_targets_cordas_html():
    src = SCRIPT.read_text()
    assert "chronicles_cordas.html" in src


def test_duration_475s():
    src = SCRIPT.read_text()
    assert "475000" in src or "475" in src


def test_output_final_mp4():
    src = SCRIPT.read_text()
    assert "chronicles_cordas_final.mp4" in src


def test_uses_playwright():
    src = SCRIPT.read_text()
    assert "playwright" in src.lower()


def test_uses_ffmpeg():
    src = SCRIPT.read_text()
    assert "ffmpeg" in src


def test_audio_merge_present():
    src = SCRIPT.read_text()
    assert "cordas_narration" in src


def test_fade_out_present():
    src = SCRIPT.read_text()
    assert "afade" in src


def test_resolution_1920():
    src = SCRIPT.read_text()
    assert "1920" in src


def test_aac_codec():
    src = SCRIPT.read_text()
    assert "aac" in src


def test_webm_to_mp4_conversion():
    src = SCRIPT.read_text()
    assert "webm" in src.lower()


def test_generates_narration_if_missing():
    src = SCRIPT.read_text()
    assert "gen_cordas_narration" in src
