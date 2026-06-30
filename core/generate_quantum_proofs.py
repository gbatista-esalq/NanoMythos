import math
import json
import os

def calculate_acertability(mass_solar, power_yw=74240):
    # Modelo: S = (P * mass^0.5) / log(1/E)
    # Acertabilidade (A) = 1 - 1/exp(S/1000)
    
    # Normalizando massa (primordiais tem massa minúscula em solar)
    m = float(mass_solar)
    if m < 1e-10: m = 1e-5 # Piso para primordiais em escala log
    
    psi = math.sqrt(m) * 12.49
    entropy = 0.0001
    
    sovereignty = (power_yw * (psi**2)) / (math.log10(1/entropy))
    
    # Prevenção de Overflow: Se S/scale > 700, exp(S/scale) estoura.
    exponent_scale = sovereignty / 1e12
    if exponent_scale > 700:
        acertability = 1.0
    else:
        acertability = 1.0 - (1.0 / math.exp(exponent_scale))
    
    return sovereignty, acertability

def generate_articles_data():
    entities = [
        {"name": "Primordiais (Micro-Vaults)", "mass": 1e-18},
        {"name": "V723 Mon (Stellar Companion)", "mass": 3.0},
        {"name": "M33 X-7 (Giant Eater)", "mass": 15.65},
        {"name": "GW190521 (Merger Shockwave)", "mass": 142.0},
        {"name": "Intermediate Gap (Invisible Nodes)", "mass": 10000.0},
        {"name": "Quasi-Star Seeds", "mass": 50000.0},
        {"name": "Sagittarius A* (Galactic Anchor)", "mass": 4000000.0},
        {"name": "M87 (Shadow Master)", "mass": 6500000000.0},
        {"name": "OJ 287 (Binary Overlord)", "mass": 18000000000.0},
        {"name": "TON 618 (Node Alpha)", "mass": 66000000000.0}
    ]
    
    final_data = {}
    for e in entities:
        s, a = calculate_acertability(e['mass'])
        final_data[e['name']] = {
            "sovereignty": f"{s:.2e}",
            "acertability": f"{a*100:.8f}%",
            "tends_to_infinity": a > 0.9999
        }
        
    with open("/opt/synapse_vault/logs/quantum_articles_proofs.json", "w") as f:
        json.dump(final_data, f, indent=2)
    
    print("✅ Provas quânticas geradas.")

if __name__ == "__main__":
    generate_articles_data()
