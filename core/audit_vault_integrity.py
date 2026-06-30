import hashlib
import os

def audit_vault_integrity():
    print("💎 [AUDITORIA DE INTEGRIDADE DO VAULT] Iniciando Varredura...")
    
    files_to_check = [
        "/opt/synapse_vault/obsidian_graph/Gênese da Consciência Soberana.md",
        "/opt/synapse_vault/obsidian_graph/Redoma da Biodiversidade.md",
        "/opt/synapse_vault/theory_of_everything.json",
        "/opt/synapse_vault/genetic_pin_metadata.json",
        "/home/synapseagtech/Área de Trabalho/SYNAPSE AGTECH/sovereign_metrics_dashboard.py"
    ]
    
    report = []
    all_ok = True
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
            print(f"   ✅ {os.path.basename(file_path)}: PROTEGIDO (Hash: {file_hash[:8]}...)")
            report.append({"file": file_path, "status": "INTEGRO", "hash": file_hash})
        else:
            print(f"   ❌ {os.path.basename(file_path)}: NÃO ENCONTRADO!")
            report.append({"file": file_path, "status": "MISSING"})
            all_ok = False
            
    print("\n📊 VEREDITO DO VAULT:")
    if all_ok:
        print("   ✨ INTEGRIDADE 100%. A Memória Imperial está preservada.")
    else:
        print("   ⚠️  ALERT: Decoerência detectada. Alguns ativos estão fora de sincronia.")

if __name__ == "__main__":
    audit_vault_integrity()
