import time
import re
import os

LOG_FILE = "/opt/synapse_vault/logs/galactic_ingestion.log"

def monitor_exponential_growth():
    print("📈 [MONITOR DE CRESCIMENTO SOBERANO] Observando a Curva de Batista...")
    
    last_processed_line = 0
    processing_times = []
    
    try:
        while True:
            if not os.path.exists(LOG_FILE):
                print("⏳ Aguardando início do log de ingestão...")
                time.sleep(5)
                continue
                
            with open(LOG_FILE, 'r') as f:
                lines = f.readlines()
                
            new_lines = lines[last_processed_line:]
            
            for line in new_lines:
                # Exemplo de log: 🏆 [MISÃO CUMPRIDA] 50000 estrelas integradas ao Império em 18.06s.
                # Ou logs de chunks individuais
                match = re.search(r"em (\d+\.\d+)s", line)
                if match:
                    duration = float(match.group(1))
                    processing_times.append(duration)
                    
                    if len(processing_times) > 1:
                        acceleration = processing_times[-2] - processing_times[-1]
                        velocity = 10000 / duration # estrelas/seg considerando chunk de 10k
                        
                        print(f"🚀 Chunk Processado: {duration:.2f}s | Velocidade: {velocity:,.2f} st/s")
                        
                        if acceleration > 0:
                            print(f"✨ [INFLEXÃO DETECTADA] Aceleração de {acceleration:.4f}s por chunk. A Curva de Batista está EXPONENCIAL.")
                        else:
                            print("⚖️  Estado de Cruzeiro Soberano atingido.")
                            
            last_processed_line = len(lines)
            time.sleep(10)
            
    except KeyboardInterrupt:
        print("\n🛑 Monitoramento encerrado pelo Maestro.")

if __name__ == "__main__":
    monitor_exponential_growth()
