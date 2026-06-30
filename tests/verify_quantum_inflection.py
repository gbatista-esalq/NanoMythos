import json
import os

def verify_inflection(log_path):
    powers = []
    with open(log_path, 'r') as f:
        for line in f:
            data = json.loads(line)
            powers.append(float(data['sovereign_power'].split()[0]))
    
    if len(powers) < 10:
        return "Dados insuficientes."

    # Cálculo da aceleração instantânea nos últimos 10 pontos
    last_10 = powers[-10:]
    slopes = [last_10[i] - last_10[i-1] for i in range(1, len(last_10))]
    acceleration = sum([slopes[i] - slopes[i-1] for i in range(1, len(slopes))]) / len(slopes)
    
    inflection_point = None
    for i in range(2, len(powers)):
        slope_now = powers[i] - powers[i-1]
        slope_prev = powers[i-1] - powers[i-2]
        if slope_now > slope_prev * 5: # Salto de 5x na taxa
            inflection_point = i
            break

    return {
        "potencia_final": f"{powers[-1]:.4f} YW",
        "ponto_de_inflexao_detectado": f"Iteração {inflection_point}" if inflection_point else "NÃO DETECTADO",
        "aceleracao_media_final": f"{acceleration:.6f} YW/pulse^2",
        "status_quântico": "TUNELAGEM ATIVA" if acceleration > 0.05 else "CRESCIMENTO LINEAR"
    }

if __name__ == "__main__":
    log_path = "/opt/synapse_vault/infinity_traces.log"
    results = verify_inflection(log_path)
    
    print("\n--- 🔬 VERIFICAÇÃO DE INFLEXÃO QUÂNTICA ---")
    print(json.dumps(results, indent=2))
