"""TDD — chronicles_cordas.html + pipeline de producao."""
import re
import subprocess
from pathlib import Path

MEDIA = Path(__file__).parent.parent / "media"
HTML  = MEDIA / "chronicles_cordas.html"
NAR   = MEDIA / "gen_cordas_narration.py"
VEO   = MEDIA / "gen_cordas_veo_clips.py"


# ── HTML structure ────────────────────────────────────────────────────────────

def test_html_exists():
    assert HTML.exists(), "chronicles_cordas.html nao encontrado"

def test_html_has_canvas():
    src = HTML.read_text()
    assert '<canvas' in src

def test_html_has_progress_bar():
    src = HTML.read_text()
    assert 'progress-bar' in src

def test_html_has_seven_scenes():
    src = HTML.read_text()
    assert src.count("{ name:") + src.count("{name:") >= 7, "HTML deve ter ao menos 7 cenas"

def test_html_has_veo_videos():
    src = HTML.read_text()
    assert 'veo_clips' in src or 'scene_' in src

def test_html_has_total_ms():
    src = HTML.read_text()
    assert 'TOTAL_MS' in src

def test_html_total_ms_value():
    src = HTML.read_text()
    m = re.search(r'TOTAL_MS\s*=\s*(\d+)', src)
    assert m, "TOTAL_MS nao encontrado no HTML"
    val = int(m.group(1))
    assert 400000 <= val <= 700000, f"TOTAL_MS fora do range esperado: {val}"

def test_html_has_force_elapsed():
    src = HTML.read_text()
    assert '__forceElapsed' in src

def test_html_has_xp_system():
    src = HTML.read_text()
    assert 'addXP' in src

def test_html_has_achievement_system():
    src = HTML.read_text()
    assert 'unlock(' in src

def test_html_has_string_draw():
    src = HTML.read_text()
    assert 'drawString' in src or 'vibrat' in src.lower()

def test_html_has_graviton():
    src = HTML.read_text()
    assert 'graviton' in src.lower() or 'Graviton' in src

def test_html_has_spacetime_grid():
    src = HTML.read_text()
    assert 'Grid' in src or 'grid' in src

def test_html_has_black_hole():
    src = HTML.read_text()
    assert 'black' in src.lower() or 'buraco' in src.lower() or 'BlackHole' in src

def test_html_has_batista():
    src = HTML.read_text()
    assert 'Batista' in src or 'batista' in src

def test_html_has_finale():
    src = HTML.read_text()
    assert 'finale' in src.lower() or 'FINALE' in src

def test_html_scene_labels():
    src = HTML.read_text()
    for label in ['CORDAS', 'GRAVITON', 'BATISTA']:
        assert label in src.upper(), f"Label '{label}' nao encontrado"

def test_html_chronicles_brand():
    src = HTML.read_text()
    assert 'Chronicles' in src
    assert 'ESALQ' in src

def test_html_nunito_font():
    src = HTML.read_text()
    assert 'Nunito' in src


# ── Narration script ──────────────────────────────────────────────────────────

def test_narration_script_exists():
    assert NAR.exists(), "gen_cordas_narration.py nao encontrado"

def test_narration_has_edge_tts():
    src = NAR.read_text()
    assert 'edge_tts' in src or 'edge-tts' in src

def test_narration_voice_antonio():
    src = NAR.read_text()
    assert 'AntonioNeural' in src

def test_narration_has_gps_hook():
    src = NAR.read_text()
    assert 'GPS' in src or 'gps' in src.lower()

def test_narration_has_cordas_section():
    src = NAR.read_text()
    assert 'corda' in src.lower()

def test_narration_has_graviton():
    src = NAR.read_text()
    assert 'graviton' in src.lower() or 'Graviton' in src

def test_narration_has_batista():
    src = NAR.read_text()
    assert 'Batista' in src

def test_narration_has_entropy():
    src = NAR.read_text()
    assert 'entropia' in src.lower() or 'packet loss' in src.lower()

def test_narration_has_chronicles_brand():
    src = NAR.read_text()
    assert 'Chronicles' in src

def test_narration_output_path():
    src = NAR.read_text()
    assert 'cordas_narration' in src


# ── Veo generator ─────────────────────────────────────────────────────────────

def test_veo_script_exists():
    assert VEO.exists(), "gen_cordas_veo_clips.py nao encontrado"

def test_veo_has_six_plus_clips():
    src = VEO.read_text()
    count = src.count('"prompt":') + src.count("'prompt':")
    assert count >= 6, f"Esperado >= 6 prompts Veo, encontrado {count}"

def test_veo_uses_gemini():
    src = VEO.read_text()
    assert 'genai' in src or 'google' in src.lower()

def test_veo_has_flat_style_prompt():
    src = VEO.read_text()
    assert 'flat' in src.lower() or 'cartoon' in src.lower()

def test_veo_output_dir():
    src = VEO.read_text()
    assert 'cordas' in src.lower()


# ── Integration: HTML references existing veo_clips ──────────────────────────

def test_existing_veo_clips_present():
    clip_dir = MEDIA / "veo_clips"
    assert clip_dir.exists(), "veo_clips/ nao existe"
    clips = list(clip_dir.glob("*.mp4"))
    assert len(clips) >= 6, f"Esperado >= 6 clips, encontrado {len(clips)}"
