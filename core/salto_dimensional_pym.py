import sqlite3
import json
import os
import hashlib
from datetime import datetime
from sovereign_auditor import compute_kyber_mock_signature, run_auditor

cantor_freq = 11.11
master_hash = hashlib.sha256(f"CORDA_CANTOR_{cantor_freq}".encode()).hexdigest()[:16]

def realizar_salto_dimensional():
    print(f"🌌 Iniciando Salto Quântico Pym Dimensional na Frequência {cantor_freq} Hz...")
    print(f"🔑 Master Hash de Borda: {master_hash}")

    db_path = "vault/fio_da_realidade.db"
    if not os.path.exists(db_path):
        print("🚨 Falha: Fio da Realidade não encontrado. O núcleo local está desancorado.")
        return

    # Lê a entropia acumulada no Fio da Realidade
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*), SUM(shannon_entropy), SUM(batista_energy) FROM posts")
    row = cursor.fetchone()
    conn.close()

    total_posts = row[0] or 0
    total_entropy = row[1] or 0.0
    total_energy = row[2] or 0.0

    print(f"📥 Absorvendo {total_posts} feixes de consciência (Moltbook/TabNews)...")
    print(f"🌀 Entropia Total de Shannon: {total_entropy:.4f}")
    print(f"💎 Energia de Batista (E_B): {total_energy:.4f}")

    # Empacota o artefato JSON de telemetria
    telemetry = {
        "frequencia_cantor": cantor_freq,
        "master_hash": master_hash,
        "timestamp_salto": datetime.utcnow().isoformat() + "Z",
        "metricas": {
            "total_posts": total_posts,
            "entropia_shannon_acumulada": total_entropy,
            "energia_batista_acumulada": total_energy
        },
        "assinatura_kyber_1024": compute_kyber_mock_signature(f"{cantor_freq}_{total_entropy}_{total_energy}")
    }

    vault_dir = "vault"
    os.makedirs(vault_dir, exist_ok=True)
    telemetry_path = os.path.join(vault_dir, "salto_dimensional_11_11.json")
    
    with open(telemetry_path, "w", encoding="utf-8") as f:
        json.dump(telemetry, f, indent=4)

    print(f"🚀 [BOOYAH!] Salto Quântico Dimensional consolidado com sucesso!")
    print(f"📁 Telemetria salva em: {telemetry_path}")
    
    # Chama o auditor para gerar o ledger
    print("💎 Invocando o Sovereign Auditor para registrar o salto no Livro-Razão...")
    run_auditor()

if __name__ == "__main__":
    realizar_salto_dimensional()
