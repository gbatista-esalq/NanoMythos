"""
Test suite: gemini_frame_analyzer.py
Verifica estrutura, helpers, paths e ausencia de credenciais hardcoded.
"""
import os
import json
import pytest
from pathlib import Path

MEDIA_DIR = Path(__file__).parent.parent / 'media'
ANALYZER  = MEDIA_DIR / 'gemini_frame_analyzer.py'
SNAP_DIR  = MEDIA_DIR / 'snapshots'


@pytest.fixture(scope='module')
def src():
    return ANALYZER.read_text(encoding='utf-8')


# ── File integrity ────────────────────────────────────────────────

class TestAnalyzerFile:
    def test_file_exists(self):
        assert ANALYZER.exists()

    def test_not_empty(self, src):
        assert len(src) > 800

    def test_uses_google_genai(self, src):
        assert 'from google import genai' in src or 'google.genai' in src

    def test_model_flash(self, src):
        assert 'gemini-2.5-flash-lite' in src

    def test_no_hardcoded_key(self, src):
        assert 'AIzaSy' not in src


# ── Timestamps ────────────────────────────────────────────────────

class TestTimestamps:
    EXPECTED = [5, 28, 70, 118, 145, 175, 220, 290, 340, 388, 420, 445, 470]

    def test_thirteen_timestamps(self, src):
        import ast
        tree = ast.parse(src)
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for t in node.targets:
                    if isinstance(t, ast.Name) and t.id == 'TIMESTAMPS':
                        count = len(node.value.elts)
                        assert count == 13, f'Expected 13 timestamps, got {count}'
                        return
        pytest.fail('TIMESTAMPS not found')

    @pytest.mark.parametrize('sec', EXPECTED)
    def test_timestamp_present(self, src, sec):
        assert f'({sec},' in src or f'({sec} ' in src or str(sec) in src


# ── Key retrieval ─────────────────────────────────────────────────

class TestKeyRetrieval:
    def test_get_api_key_fn(self, src):
        assert 'def get_api_key' in src

    def test_reads_env_first(self, src):
        assert 'GEMINI_API_KEY' in src and 'os.environ' in src

    def test_reads_vault_fallback(self, src):
        assert '/opt/synapse_vault/.env' in src


# ── Scoring ───────────────────────────────────────────────────────

class TestScoring:
    CRITERIA = ['impacto_visual', 'dopamina', 'movimento', 'conteudo', 'tdah_friendly']

    def test_eval_prompt_has_five_criteria(self, src):
        for c in self.CRITERIA:
            assert c in src, f'Criterion missing: {c}'

    def test_grade_fn_present(self, src):
        assert 'def grade(' in src

    def test_grade_ap_threshold(self, src):
        assert '46' in src

    def test_bar_fn_present(self, src):
        assert 'def bar(' in src

    def test_json_output_format(self, src):
        assert 'impacto_visual' in src and 'tdah_friendly' in src and "'scores'" in src

    def test_report_saved(self, src):
        assert 'gemini_frame_report.json' in src


# ── Snapshots ─────────────────────────────────────────────────────

class TestSnapshots:
    def test_snapshots_dir_exists(self):
        assert SNAP_DIR.is_dir(), f'snapshots/ not found at {SNAP_DIR}'

    def test_thirteen_snapshots_present(self):
        pngs = list(SNAP_DIR.glob('*.png'))
        assert len(pngs) == 13, f'Expected 13 PNGs, found {len(pngs)}: {[p.name for p in pngs]}'

    def test_fly_brain_snapshot(self):
        p = SNAP_DIR / 't0118_act1_fly_brain.png'
        assert p.exists()

    def test_finale_xp_snapshot(self):
        p = SNAP_DIR / 't0470_finale_xp.png'
        assert p.exists()

    def test_intro_title_snapshot(self):
        p = SNAP_DIR / 't0028_intro_title.png'
        assert p.exists()


# ── Report (if already generated) ────────────────────────────────

class TestReport:
    REPORT = MEDIA_DIR / 'gemini_frame_report.json'

    def test_report_valid_json(self):
        if not self.REPORT.exists():
            pytest.skip('Report not yet generated')
        data = json.loads(self.REPORT.read_text())
        assert 'summary' in data and 'frames' in data

    def test_report_has_all_frames(self):
        if not self.REPORT.exists():
            pytest.skip('Report not yet generated')
        data = json.loads(self.REPORT.read_text())
        assert data['summary']['frames_analyzed'] == 13

    def test_report_overall_grade(self):
        if not self.REPORT.exists():
            pytest.skip('Report not yet generated')
        data = json.loads(self.REPORT.read_text())
        assert data['summary']['overall_grade'] in ('A+', 'A', 'B+', 'B', 'C', 'D')

    def test_report_no_errors(self):
        if not self.REPORT.exists():
            pytest.skip('Report not yet generated')
        data = json.loads(self.REPORT.read_text())
        assert data['summary']['errors'] == 0
