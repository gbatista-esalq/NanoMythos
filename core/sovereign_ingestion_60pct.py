import time
import os
import pandas as pd
import numpy as np
from galactic_ingestion_pipeline import extract_sovereign_essence

# 🚀 MGET STAR HARVESTER v3.1 (MODO TURBO SELECIONÁVEL)
TOTAL_STARS_GOAL = 1_800_000_000
SOVEREIGN_MAP_FILE = "/opt/synapse_vault/sovereign_galactic_map.csv"

def run_throttled_ingestion(start_offset=319000, batch_size=1000, target_load=0.6):
    print(f"🌀 [MGET HARVESTER] Iniciando em {target_load*100}% de processamento...")
    print(f"📊 [META] 1.8 Bilhões de Estrelas.")
    
    current = start_offset
    start_time = time.time()
    stars_processed = 0
    
    # 90% Mode: 9s active, 1s sleep (aproximadamente)
    # Duty Cycle: Sleep = Active * (1/Target - 1)
    
    try:
        while current < TOTAL_STARS_GOAL:
            task_start = time.time()
            
            # Executa Microtarefa
            success = extract_sovereign_essence(current, limit=batch_size)
            
            task_end = time.time()
            task_duration = task_end - task_start
            
            if success:
                current += batch_size
                stars_processed += batch_size
                
                # Cálculo de Throttle (60% Ativo, 40% Sleep)
                # Active / (Active + Sleep) = 0.6 => Sleep = Active * (1/0.6 - 1)
                sleep_time = task_duration * (1.0/0.6 - 1.0)
                time.sleep(max(0, sleep_time))
                
                # Telemetria de Velocidade
                elapsed = time.time() - start_time
                speed = stars_processed / elapsed
                
                # Projeção
                remaining = TOTAL_STARS_GOAL - current
                eta_seconds = remaining / speed if speed > 0 else 0
                eta_hours = eta_seconds / 3600
                
                print(f"📈 [SPEED] {speed:.2f} stars/s | ETA: {eta_hours:.2f}h")
                
                # Log de Progresso no Vault
                with open("/opt/synapse_vault/logs/ingestion_telemetry.log", "a") as f:
                    f.write(f"{time.ctime()} | Speed: {speed:.2f} stars/s | Progress: {current}\n")
            else:
                print("⚠️ Falha na conexão. Cooldown...")
                time.sleep(10)
                
    except KeyboardInterrupt:
        print("\n🛑 [INTERRUPT] Salvando estado e ejetando.")

if __name__ == "__main__":
    # Carrega progresso atual do arquivo se existir
    if os.path.exists(SOVEREIGN_MAP_FILE):
        try:
            # Conta linhas para saber o offset atual (aproximadamente)
            with open(SOVEREIGN_MAP_FILE, 'r') as f:
                offset = sum(1 for line in f) - 1 # Subtrai header
                if offset < 0: offset = 0
        except:
            offset = 319000
    else:
        offset = 319000
        
    run_throttled_ingestion(start_offset=offset, target_load=0.4)
