import json
import os
import psutil

def get_system_mode():
    cpu_count = psutil.cpu_count()
    total_ram_gb = psutil.virtual_memory().total / (1024**3)
    
    # Lógica de Adaptação Elástica
    if cpu_count <= 2 or total_ram_gb <= 4:
        mode = "LEAN (Modo Sobrevivência)"
        config = {
            "encryption": "AES-128 (Lighter)",
            "telemetry_freq": "60s",
            "zkp_enabled": False,
            "obsidian_sync": "Manual",
            "audit_depth": "Basic"
        }
    elif cpu_count >= 8 and total_ram_gb >= 16:
        mode = "ULTRA (Modo Diamante)"
        config = {
            "encryption": "ChaCha20-Poly1305 (Post-Quantum Ready)",
            "telemetry_freq": "1s",
            "zkp_enabled": True,
            "obsidian_sync": "Real-time",
            "audit_depth": "Deep (SHA-512 + Chaining)"
        }
    else:
        mode = "BALANCED (Sincronia Padrão)"
        config = {
            "encryption": "AES-256",
            "telemetry_freq": "10s",
            "zkp_enabled": True,
            "obsidian_sync": "Auto",
            "audit_depth": "Standard"
        }
        
    return mode, config

def save_elastic_config():
    mode, config = get_system_mode()
    vault_config_path = "/opt/synapse_vault/synapse_elastic_config.json"
    
    payload = {
        "system_mode": mode,
        "hardware_specs": {
            "cpus": psutil.cpu_count(),
            "ram_gb": round(psutil.virtual_memory().total / (1024**3), 2)
        },
        "active_profiles": config
    }
    
    with open(vault_config_path, 'w') as f:
        json.dump(payload, f, indent=2)
    
    print(f"✅ Configuração Elástica gerada: {mode}")
    return payload

if __name__ == "__main__":
    save_elastic_config()
