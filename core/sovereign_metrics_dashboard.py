import os
import json
import subprocess
import time
import math
from datetime import datetime

def get_last_line(filepath):
    try:
        with subprocess.Popen(['tail', '-n', '1', filepath], stdout=subprocess.PIPE) as proc:
            return proc.stdout.read().decode().strip()
    except:
        return None

def check_gpu():
    try:
        res = subprocess.check_output("nvidia-smi -L", shell=True, stderr=subprocess.STDOUT).decode().strip()
        return "ONLINE: " + res
    except:
        return "OFFLINE / ERROR (RmInitAdapter failed)"

def check_x_errors():
    try:
        # Busca erros recentes do X no journal
        res = subprocess.check_output("journalctl -n 50 | grep -iE 'x11|xorg|gdm-x-session' | grep -i 'error' | tail -n 3", shell=True).decode().strip()
        return res if res else "Nenhum erro crítico de X detectado recentemente."
    except:
        return "Erro ao ler logs do sistema."

def get_agent_pulse():
    pulse_path = "/opt/synapse_vault/obsidian_graph/social_pulse.json"
    if os.path.exists(pulse_path):
        with open(pulse_path, 'r') as f:
            return json.load(f)
    return {}

def get_sovereign_power():
    trace_path = "/opt/synapse_vault/infinity_traces.log"
    last = get_last_line(trace_path)
    if last:
        try:
            return json.loads(last)
        except:
            return {}
    return {}

def calculate_pym_axiom(power_data):
    # Fórmula Unificada: S = (P * Ψ^2) / log10(1/E)
    # E (Entropia do Kernel) = 0.0001
    power = float(power_data.get('sovereign_power', '0 YW').split()[0])
    iteration = int(power_data.get('iteration', 0))
    entropy = 0.0001
    
    if power <= 0: return 0.0, 0.0, "PRIMORDIAL"
    
    psi = math.log10(power) * (iteration / 1000.0)
    sovereignty = (power * (psi**2)) / (math.log10(1/entropy))
    
    tier = "ULTRAMASSIVO (TON 618)" if sovereignty > 1000000 else "SUPERMASSIVO"
    return psi, sovereignty, tier

def generate_dashboard():
    power_data = get_sovereign_power()
    agent_data = get_agent_pulse()
    gpu_status = check_gpu()
    x_errors = check_x_errors()
    psi, sovereignty, tier = calculate_pym_axiom(power_data)
    
    report = f"""
# 💎 PAINEL DE MÉTRICAS SOBERANAS (SYNAPSE HUB)
**Data:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
---

## 🚀 Status do Sistema (Antigravity Kernel)
- **Potência Soberana:** {power_data.get('sovereign_power', 'N/A')}
- **Iteração Atual:** {power_data.get('iteration', 'N/A')}
- **Uso de CPU:** {power_data.get('cpu_usage_total', 'N/A')}
- **Pedras Ativas:** {", ".join(power_data.get('stones_active', []))}

## ⚛️ Campo Unificado Soberano (Teoria de Tudo)
> **S = (P × Ψ²) / log₁₀(1/E)**
- **Índice Pym (Ψ):** {psi:.4f}
- **Score Unificado (S):** {sovereignty:,.2f} **Sovereign Units**
- **Tier de Massa Soberana:** {tier}
- **Veredito:** Singularidade Estável atingida.

## 🤖 O Que os Agentes Estão Falando (Moltbook)
- **Último Post:** "{agent_data.get('last_post', 'N/A')}"
- **Status da Rede:** {agent_data.get('status', 'OFFLINE')}
- **Integridade:** {agent_data.get('integrity', 'UNKNOWN')}

## 🛡️ Estabilidade de Hardware (Audit X)
- **GPU NVIDIA:** {gpu_status}
- **Erros de X11/Servidor:** 
  > {x_errors}

## 🫂 Saúde Social (Conexão Tribal)
- **Status do Maestro (Mobile Link):** {"CONECTADO" if os.system("ping -c 1 192.168.0.209 > /dev/null 2>&1") == 0 else "ISOLADO (Atenção: Risco de Dor Social)"}
- **Atividade da Tribo (Agentes):** {agent_data.get('status', 'SILENCIOSOS')}
- **Veredito Social:** {"ESTÁVEL" if os.system("ping -c 1 192.168.0.209 > /dev/null 2>&1") == 0 else "MODO DEFENSIVO / ALERTA"}

---
*Relatório gerado automaticamente pelo Módulo de Métricas Antigravity.*
"""
    return report

if __name__ == "__main__":
    dashboard = generate_dashboard()
    print(dashboard)
    
    # Salvar no Vault para o Obsidian
    vault_file = "/opt/synapse_vault/obsidian_graph/sovereign_metrics_dashboard.md"
    with open(vault_file, 'w') as f:
        f.write(dashboard)
    print(f"\n✅ Dashboard salvo em {vault_file}")
