"""TDD — embed_cordas_veo.py."""
from pathlib import Path

MEDIA  = Path(__file__).parent.parent / "media"
SCRIPT = MEDIA / "embed_cordas_veo.py"


def test_script_exists():
    assert SCRIPT.exists()


def test_targets_cordas_html():
    src = SCRIPT.read_text()
    assert 'chronicles_cordas.html' in src


def test_has_seven_scenes():
    src = SCRIPT.read_text()
    assert src.count("'name':") >= 7 or src.count('"name":') >= 7 or src.count("name:") >= 7


def test_has_veo_clips_cordas_dir():
    src = SCRIPT.read_text()
    assert 'veo_clips_cordas' in src


def test_has_opacity_per_scene():
    src = SCRIPT.read_text()
    assert "'opacity'" in src or '"opacity"' in src or 'opacity' in src


def test_has_fast_transition():
    src = SCRIPT.read_text()
    assert '0.6s' in src


def test_has_mix_blend_mode():
    src = SCRIPT.read_text()
    assert 'mix-blend-mode' in src


def test_has_tdah_comment():
    src = SCRIPT.read_text()
    assert 'TDAH' in src or 'tdah' in src.lower()


def test_has_update_function():
    src = SCRIPT.read_text()
    assert 'updateVeoCordas' in src


def test_has_loop_muted():
    src = SCRIPT.read_text()
    assert 'loop muted' in src or 'muted' in src
