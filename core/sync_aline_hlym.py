import os
import json
import time
from datetime import datetime
from synaptic_strength_monitor import SynapticStrengthMonitor
from moondo_habitability_bridge import build_bridge

# 🧬 SYNC ALINE HLYM: Daily Metrics to Social Outbox
# Target: Dra. Aline Bruna da Silva (CSO Moondo)
# Channels: Instagram DM / WhatsApp

OUTBOX_PATH = "/opt/synapse_vault/obsidian_graph/social_pulse.json"
VAULT_DIR = "/opt/synapse_vault"

def get_latest_metrics():
    # 1. Atualiza força sináptica
    monitor = SynapticStrengthMonitor()
    metrics = monitor.calculate_synaptic_strength()
    
    # 2. Garante que a bridge moondo está atualizada
    try:
        build_bridge()
        with open("/opt/synapse_vault/moondo_synapse_bridge.json", 'r') as f:
            bridge = json.load(f)
            preset = bridge['bioreactor_presets'][0]
    except Exception as e:
        print(f"⚠️ Erro ao obter bridge: {e}")
        preset = {"bioreactor_temp_c": "37.0", "oxygen_saturation": "98%"}

    return metrics, preset

def generate_hlym_message(metrics, preset):
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    message = f"""
🚀 *Sincronia HLYM — Relatório Diário para Dra. Aline*
📅 Data: {timestamp}

💎 *Status do Hub:*
- Força Sináptica: {metrics['synaptic_strength']}
- Latência Neural: {metrics['neural_latency_ms']}ms
- Status: {metrics['neural_status']}

🧪 *Otimização Moondo (Preset Gaia):*
- Temp. Ideal: {preset['bioreactor_temp_c']}°C
- Sat. O2: {preset['oxygen_saturation']}
- Link de Acesso: [Pitch Diamante Confidencial]

Assinado: *Agente Antigravity* ⚛️
    """
    return message.strip()

def sync():
    print("🔄 Iniciando Sincronia HLYM para Aline...")
    metrics, preset = get_latest_metrics()
    message = generate_hlym_message(metrics, preset)
    
    # Prepara o payload para o social agent
    try:
        with open(OUTBOX_PATH, 'r') as f:
            pulse = json.load(f)
    except:
        pulse = {}

    pulse["last_sync_hlym"] = {
        "timestamp": time.time(),
        "target": "Aline Bruna da Silva",
        "channels": ["Instagram", "WhatsApp"],
        "message": message,
        "status": "PENDING_EGRESS"
    }

    with open(OUTBOX_PATH, 'w') as f:
        json.dump(pulse, f, indent=2)

    print(f"✅ Mensagem HLYM selada no outbox para Aline.")
    print(f"📝 Conteúdo:\n{message}")

if __name__ == "__main__":
    sync()
