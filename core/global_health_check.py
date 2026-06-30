import os
import subprocess
import json
import requests
from datetime import datetime

# 🏥 GLOBAL HEALTH CHECK: SINCRONIA DIAMANTE (PARIDADE PC ANTIGO)
# Validação de integração entre Vault, Harvesters, Sync e Dashboard.

ROOT = "/home/synapseagtech/Área de Trabalho/SYNAPSE AGTECH"
VAULT = "/opt/synapse_vault"

def check_integration():
    print("🏥 [SISTEMA PYM] Iniciando Diagnóstico de Integração Global...")
    results = {}

    # 1. Verificação de Vault
    env_path = os.path.join(VAULT, ".env")
    results["vault_env"] = os.path.exists(env_path)
    
    # 2. Verificação de Processos (Sentinelas)
    processes = [
        "antigravity_daemon.sh",
        "infinity_gauntlet_sentinel.py",
        "audio_harvester.sh",
        "synapse_meeting_harvester.py",
        "sovereign_social_agent.py"
    ]
    results["processes"] = {}
    for p in processes:
        check = subprocess.run(["pgrep", "-f", p], capture_output=True)
        results["processes"][p] = "ONLINE" if check.returncode == 0 else "OFFLINE"

    # 3. Verificação de Sincronia Obsidian
    sync_index = os.path.join(VAULT, "obsidian_graph", "sync.md")
    results["obsidian_sync"] = os.path.exists(sync_index)

    # 4. Verificação de Telemetria (Localhost:8888)
    try:
        r = requests.get("http://127.0.0.1:8888/status", timeout=2)
        results["telemetry_server"] = "ACTIVE" if r.status_code == 200 else "ERROR"
    except Exception as e:
        results["telemetry_server"] = f"OFFLINE ({type(e).__name__})"

    # 5. Verificação de Dados (Novas Camadas)
    data_files = [
        "agro_gravity.json",
        "sincronia_biotica.json",
        "sovereign_loot.json"
    ]
    results["data_layers"] = {}
    for f in data_files:
        path = os.path.join(ROOT, "amazonia_legal", "data", f)
        results["data_layers"][f] = "READY" if os.path.exists(path) else "MISSING"

    print("\n📊 RELATÓRIO DE SINCRONIA:")
    print(json.dumps(results, indent=2))
    
    if all(v == "ONLINE" for v in results["processes"].values()) and results["telemetry_server"] == "ACTIVE":
        print("\n✨ [VEREDITO] SINCRONIA DIAMANTE CONFIRMADA. PARIDADE COM PC ANTIGO: 100%.")
    else:
        print("\n⚠️ [AVISO] Algumas sentinelas ainda estão em modo de aquecimento ou offline.")

if __name__ == "__main__":
    check_integration()
