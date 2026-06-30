"""
Test suite: gemini_timeline_analyzer.py
"""
import json
import pytest
from pathlib import Path

MEDIA    = Path(__file__).parent.parent / 'media'
ANALYZER = MEDIA / 'gemini_timeline_analyzer.py'
REPORT   = MEDIA / 'gemini_timeline_report.json'


@pytest.fixture(scope='module')
def src():
    return ANALYZER.read_text(encoding='utf-8')


# ── File integrity ─────────────────────────────────────────────────

class TestFile:
    def test_exists(self):
        assert ANALYZER.exists()

    def test_not_empty(self, src):
        assert len(src) > 1000

    def test_uses_genai(self, src):
        assert 'from google import genai' in src

    def test_model(self, src):
        assert 'gemini-2.5-flash-lite' in src

    def test_no_hardcoded_key(self, src):
        assert 'AIzaSy' not in src


# ── Configuration ─────────────────────────────────────────────────

class TestConfig:
    def test_total_ms(self, src):
        assert 'TOTAL_MS' in src and '482000' in src

    def test_interval_half_sec(self, src):
        assert 'INTERVAL' in src and '0.5' in src

    def test_batch_size(self, src):
        assert 'BATCH_SIZE' in src and '3' in src

    def test_rpm_limit(self, src):
        assert 'RPM' in src and '25' in src

    def test_expected_frames(self, src):
        # 482000ms / 1000 / 0.5 = 964
        assert '964' in src or 'TIMESTAMPS' in src

    def test_html_path(self, src):
        assert 'chronicles_kurzgesagt.html' in src

    def test_report_path(self, src):
        assert 'gemini_timeline_report.json' in src


# ── Pipeline functions ─────────────────────────────────────────────

class TestFunctions:
    def test_get_api_key(self, src):
        assert 'def get_api_key' in src

    def test_vault_fallback(self, src):
        assert '/opt/synapse_vault/.env' in src

    def test_analyze_batch_sync(self, src):
        assert 'def analyze_batch_sync' in src

    def test_capture_frames(self, src):
        assert 'async def capture_frames' in src

    def test_analyze_all(self, src):
        assert 'async def analyze_all' in src

    def test_main_async(self, src):
        assert 'async def main' in src

    def test_asyncio_run(self, src):
        assert 'asyncio.run(main())' in src

    def test_grade_fn(self, src):
        assert 'def grade(' in src

    def test_bar_fn(self, src):
        assert 'def bar(' in src

    def test_heatmap_fn(self, src):
        assert 'def heatmap_row(' in src or 'heatmap' in src.lower()


# ── Batch prompt ───────────────────────────────────────────────────

class TestBatchPrompt:
    def test_prompt_template(self, src):
        assert 'PROMPT_TMPL' in src

    def test_prompt_iv_dopamina_fields(self, src):
        assert 'iv' in src and 'd=dopamina' in src

    def test_prompt_json_array(self, src):
        assert 'JSON array' in src or 'json array' in src.lower()

    def test_rate_limiting(self, src):
        assert 'CALL_DELAY' in src or 'call_delay' in src.lower()

    def test_asyncio_to_thread(self, src):
        assert 'asyncio.to_thread' in src


# ── Report (if already generated) ─────────────────────────────────

class TestReport:
    def test_report_valid_json(self):
        if not REPORT.exists():
            pytest.skip('Report not yet generated')
        data = json.loads(REPORT.read_text())
        assert 'summary' in data and 'timeline' in data

    def test_report_summary_keys(self):
        if not REPORT.exists():
            pytest.skip('Report not yet generated')
        s = json.loads(REPORT.read_text())['summary']
        for key in ('avg_dopamina', 'avg_movimento', 'overall_grade', 'total_frames'):
            assert key in s, f'Missing key: {key}'

    def test_report_timeline_length(self):
        if not REPORT.exists():
            pytest.skip('Report not yet generated')
        tl = json.loads(REPORT.read_text())['timeline']
        assert len(tl) >= 900, f'Expected ~964 frames, got {len(tl)}'

    def test_report_first_frame(self):
        if not REPORT.exists():
            pytest.skip('Report not yet generated')
        tl = json.loads(REPORT.read_text())['timeline']
        assert tl[0]['t'] == 0.0 or tl[0]['t'] == 0.5

    def test_report_no_major_errors(self):
        if not REPORT.exists():
            pytest.skip('Report not yet generated')
        s = json.loads(REPORT.read_text())['summary']
        assert s['errors'] < 50, f'Too many errors: {s["errors"]}'

    def test_report_overall_grade(self):
        if not REPORT.exists():
            pytest.skip('Report not yet generated')
        s = json.loads(REPORT.read_text())['summary']
        assert s['overall_grade'] in ('A+', 'A', 'B+', 'B', 'C', 'D')
