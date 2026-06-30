import numpy as np
import json
import time
import os

# 🌌 AGRO-GRAVITY SIMULATION: MIP QUÂNTICO / SOBERANIA AGROFLORESTAL
# Mapeamento de Entropia e Resiliência em Sistemas Agroflorestais (SAFs)

def generate_agro_gravity_data():
    print("🌌 [SISTEMA PYM] Calculando Matriz de Gravidade Populacional...")
    
    # Configurações da "Malha" de Borda (Farm Grid)
    grid_size = 100
    num_pests = 5
    num_saf_nodes = 3
    
    # 1. Poços Gravitacionais (Pragas / Infestação)
    pests = [
        {"name": "Spodoptera frugiperda", "mass": 0.85, "x": 20, "z": 30, "type": "GRAVITY_WELL"},
        {"name": "Euschistus heros", "mass": 0.92, "x": -40, "z": 10, "type": "GRAVITY_WELL"},
        {"name": "Tuta absoluta", "mass": 0.75, "x": 10, "z": -45, "type": "GRAVITY_WELL"},
        {"name": "Hypothenemus hampei", "mass": 0.88, "x": 35, "z": -20, "type": "GRAVITY_WELL"},
        {"name": "Anticarsia gemmatalis", "mass": 0.80, "x": -25, "z": -35, "type": "GRAVITY_WELL"}
    ]
    
    # 2. Nós de Repulsão / Resiliência (SAFs / Agrofloresta)
    saf_nodes = [
        {"name": "Módulo Biodiverso Alpha", "repulsion": 0.95, "x": 0, "z": 0, "type": "REPULSION_NODE"},
        {"name": "Barreira de Semioquímicos Beta", "repulsion": 0.88, "x": 45, "z": 45, "type": "SHIELD_NODE"},
        {"name": "Corredor de Biodiversidade Gamma", "repulsion": 0.92, "x": -45, "z": -45, "type": "REPULSION_NODE"}
    ]
    
    # 3. Cálculo de Distorção do Espaço-Tempo Biológico
    gravity_map = []
    for p in pests:
        # P' = Mass * exp(-distance / shield)
        # Simulação simples de influência
        gravity_map.append({
            "id": p["name"],
            "x": p["x"],
            "z": p["z"],
            "intensity": p["mass"],
            "distortion": round(p["mass"] * 1.2, 4),
            "status": "CRITICAL" if p["mass"] > 0.8 else "STABLE"
        })
        
    # 4. Cálculo de Escudo (Soberania)
    shield_data = []
    for s in saf_nodes:
        shield_data.append({
            "id": s["name"],
            "x": s["x"],
            "z": s["z"],
            "radius": round(s["repulsion"] * 25, 2),
            "integrity": s["repulsion"]
        })

    data = {
        "metadata": {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "protocol": "MIP-QUANTUM-GRAVITY-V1",
            "maestro": "@eniripsa",
            "status": "SOBERANO"
        },
        "gravity_wells": gravity_map,
        "shield_nodes": shield_data,
        "global_entropy": 0.0042 # Sincronizado com a Redoma
    }
    
    output_path = "/home/synapseagtech/Área de Trabalho/SYNAPSE AGTECH/amazonia_legal/data/agro_gravity.json"
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"✨ [STATUS FINAL] Matriz Agro-Gravitacional exportada para {output_path}")
    return data

if __name__ == "__main__":
    generate_agro_gravity_data()
