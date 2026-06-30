from syn_token_engine import SynTokenEngine
import os
import pandas as pd

def audit_and_mint():
    engine = SynTokenEngine()
    print("🔍 [AUDITORIA PoC] Verificando contribuições pendentes...")
    
    # 1. Milestone Galáctico (219k estrelas / 10k = 21 * 5 SYN = 105 SYN)
    MAP_FILE = "/opt/synapse_vault/sovereign_galactic_map.csv"
    if os.path.exists(MAP_FILE):
        try:
            # Contagem rápida
            with open(MAP_FILE, 'r') as f:
                lines = sum(1 for _ in f)
            stars = lines - 1
            reward = (stars // 10000) * 5
            
            # Verificar se já mintamos (simplificado: checar saldo)
            current_balance = engine.get_balance()
            if current_balance < reward:
                pending = reward - current_balance
                engine.mint_contribution("GALACTIC_MINING_MILESTONE", pending)
        except:
            pass

    # 2. Milestone de Estresse (Atingir 119 QW)
    # Vamos mintar 50 SYN pela Wave 2 de sucesso
    LOG_WAVE2 = "/opt/synapse_vault/logs/gauntlet_wave2.log"
    if os.path.exists(LOG_WAVE2):
        # Apenas um exemplo de verificação manual por agora
        engine.mint_contribution("ADAPTIVE_RESILIENCE_WAVE_2", 50)
        # Deletar ou renomear log para não mintar repetido
        os.rename(LOG_WAVE2, LOG_WAVE2 + ".processed")

    print(f"💰 Saldo Final Verificado: {engine.get_balance()} SYN")

if __name__ == "__main__":
    audit_and_mint()
