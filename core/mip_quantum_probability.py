import numpy as np
import json

# 🧪 MIP QUANTUM PROBABILITY: FEROMÔNIOS BRASIL 2026
# Alinhado com a Tese Moondo x Synapse (Dra. Aline Bruna da Silva)

def calculate_pheromone_prominence():
    print("🧪 [LOGIC] Calculando Probabilidade Quântica de Sucesso (MIP)...")
    
    # Base de dados de pragas e feromônios (Brasil)
    # Estados: [Eficácia, Custo, Adaptabilidade Regional, Resiliência]
    feromonios = {
        "Spodoptera frugiperda (Lagarta-do-cartucho)": {
            "composto": "(Z)-9-tetradecenyl acetate",
            "state_vector": [0.92, 0.85, 0.98, 0.90],
            "cultura": "Milho/Soja",
            "regiao": "Nacional (Cerrado)"
        },
        "Euschistus heros (Percevejo-marrom)": {
            "composto": "Methyl 2,6,10-trimethyltridecanoate",
            "state_vector": [0.88, 0.70, 0.95, 0.85],
            "cultura": "Soja",
            "regiao": "Centro-Oeste"
        },
        "Tuta absoluta (Traça-do-tomateiro)": {
            "composto": "(E,Z,Z)-3,8,11-tetradecatrienyl acetate",
            "state_vector": [0.95, 0.60, 0.80, 0.75],
            "cultura": "Tomate",
            "regiao": "Sudeste/Nordeste"
        },
        "Hypothenemus hampei (Broca-do-café)": {
            "composto": "Kairomônio Etanol/Metanol (Sincronizado)",
            "state_vector": [0.80, 0.95, 0.90, 0.88],
            "cultura": "Café",
            "regiao": "MG/SP/ES"
        },
        "Anticarsia gemmatalis (Lagarta-da-soja)": {
            "composto": "(Z,Z,Z)-3,6,9-eicosatriene",
            "state_vector": [0.85, 0.80, 0.92, 0.80],
            "cultura": "Soja",
            "regiao": "Sul/Cerrado"
        }
    }
    
    results = []
    
    for praga, data in feromonios.items():
        v = np.array(data["state_vector"])
        # Logica Probabilística Quântica: P = Σ(v_i^2) / n
        # Pym Inflexion Correction (Ψ): P' = P * exp(1 - entropia)
        base_prob = np.mean(v**2)
        entropy = 1 - np.mean(v)
        pym_score = base_prob * np.exp(1 - entropy)
        
        results.append({
            "praga": praga,
            "composto": data["composto"],
            "cultura": data["cultura"],
            "regiao": data["regiao"],
            "probabilidade_promessa": f"{pym_score * 10:.2f}%", # Escalonado
            "score_soberano": pym_score
        })
        
    # Sort by prominence
    results.sort(key=lambda x: x["score_soberano"], reverse=True)
    
    return results

if __name__ == "__main__":
    promising_pheromones = calculate_pheromone_prominence()
    print(json.dumps(promising_pheromones, indent=2))
    
    with open("/opt/synapse_vault/logs/mip_pheromone_analysis.json", "w") as f:
        json.dump(promising_pheromones, f, indent=2)
