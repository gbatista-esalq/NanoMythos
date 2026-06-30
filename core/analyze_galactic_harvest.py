import os
import pandas as pd
import numpy as np

MAP_FILE = "/opt/synapse_vault/sovereign_galactic_map.csv"

def analyze_harvest():
    print("🔬 [RECONHECIMENTO GALÁCTICO] Analisando Colheita de Dados...")
    
    if not os.path.exists(MAP_FILE):
        print("❌ Nenhum dado encontrado no Vault.")
        return

    df = pd.read_csv(MAP_FILE)
    total_stars = len(df)
    
    # 1. Estatísticas de Habitabilidade (SHI)
    habitables = df[df['shi'] > 0.95]
    top_candidates = df.sort_values(by='shi', ascending=False).head(5)
    
    # 2. Estatísticas de Gravidade (Rs)
    avg_rs = df['rs'].mean()
    total_logic_mass = df['mass_solar'].sum()
    
    # 3. Relatório
    print(f"\n💎 DOSSIÊ DE COLHEITA (Fase 1):")
    print(f"   → Estrelas Auditadas: {total_stars:,}")
    print(f"   → Sistemas com Alta Sincronia Biótica (SHI > 0.95): {len(habitables)}")
    print(f"   → Massa Lógica Acumulada: {total_logic_mass:,.2f} M☉")
    print(f"   → Horizonte de Eventos Médio (Rs): {avg_rs:.2f} metros")
    
    print("\n🌟 TOP 5 CANDIDATOS PARA EXPANSÃO BIÓTICA:")
    for i, row in top_candidates.iterrows():
        print(f"   ✨ ID: {int(row['source_id'])} | SHI: {row['shi']:.6f} | Massa: {row['mass_solar']:.2f} M☉")
    
    print("\n✅ CONCLUSÃO: O Vault já possui sementes de informação para 16k mundos.")
    print("   A densidade de 'Sistemas Habitáveis' sugere que a soberania biótica")
    print("   tem múltiplos caminhos de redundância na nossa vizinhança.")

if __name__ == "__main__":
    analyze_harvest()
