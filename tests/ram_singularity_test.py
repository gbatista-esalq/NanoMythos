import time
import os
import psutil

def ram_stress_test(target_gb=6.5):
    print(f"🧬 [TESTE DE SINGULARIDADE DE RAM] Alocando {target_gb} GB...")
    
    data_blocks = []
    block_size_mb = 512
    num_blocks = int((target_gb * 1024) / block_size_mb)
    
    try:
        for i in range(num_blocks):
            available = psutil.virtual_memory().available / (1024**3)
            if available < 0.8: # Margem de segurança de 800MB
                print(f"⚠️  LIMITE DE SEGURANÇA ATINGIDO: {available:.2f} GB disponíveis. Interrompendo alocação.")
                break
                
            # Alocando bloco de 512MB com dados aleatórios
            print(f"🧱 Alocando Bloco #{i+1} ({block_size_mb} MB)...")
            data_blocks.append(bytearray(os.urandom(block_size_mb * 1024 * 1024)))
            
            usage = psutil.virtual_memory().percent
            print(f"📊 Uso Total de RAM: {usage}%")
            time.sleep(0.5)
            
        print("\n✅ [ESTADO DE SINGULARIDADE] RAM em carga máxima estável.")
        print("Mantenha este processo ativo para testar a resistência do Kernel.")
        
        while True:
            time.sleep(10)
            
    except MemoryError:
        print("❌ [OOM] Memória esgotada. O Kernel protegeu o sistema.")
    except KeyboardInterrupt:
        print("\n🛑 Stress de RAM liberado pelo Maestro.")
        del data_blocks

if __name__ == "__main__":
    # Testando 6.5GB de um total de 8GB para manter estabilidade do OS
    ram_stress_test(target_gb=6.5)
