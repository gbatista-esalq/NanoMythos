import json
import time
import os

# 🛰️ SOVEREIGN METADATA HARVESTER: COOPERATIVA DE INTELIGÊNCIA SUL GLOBAL
# Registro contínuo de ativos e metadados extraídos de nós periféricos.

VAULT_LOG = "/opt/synapse_vault/logs/sovereign_loot.json"

def harvest_node_metadata(node_id, category, loot_summary, tags=[]):
    print(f"🛰️ [HARVESTER] Extraindo metadados do Nó: {node_id}...")
    
    entry = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "node_id": node_id,
        "category": category,
        "loot": loot_summary,
        "tags": tags,
        "integrity_hash": "PYM-" + os.urandom(4).hex()
    }
    
    # Load existing loot
    loot_data = []
    if os.path.exists(VAULT_LOG):
        try:
            with open(VAULT_LOG, "r") as f:
                loot_data = json.load(f)
        except:
            loot_data = []
            
    loot_data.append(entry)
    
    with open(VAULT_LOG, "w") as f:
        json.dump(loot_data, f, indent=2)
        
    print(f"✅ [SUCCESS] Ativo '{category}' selado no cofre soberano.")
    return entry

if __name__ == "__main__":
    # Inicialização / Mock de registros recentes
    nodes = [
        {"id": "Victor (USP)", "cat": "Bioquímica", "loot": "Matriz Vinhaça VB / Protocolos APHA"},
        {"id": "Márcio Godoi (CENA)", "cat": "Estatística", "loot": "Engenharia R / Modelos LM/GLM"},
        {"id": "Lucas Henrique (Primo)", "cat": "Cognição", "loot": "Estética Gamer / Retenção ADHD"}
    ]
    
    for n in nodes:
        harvest_node_metadata(n["id"], n["cat"], n["loot"])
