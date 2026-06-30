"""
Test suite: audit_360_hud.html — TDAH-friendly fly-brain audit dashboard.
Verifies structure, neuron checks, PYM data, and TDAH dopamine features.
"""
import os
import re
import pytest

MEDIA_DIR = os.path.join(os.path.dirname(__file__), '..', 'media')
HUD_PATH  = os.path.join(MEDIA_DIR, 'audit_360_hud.html')


@pytest.fixture(scope='module')
def hud():
    assert os.path.exists(HUD_PATH), f'Not found: {HUD_PATH}'
    with open(HUD_PATH, encoding='utf-8') as f:
        return f.read()


# ── File integrity ───────────────────────────────────────────────

class TestHUDFile:
    def test_file_exists(self):
        assert os.path.exists(HUD_PATH)

    def test_file_not_empty(self, hud):
        assert len(hud) > 3000

    def test_has_canvas(self, hud):
        assert '<canvas' in hud

    def test_has_nunito(self, hud):
        assert 'Nunito' in hud

    def test_has_progress_bar(self, hud):
        assert 'bottom-prog' in hud or 'progress' in hud.lower()


# ── TDAH / Dopamine features ─────────────────────────────────────

class TestDopamineFeatures:
    def test_xp_system(self, hud):
        assert 'xp' in hud.lower() and 'XP_MAX' in hud

    def test_achievement_system(self, hud):
        assert 'unlock(' in hud

    def test_screen_flash(self, hud):
        assert 'flash(' in hud

    def test_burst_particles(self, hud):
        assert 'burst(' in hud

    def test_glow_circles(self, hud):
        assert 'glowCircle(' in hud

    def test_has_animate_pulse(self, hud):
        assert 'pulse' in hud.lower()


# ── 12 Neurons (system checks) ───────────────────────────────────

class TestNeurons:
    REQUIRED_IDS = [
        'hw', 'vault', 'busy', 'daemon', 'ai',
        'pym', 'server', 'tunnel', 'git', 'tests',
        'synvault', 'chronic',
    ]

    def test_twelve_neurons_defined(self, hud):
        m = re.search(r'const NEURONS\s*=\s*\[(.*?)\];', hud, re.DOTALL)
        assert m, 'NEURONS array not found'
        count = m.group(1).count('id:')
        assert count == 12, f'Expected 12 neurons, got {count}'

    @pytest.mark.parametrize('nid', REQUIRED_IDS)
    def test_neuron_id_present(self, hud, nid):
        assert f"id:'{nid}'" in hud or f'id:"{nid}"' in hud, f"Neuron id '{nid}' not found"

    def test_busy_poll_lock_verified(self, hud):
        assert 'busy_poll' in hud.lower() or 'BUSY_POLL' in hud

    def test_vault_seal_verified(self, hud):
        assert 'SEALED' in hud or 'vault' in hud.lower()

    def test_pytest_check_verified(self, hud):
        assert '175 passed' in hud or 'pytest' in hud.lower()

    def test_pym_data_present(self, hud):
        assert '19245' in hud or '19.245' in hud


# ── Palette ──────────────────────────────────────────────────────

class TestPalette:
    COLORS = {'CYAN':'#00e5ff', 'GREEN':'#00ff88', 'MAGENTA':'#ff2d78',
              'YELLOW':'#ffe500', 'PURPLE':'#7000ff'}

    @pytest.mark.parametrize('name,val', COLORS.items())
    def test_palette_color_present(self, hud, name, val):
        assert val in hud.lower(), f'Missing color: {name} ({val})'

    def test_dark_background(self, hud):
        assert '#060a12' in hud or '#080c14' in hud


# ── Fly-brain concept ─────────────────────────────────────────────

class TestFlyBrain:
    def test_fly_brain_label(self, hud):
        assert 'fly-label' in hud or 'FLY-BRAIN' in hud.upper() or 'Fly-Brain' in hud

    def test_neuron_count_referenced(self, hud):
        assert '100.000' in hud or '100000' in hud

    def test_parallel_mode_mentioned(self, hud):
        assert 'paralelo' in hud.lower() or 'parallel' in hud.lower()

    def test_pym_protocol_referenced(self, hud):
        assert 'PYM' in hud


# ── Branding ─────────────────────────────────────────────────────

class TestBranding:
    def test_synapse_hub(self, hud):
        assert 'Synapse Hub' in hud or 'SYNAPSE HUB' in hud

    def test_eniripsa_identity(self, hud):
        assert 'eniripsa' in hud.lower() or '@ENIRIPSA' in hud

    def test_trava_mestra(self, hud):
        assert 'TRAVA MESTRA' in hud or 'trava' in hud.lower()

    def test_amazonia_pym_data(self, hud):
        assert 'amazonia' in hud.lower() or 'amazônia' in hud.lower() or 'amazônia' in hud

    def test_chronicles_check(self, hud):
        assert 'chronicles' in hud.lower()


# ── Audit logic ───────────────────────────────────────────────────

class TestAuditLogic:
    def test_results_array_present(self, hud):
        assert 'const RESULTS' in hud or 'RESULTS' in hud

    def test_run_next_check_fn(self, hud):
        assert 'runNextCheck' in hud or 'run_next_check' in hud

    def test_finalize_audit_fn(self, hud):
        assert 'finalizeAudit' in hud or 'finalize_audit' in hud

    def test_set_neuron_status_fn(self, hud):
        assert 'setNeuronStatus' in hud

    def test_add_log_fn(self, hud):
        assert 'addLog' in hud

    def test_health_score_tracked(self, hud):
        assert 'health' in hud.lower() and 'score' in hud.lower()

    def test_net_pulses_present(self, hud):
        assert 'netPulses' in hud or 'net_pulses' in hud

    def test_canvas_render_loop(self, hud):
        assert 'requestAnimationFrame' in hud
