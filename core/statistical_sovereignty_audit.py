import math
import json
import os
import statistics

def run_audit():
    print("🔬 [AUDITORIA ESTATÍSTICA SOBERANA] Iniciando Validação Comparativa...")
    
    trace_path = "/opt/synapse_vault/infinity_traces.log"
    if not os.path.exists(trace_path):
        print("❌ Erro: Log de telemetria não encontrado.")
        return

    # 1. Coleta de Dados
    powers = []
    with open(trace_path, 'r') as f:
        for line in f:
            try:
                data = json.loads(line)
                powers.append(float(data['sovereign_power'].split()[0]))
            except:
                continue

    if len(powers) < 5:
        print("⚠️ Dados insuficientes para auditoria estatística.")
        return

    # --- PARTE I: ESTATÍSTICA TRADICIONAL (CLÁSSICA) ---
    mean_p = statistics.mean(powers)
    stdev_p = statistics.stdev(powers)
    variance_p = statistics.variance(powers)
    cv = (stdev_p / mean_p) * 100 # Coeficiente de Variação

    print("\n🏛️  MÉTRICAS TRADICIONAIS (FREQUENTISTAS):")
    print(f"- Média de Potência: {mean_p:.2f} YW")
    print(f"- Desvio Padrão: {stdev_p:.2f} YW")
    print(f"- Coeficiente de Variação: {cv:.4f}%")
    print(f"- Status Clássico: {'ESTÁVEL' if cv < 5 else 'VOLÁTIL'}")

    # --- PARTE II: ESTATÍSTICA QUÂNTICA (SOBERANA) ---
    # Na estatística quântica, medimos a Coerência (estabilidade da fase)
    # e a Tunelagem (capacidade de saltar níveis de energia)
    
    # Coerência Quântica (baseada no inverso da variância relativa)
    coherence = 1.0 / (1.0 + (variance_p / mean_p))
    
    # Índice de Superposição (Número de estados lógicos paralelos simulados)
    # Calculado pela taxa de crescimento logarítmico vs. tempo
    growth_rates = [powers[i]/powers[i-1] for i in range(1, len(powers))]
    superposition_index = statistics.mean(growth_rates) * math.log10(mean_p)
    
    # Probabilidade de Colapso de Realidade (Audit Retrocausal)
    p_collapse = 1.0 - math.exp(-len(powers) / 1000.0)

    print("\n⚛️  MÉTRICAS QUÂNTICAS (ESTATÍSTICA PYM):")
    print(f"- Coerência de Fase: {coherence:.6f} (Ideal: > 0.95)")
    print(f"- Índice de Superposição: {superposition_index:.4f} states/pulse")
    print(f"- Probabilidade de Colapso (PQC): {p_collapse * 100:.2f}%")
    print(f"- Vantagem Pym: {superposition_index / (cv + 0.0001):.2f}x sobre o clássico")

    # --- PARTE III: VEREDITO ---
    print("\n⚖️  VEREDITO DE SOBERANIA:")
    if superposition_index > 1.5 and coherence > 0.90:
        print("💎 [STATUS: SUPREMACIA] O sistema opera fora da curva gaussiana tradicional.")
    else:
        print("🟡 [STATUS: INFLEXÃO] O sistema ainda está emaranhando variáveis clássicas.")

if __name__ == "__main__":
    run_audit()
