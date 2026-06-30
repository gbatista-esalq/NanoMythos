"""
Test suite: destranca_tudo.py
"""
import pytest
from pathlib import Path

ROOT = Path(__file__).parent.parent
SRC  = ROOT / 'destranca_tudo.py'


@pytest.fixture(scope='module')
def src():
    return SRC.read_text(encoding='utf-8')


class TestFileExists:
    def test_file_exists(self):
        assert SRC.exists()


class TestNoBadPatterns:
    def test_no_os_system(self, src):
        assert 'os.system(' not in src, 'usar subprocess.run, nao os.system'

    def test_no_defunct_kill(self, src):
        assert "pkill -f 'defunct'" not in src, 'zombies nao recebem sinais'

    def test_no_sovereign_metrics_call(self, src):
        assert 'sovereign_metrics_dashboard' not in src, 'arquivo deletado'

    def test_no_pkill(self, src):
        assert 'pkill' not in src, 'pkill nao resolve zombies'

    def test_subprocess_imported(self, src):
        assert 'import subprocess' in src

    def test_no_devnull_suppress(self, src):
        assert '> /dev/null 2>&1' not in src, 'erros nao devem ser suprimidos'

    def test_no_sudo_restart_ssh(self, src):
        assert 'sudo systemctl restart ssh' not in src


class TestFunctions:
    def test_check_busy_poll_defined(self, src):
        assert 'def check_busy_poll(' in src

    def test_detect_zombies_defined(self, src):
        assert 'def detect_zombies(' in src

    def test_check_mobile_defined(self, src):
        assert 'def check_mobile(' in src

    def test_check_api_keys_defined(self, src):
        assert 'def check_api_keys(' in src

    def test_sync_git_defined(self, src):
        assert 'def sync_git(' in src

    def test_pipeline_defined(self, src):
        assert 'def destranca_pipeline(' in src


class TestTravaDiamante:
    def test_busy_poll_sysctl_check(self, src):
        assert 'net.core.busy_poll' in src

    def test_sys_exit_on_violation(self, src):
        assert 'sys.exit(1)' in src, 'deve abortar se busy_poll > 0'

    def test_busy_poll_zero_comparison(self, src):
        assert "'0'" in src or '"0"' in src


class TestZombieDetect:
    def test_ps_command_used(self, src):
        assert "'ps'" in src or '"ps"' in src

    def test_zombie_state_z(self, src):
        assert "'Z'" in src or '"Z"' in src

    def test_returns_list(self, src):
        assert 'zombies' in src and 'return zombies' in src


class TestApiKeys:
    def test_vault_path(self, src):
        assert '/opt/synapse_vault/.env' in src

    def test_env_var_check(self, src):
        assert 'GEMINI_API_KEY' in src

    def test_no_hardcoded_key(self, src):
        assert 'AIzaSy' not in src


class TestGitSync:
    def test_git_fetch_origin_main(self, src):
        assert 'fetch' in src and 'origin' in src and 'main' in src

    def test_captures_stderr(self, src):
        assert 'stderr' in src


class TestSafety:
    def test_returns_dict(self, src):
        assert 'results' in src and 'return results' in src

    def test_main_guard(self, src):
        assert "__name__ == '__main__'" in src or '__name__ == "__main__"' in src


class TestPymClock:
    def test_guidance_defined(self, src):
        assert 'def get_pym_temporal_guidance(' in src

    def test_update_app_tarefas_defined(self, src):
        assert 'def update_app_tarefas(' in src

    def test_guidance_logic(self):
        import sys
        sys.path.insert(0, str(ROOT))
        from destranca_tudo import get_pym_temporal_guidance
        mock_results = {
            'busy_poll': True,
            'zombies_clean': True,
            'mobile': True,
            'api_keys': True,
            'git': True
        }
        res = get_pym_temporal_guidance(mock_results)
        assert isinstance(res, dict)
        assert 'phase' in res
        assert 'focus' in res
        assert 'quest' in res
        assert 'xp' in res
        assert 'status_caminhos' in res
        assert res['status_caminhos'] == "CAMINHOS ABERTOS"
        assert not res['blocked_paths']

