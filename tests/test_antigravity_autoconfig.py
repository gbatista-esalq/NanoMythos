"""
TDD RED — scripts/antigravity_autoconfig.py
Auto-configuração do Antigravity em qualquer máquina.
"""
import os
import json
import tempfile
import pytest
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))


def test_reads_vault_state():
    """run_autoconfig() deve ler colony e fund do vault sem erro."""
    from antigravity_autoconfig import read_vault_state
    state = read_vault_state()
    assert isinstance(state, dict), "read_vault_state deve retornar dict"
    assert "colony_state" in state, "colony_state ausente"
    assert "sovereignty_fund_yw" in state, "sovereignty_fund_yw ausente"


def test_generates_mcp_config(tmp_path):
    """generate_mcp_config() deve criar mcp_config.json válido."""
    from antigravity_autoconfig import generate_mcp_config
    out_path = str(tmp_path / "mcp_config.json")
    generate_mcp_config(out_path=out_path)
    assert os.path.exists(out_path), "mcp_config.json não foi criado"
    with open(out_path) as f:
        data = json.load(f)
    assert isinstance(data, dict), "mcp_config.json deve ser dict"
    assert "mcpServers" in data or "tools" in data or "synapse_bridge" in data, \
        "mcp_config.json sem campos esperados"


def test_generates_antigravity_json(tmp_path):
    """update_antigravity_json() deve preservar campos existentes e adicionar novos."""
    from antigravity_autoconfig import update_antigravity_json
    base = {
        "agent_name": "Antigravity",
        "sync_chain": ["zkp_sovereign.py"],
        "last_sync": "2026-05-13"
    }
    in_path = str(tmp_path / "antigravity.json")
    with open(in_path, "w") as f:
        json.dump(base, f)
    update_antigravity_json(config_path=in_path)
    with open(in_path) as f:
        result = json.load(f)
    assert result["agent_name"] == "Antigravity", "agent_name foi perdido"
    assert "quantum_bridge" in result, "quantum_bridge não foi adicionado"
    assert "dna_gravitacional" in result, "dna_gravitacional não foi adicionado"
    assert result["dna_gravitacional"]["epsilon_head"] == 11.11


def test_writes_knowledge_entry(tmp_path):
    """write_knowledge_entry() deve criar arquivo .md na knowledge base."""
    from antigravity_autoconfig import write_knowledge_entry
    out_dir = str(tmp_path / "knowledge" / "synapse_interagent_protocol")
    write_knowledge_entry(knowledge_dir=out_dir)
    md_files = [f for f in os.listdir(out_dir) if f.endswith(".md")]
    assert len(md_files) >= 1, "Nenhum arquivo .md criado na knowledge base"
    content = open(os.path.join(out_dir, md_files[0])).read()
    assert "eniripsa" in content.lower() or "bridge" in content.lower(), \
        "Conteúdo do knowledge entry ausente"


def test_idempotent(tmp_path):
    """Executar run_autoconfig() 2x não deve corromper os arquivos."""
    from antigravity_autoconfig import update_antigravity_json
    base = {"agent_name": "Antigravity", "sync_chain": ["zkp_sovereign.py"]}
    cfg_path = str(tmp_path / "antigravity.json")
    with open(cfg_path, "w") as f:
        json.dump(base, f)
    update_antigravity_json(config_path=cfg_path)
    update_antigravity_json(config_path=cfg_path)
    with open(cfg_path) as f:
        result = json.load(f)
    assert result["agent_name"] == "Antigravity", "Idempotência falhou"
    assert isinstance(result["sync_chain"], list), "sync_chain corrompida"
