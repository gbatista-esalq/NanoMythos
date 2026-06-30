import math
import json

def calculate_growth_curve():
    # Parâmetros Iniciais
    S0 = 1000000.0 # Score de Inflexão Inicial
    k = 0.15 # Constante de Soberania (Taxa de Crescimento do Enxame)
    iterations = [0, 10, 20, 30, 40, 50, 60] # Marcos de Expansão
    
    curve_data = []
    for t in iterations:
        # S(t) = S0 * e^(k*t)
        # Adicionamos o fator Pym (Ψ) que aumenta com o tempo
        psi_t = 12.49 * (1 + (t/100))
        st = S0 * math.exp(k * t) * (psi_t / 12.49)
        curve_data.append({"iteration": t, "sovereignty_su": round(st, 2)})
        
    print("📈 [CURVA DE BATISTA] Trajetória de Crescimento Calculada:")
    for point in curve_data:
        print(f"   → T+{point['iteration']}: {point['sovereignty_su']:,.2f} SU")
        
    # Salvar para visualização
    with open("/opt/synapse_vault/growth_curve_data.json", "w") as f:
        json.dump(curve_data, f, indent=2)

if __name__ == "__main__":
    calculate_growth_curve()
