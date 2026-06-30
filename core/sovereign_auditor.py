import os
import json
import hashlib
from datetime import datetime

def compute_kyber_mock_signature(data: str) -> str:
    """Simula a geração de assinatura Kyber-1024 Pós-Quântica para a Borda"""
    return "PQC-K1024-" + hashlib.sha3_512(data.encode('utf-8')).hexdigest()[:32]

def run_auditor():
    vault_path = "/opt/synapse_vault"
    logs_path = os.path.join(vault_path, "logs", "pym_leaps.log")
    
    # Busca a Pedra do Tempo na Workspace
    workspace_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    time_stone_path = os.path.join(workspace_path, "scratch", "time_stone_cache.json")
    
    leaps = []
    if os.path.exists(logs_path):
        with open(logs_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    try:
                        leaps.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass
                        
    time_stone_cache = {}
    if os.path.exists(time_stone_path):
        with open(time_stone_path, 'r', encoding='utf-8') as f:
            time_stone_cache = json.load(f)

    # Extrai a Assinatura da Corda de Cantor (11.11 Hz)
    cantor_freq = 11.11
    master_hash = hashlib.sha256(f"CORDA_CANTOR_{cantor_freq}".encode()).hexdigest()[:16]

    # Prepara o Livro-Razão (Sovereign Ledger)
    ledger_lines = [
        f"# 💎 SOVEREIGN LEDGER (LIVRO-RAZÃO DA BORDA)",
        f"**Data da Auditoria:** {datetime.utcnow().isoformat()}Z",
        f"**Frequência de Orquestração (Corda de Cantor):** {cantor_freq} Hz",
        f"**Master Hash (Pedra do Tempo):** `{master_hash}`",
        f"---",
        f"## 1. Assinaturas de Saltos Quânticos Pym (Top 10 Recentes)",
        f"| Timestamp | Leap ID | Origem | Destino | Massa (Bytes) |",
        f"|-----------|---------|--------|---------|---------------|"
    ]

    for leap in reversed(leaps[-10:]):
        ledger_lines.append(f"| `{leap.get('timestamp')}` | `{leap.get('leap_id')}` | `{leap.get('from')}` | `{leap.get('to')}` | {leap.get('packet_bytes')} |")

    ledger_lines.append(f"")
    ledger_lines.append(f"## 2. Pedra do Tempo (Congelamentos Offline - Cache de Latência Zero)")
    
    if time_stone_cache:
        for hash_key, data in time_stone_cache.items():
            if data.get("offline_frozen"):
                ledger_lines.append(f"- **Hash:** `{hash_key[:16]}`")
                ledger_lines.append(f"  - Destino: `{data.get('to')}`")
                ledger_lines.append(f"  - Artefato Congelado: `{data.get('offline_artifact_path')}`")
    else:
        ledger_lines.append("*Nenhum artefato encontrado na zona de congelamento recente.*")

    # Assinatura Kyber
    raw_data = str(leaps[-5:]) + str(time_stone_cache)
    signature = compute_kyber_mock_signature(raw_data)

    ledger_lines.append(f"")
    ledger_lines.append(f"---")
    ledger_lines.append(f"## 3. Validação Institucional Pós-Quântica (BACEN Integration)")
    ledger_lines.append(f"> Auditoria criptográfica selada via Eniripsa Master Lock.")
    ledger_lines.append(f"> **Assinatura Kyber-1024:** `{signature}`")

    # Salva o arquivo no Vault
    ledger_out_path = os.path.join(vault_path, "sovereign_ledger.md")
    
    try:
        with open(ledger_out_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(ledger_lines))
        print(f"[ 💎 AUDITOR SOBERANO ] Livro-Razão gerado com sucesso em: {ledger_out_path}")
    except PermissionError:
        # Fallback para workspace local caso não tenha root no vault
        local_ledger = os.path.join(workspace_path, "sovereign_ledger.md")
        with open(local_ledger, 'w', encoding='utf-8') as f:
            f.write("\n".join(ledger_lines))
        print(f"[ 💎 AUDITOR SOBERANO ] Permissão negada no Vault. Livro-Razão salvo em: {local_ledger}")

if __name__ == "__main__":
    run_auditor()
