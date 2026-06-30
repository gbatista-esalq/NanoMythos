import sys
import os
import json
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open

# Adiciona o diretório raiz e scripts ao PATH do Python para importar
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import sovereign_bridge

class TestSovereignBridgeCode:
    def test_imports_sys(self):
        src_path = ROOT / "scripts" / "sovereign_bridge.py"
        src = src_path.read_text(encoding="utf-8")
        assert "import sys" in src, "import sys deve estar no topo do arquivo para evitar NameError"

    def test_extract_url_from_systemd(self):
        journal_output = (
            "May 18 10:30:00 tuf cloudflared[1234]: 2026-05-18T13:30:00Z INF +------------------------------------------------------------+\n"
            "May 18 10:30:00 tuf cloudflared[1234]: 2026-05-18T13:30:00Z INF |  Your quick Tunnel has been created! Visit it at:          |\n"
            "May 18 10:30:00 tuf cloudflared[1234]: 2026-05-18T13:30:00Z INF |  https://test-tunnel-url-extracted.trycloudflare.com       |\n"
            "May 18 10:30:00 tuf cloudflared[1234]: 2026-05-18T13:30:00Z INF +------------------------------------------------------------+\n"
        )
        
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = journal_output
        
        with patch("subprocess.run", return_value=mock_result) as mock_run:
            url = sovereign_bridge.extract_url_from_systemd()
            assert url == "https://test-tunnel-url-extracted.trycloudflare.com"
            mock_run.assert_called_once()
            args = mock_run.call_args[0][0]
            assert "journalctl" in args
            assert "synapse-cloudflared-bridge.service" in args

    def test_extract_url_from_log_file(self):
        log_content = (
            "2026-05-18T13:30:00Z INF +------------------------------------------------------------+\n"
            "2026-05-18T13:30:00Z INF |  Your quick Tunnel has been created! Visit it at:          |\n"
            "2026-05-18T13:30:00Z INF |  https://log-extracted-tunnel.trycloudflare.com            |\n"
            "2026-05-18T13:30:00Z INF +------------------------------------------------------------+\n"
        )
        
        with patch("os.path.exists", return_value=True), \
             patch("builtins.open", mock_open(read_data=log_content)):
            url = sovereign_bridge.extract_url_from_log_file()
            assert url == "https://log-extracted-tunnel.trycloudflare.com"

    def test_update_obsidian_vault_new_section(self):
        initial_obsidian_content = (
            "# 🏠 SYNAPSE HUB\n\n"
            "## 📊 STATUS DO SISTEMA\n"
            "🟢 Nó Α — ANTIGRAVITY\n"
        )
        
        mock_exists = MagicMock(return_value=True)
        mock_read = MagicMock(return_value=initial_obsidian_content)
        mock_write = MagicMock()
        
        with patch.object(Path, "exists", mock_exists), \
             patch.object(Path, "read_text", mock_read), \
             patch.object(Path, "write_text", mock_write):
            
            sovereign_bridge.update_obsidian_vault("https://new-url-test.trycloudflare.com")
            
            mock_write.assert_called_once()
            written_content = mock_write.call_args[0][0]
            assert "## 🔗 PONTE ATIVA" in written_content
            assert "https://new-url-test.trycloudflare.com" in written_content
            assert "## 📊 STATUS DO SISTEMA" in written_content

    def test_update_obsidian_vault_existing_section(self):
        existing_obsidian_content = (
            "# 🏠 SYNAPSE HUB\n\n"
            "## 🔗 PONTE ATIVA\n"
            "🔗 **URL Estelar:** [https://old-url.trycloudflare.com](https://old-url.trycloudflare.com)\n"
            "📅 *Atualizado em:* Mon May 18 10:00:00 2026\n\n"
            "## 📊 STATUS DO SISTEMA\n"
            "🟢 Nó Α — ANTIGRAVITY\n"
        )
        
        mock_exists = MagicMock(return_value=True)
        mock_read = MagicMock(return_value=existing_obsidian_content)
        mock_write = MagicMock()
        
        with patch.object(Path, "exists", mock_exists), \
             patch.object(Path, "read_text", mock_read), \
             patch.object(Path, "write_text", mock_write):
            
            sovereign_bridge.update_obsidian_vault("https://new-url-test.trycloudflare.com")
            
            mock_write.assert_called_once()
            written_content = mock_write.call_args[0][0]
            assert "## 🔗 PONTE ATIVA" in written_content
            assert "https://new-url-test.trycloudflare.com" in written_content
            assert "https://old-url.trycloudflare.com" not in written_content
            assert "## 📊 STATUS DO SISTEMA" in written_content
