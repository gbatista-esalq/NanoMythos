#!/usr/bin/env python3
import os
import json
import time
import shutil
from datetime import datetime

VAULT_PATH = "/opt/synapse_vault"
GHOST_MIRROR = "/opt/synapse_vault/ghost_kernel_mirror.json"
BACKUP_PATH = "/home/synapseagtech/Área de Trabalho/SYNAPSE AGTECH/backups/ghost_state.json"

def harvest_state():
    state = {
        "timestamp": datetime.now().isoformat(),
        "node": "SYNAPSE-HUB-LINUX",
        "status": "DIAMANTE",
        "active_keys": [],
        "telemetry_summary": {}
    }
    
    # Harvest keys (names only, for safety)
    env_file = os.path.join(VAULT_PATH, ".env")
    if os.path.exists(env_file):
        with open(env_file, "r") as f:
            for line in f:
                if "=" in line:
                    state["active_keys"].append(line.split("=")[0])
                    
    # Harvest last logs
    log_file = os.path.join(VAULT_PATH, "logs/sessions.log")
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            state["last_log"] = f.readlines()[-1].strip()
            
    return state

def get_temperature():
    """Lê a temperatura da CPU."""
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            return int(f.read().strip()) / 1000
    except:
        return 0

def save_ghost(state):
    try:
        temp = get_temperature()
        state["cpu_temp"] = temp
        
        # --- AMORTECEDOR DE ENTROPIA (PROTOCOLO FANTASMA) ---
        if temp > 85.0:
            state["status"] = "GHOST_MODE"
            state["warning"] = "CRITICAL_TEMP_DETECTED - SUSPENDING VISUALS"
            # No modo fantasma, paramos de processar telemetria visual pesada
            # e apenas escrevemos o estado crítico.
            log_path = os.path.join(VAULT_PATH, "logs/ghost_critical.log")
            with open(log_path, "a") as f:
                f.write(f"[{datetime.now()}] EMERGENCY: Temp {temp}C. Entropy Damper Active.\n")
        
        with open(GHOST_MIRROR, "w") as f:
            json.dump(state, f, indent=2)
        shutil.copy2(GHOST_MIRROR, BACKUP_PATH)
        print(f"[{datetime.now()}] Ghost Kernel: Sincronia Diamante ({state['status']}) espelhada.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    while True:
        state = harvest_state()
        save_ghost(state)
        time.sleep(60) # Sync every minute
