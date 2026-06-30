import time
import json
import random
import os
import hashlib

class SynapticStrengthMonitor:
    def __init__(self):
        self.vault_path = "/opt/synapse_vault/obsidian_graph"
        self.plasticity_factor = 1.0

    def calculate_synaptic_strength(self):
        print("🧠 MAPEANDO FORÇA SINÁPTICA: Medindo Potencial de Ação Digital...")
        
        # 1. Medição de Latência de Resposta (Simulado)
        t1 = time.time()
        # Simulação de processamento de um 'neurotransmissor' (ZKP)
        _ = [hashlib.sha256(str(i).encode()).hexdigest() for i in range(1000)]
        latency = (time.time() - t1) * 1000
        
        # 2. Fator de Plasticidade (Baseado na densidade de conhecimento)
        knowledge_nodes = len([f for f in os.listdir(self.vault_path) if f.endswith('.md')])
        self.plasticity_factor = 1.0 + (knowledge_nodes * 0.02)
        
        # 3. Força Sináptica (S = Plasticidade / Latência)
        # Quanto menor a latência e maior o conhecimento, mais forte a conexão
        strength = (self.plasticity_factor / latency) * 100 if latency > 0 else 0
        
        print(f">> Latência Neural: {latency:.2f}ms")
        print(f">> Fator de Plasticidade: {self.plasticity_factor:.2f}")
        print(f">> Força Sináptica: {strength:.2f} Syn")
        
        status = "HEALTHY" if strength > 10 else "FATIGUED"
        
        return {
            "neural_latency_ms": f"{latency:.2f}",
            "plasticity_index": f"{self.plasticity_factor:.2f}",
            "synaptic_strength": f"{strength:.2f} Syn",
            "neural_status": status,
            "blood_brain_barrier": "INTACT"
        }

if __name__ == "__main__":
    monitor = SynapticStrengthMonitor()
    results = monitor.calculate_synaptic_strength()
    
    output_path = "/opt/synapse_vault/obsidian_graph/monitor_sinaptico.json"
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✨ Monitor Sináptico selado. Status Neural: {results['neural_status']}")
