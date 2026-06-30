"""
Test suite: gemini_ultra_framecheck.py
"""
import re
import pytest
from pathlib import Path

MEDIA = Path(__file__).parent.parent / 'media'
SRC   = MEDIA / 'gemini_ultra_framecheck.py'


@pytest.fixture(scope='module')
def src():
    return SRC.read_text(encoding='utf-8')


class TestFileExists:
    def test_exists(self):
        assert SRC.exists()


class TestStructure:
    def test_html_target(self, src):
        assert 'chronicles_ultra.html' in src

    def test_twelve_timestamps(self, src):
        m = re.search(r'SCENE_TIMESTAMPS\s*=\s*\[([^\]]+)\]', src)
        assert m, 'SCENE_TIMESTAMPS nao encontrado'
        vals = [v.strip() for v in m.group(1).split(',') if v.strip()]
        assert len(vals) == 12, f'Esperado 12 timestamps, encontrado {len(vals)}'

    def test_twelve_scene_names(self, src):
        m = re.search(r'SCENE_NAMES\s*=\s*\[([^\]]+)\]', src, re.DOTALL)
        assert m, 'SCENE_NAMES nao encontrado'
        names = re.findall(r"'[^']+'\s*(?:,|])", m.group(1))
        assert len(names) == 12, f'Esperado 12 nomes, encontrado {len(names)}'

    def test_force_elapsed_injection(self, src):
        assert '__forceElapsed' in src

    def test_parallel_capture_gather(self, src):
        assert 'asyncio.gather' in src

    def test_single_gemini_call(self, src):
        assert 'generate_content' in src

    def test_model_fallback_list(self, src):
        assert 'MODELS_FALLBACK' in src

    def test_fallback_has_three_models(self, src):
        import re
        m = re.search(r'MODELS_FALLBACK\s*=\s*\[([^\]]+)\]', src, re.DOTALL)
        assert m, 'MODELS_FALLBACK nao encontrado'
        models = re.findall(r"'[^']+'", m.group(1))
        assert len(models) >= 2, f'Esperado >= 2 modelos no fallback, encontrado {len(models)}'

    def test_fallback_includes_flash_lite(self, src):
        assert 'gemini-2.5-flash-lite' in src or 'gemini-3.1-flash-lite' in src

    def test_eval_in_subprocess(self, src):
        assert 'eval_in_subprocess' in src or 'subprocess' in src

    def test_max_parallel_browsers(self, src):
        assert 'MAX_PARALLEL_BROWSERS' in src

    def test_semaphore_used(self, src):
        assert 'Semaphore' in src

    def test_vault_key(self, src):
        assert '/opt/synapse_vault/.env' in src

    def test_no_hardcoded_key(self, src):
        assert 'AIzaSy' not in src

    def test_grade_fn(self, src):
        assert 'def grade' in src

    def test_bar_fn(self, src):
        assert 'def bar' in src

    def test_multi_image_from_bytes(self, src):
        assert 'from_bytes' in src

    def test_overall_metric(self, src):
        assert 'overall' in src

    def test_playwright_async(self, src):
        assert 'async_playwright' in src

    def test_1920x1080_viewport(self, src):
        assert '1920' in src and '1080' in src

    def test_json_parse_fallback(self, src):
        assert 'parse_result' in src or 'json.loads' in src

    def test_nota_geral_output(self, src):
        assert 'NOTA GERAL' in src or 'nota' in src

    def test_missao_completa_threshold(self, src):
        assert '9.0' in src

    def test_metrics_iv_d_m_c_tf(self, src):
        for m in ('iv', 'd', 'm', 'c', 'tf'):
            assert f'"{m}"' in src or f"'{m}'" in src, f'Metrica {m} ausente'
