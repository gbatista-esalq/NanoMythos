"""TDD — gemini_cordas_framecheck.py."""
from pathlib import Path

MEDIA  = Path(__file__).parent.parent / "media"
SCRIPT = MEDIA / "gemini_cordas_framecheck.py"


def test_script_exists():
    assert SCRIPT.exists()


def test_has_force_elapsed():
    src = SCRIPT.read_text()
    assert '__forceElapsed' in src


def test_has_subprocess_isolation():
    src = SCRIPT.read_text()
    assert 'subprocess' in src
    assert 'EVAL_SCRIPT' in src


def test_has_seventeen_timestamps():
    src = SCRIPT.read_text()
    assert 'SCENE_TIMESTAMPS' in src
    import re
    m = re.search(r'SCENE_TIMESTAMPS\s*=\s*\[([^\]]+)\]', src)
    assert m, "SCENE_TIMESTAMPS nao encontrado"
    vals = [v.strip() for v in m.group(1).split(',') if v.strip()]
    assert len(vals) >= 14, f"Esperado >= 14 timestamps, encontrado {len(vals)}"


def test_has_ipv4_fix():
    src = SCRIPT.read_text()
    assert 'AF_INET' in src or '_v4_first' in src


def test_has_melhoria_field():
    src = SCRIPT.read_text()
    assert 'melhoria' in src


def test_targets_cordas_html():
    src = SCRIPT.read_text()
    assert 'chronicles_cordas.html' in src


def test_saves_report():
    src = SCRIPT.read_text()
    assert 'gemini_cordas_report.json' in src


def test_has_model_fallback():
    src = SCRIPT.read_text()
    assert 'MODELS_FALLBACK' in src
    assert 'gemini-2.5-flash' in src
