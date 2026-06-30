import json
import time
import random
import os

# 🐝 SINCRONIA BIÓTICA: MAPEAMENTO DE HIMENÓPTERAS (ABELHAS/FORMIGAS)
# Modelo de Inteligência Coletiva e Feromônios para a Redoma V6

def generate_bee_data():
    print("🐝 [SISTEMA PYM] Sincronizando Colmeias de Doçura e Trilhas de Feromônio Quântico...")
    
    # 1. Colmeias de Abelhas Sem Ferrão do Sul Global (Meliponini - Abelhas de Doçura)
    hives = [
        {"name": "Colmeia Central Jataí (QMP Alpha)", "x": 0, "z": 0, "health": 0.99, "type": "HIVE", "species": "Jataí Soberana", "sweetness_yw": 161.00},
        {"name": "Módulo Melipona Rufiventris (Uruçu Amarela)", "x": -30, "z": 40, "health": 0.95, "type": "HIVE", "species": "Uruçu Amarela", "sweetness_yw": 144.00},
        {"name": "Polinizadora Mandaçaia Gamma", "x": 40, "z": -25, "health": 0.92, "type": "HIVE", "species": "Mandaçaia MQA", "sweetness_yw": 128.00}
    ]
    
    # 2. Trilhas de Feromônio e Saltos Quânticos Multiversais
    trails = []
    for i in range(12):
        h = random.choice(hives)
        trails.append({
            "id": f"Quantum-Leap-Trail-{i}",
            "start": {"x": h["x"], "z": h["z"]},
            "end": {"x": random.uniform(-60, 60), "z": random.uniform(-60, 60)},
            "intensity": round(random.uniform(0.65, 0.99), 2),
            "multiversal_gateway": f"11D-Gate-{random.randint(1, 11)}",
            "coherence": round(random.uniform(0.90, 0.99), 4)
        })
        
    # 3. Enxames Ativos (Swarms) com Fator de Doçura e Polinização Ativa
    swarms = []
    for i in range(20):
        swarms.append({
            "id": f"Swarm-{i}",
            "x": random.uniform(-50, 50),
            "z": random.uniform(-50, 50),
            "count": random.randint(300, 1500),
            "activity": "POLLINATING_SWEETNESS" if random.random() > 0.3 else "QUANTUM_SCOUTING",
            "velocity_c": round(random.uniform(0.12, 0.99), 2)
        })

    data = {
        "metadata": {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "protocol": "BEE-SWEET-QUANTUM-LEAP-V2",
            "maestro": "@eniripsa",
            "sweetness_total_yw": sum(h["sweetness_yw"] for h in hives),
            "multiversal_status": "SINCRO DIAMANTE SUL GLOBAL"
        },
        "hives": hives,
        "trails": trails,
        "swarms": swarms
    }
    
    output_path = "/home/synapseagtech/Área de Trabalho/SYNAPSE AGTECH/amazonia_legal/data/sincronia_biotica.json"
    vault_path = "/opt/synapse_vault/obsidian_graph/sincronia_biotica.json"
    
    # Garantir diretórios
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    os.makedirs(os.path.dirname(vault_path), exist_ok=True)
    
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)
    with open(vault_path, "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"✨ [STATUS FINAL] Sincronia Biótica exportada para {output_path} e {vault_path}")
    return data

if __name__ == "__main__":
    generate_bee_data()
