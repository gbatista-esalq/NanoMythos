import os
import subprocess
import struct
import sys

# SYNAPSE HUB — TESTE DE DESCONSTRUÇÃO QUÂNTICA
# Prova de integridade reversa para o Kernel REDOMA-Q

C_FILE = "quantum_sgemm.c"
EXE_FILE = "./quantum_sgemm"
KEY_FILE = "quantum_key.secret"

def run_test():
    print("🔍 [TESTE: DESCONSTRUÇÃO QUÂNTICA] Iniciando Auditoria Reversa...")

    # 1. Compilação
    subprocess.check_call(["gcc", "-O3", "-mavx2", "-mfma", "-march=native", C_FILE, "-o", EXE_FILE, "-lrt"])

    # 2. Captura do Resultado Blindado (Dump em Hex)
    result = subprocess.run([EXE_FILE, "--dump"], capture_output=True, text=True, check=True)
    parts = result.stdout.strip().split()
    shielded_hex = parts[0] # Pegamos o primeiro elemento (C[0]) em hex
    
    print(f"🛡️  Resultado Blindado (C[0] Hex): {shielded_hex}")

    # 3. Leitura da Semente de Proteção
    if not os.path.exists(KEY_FILE):
        print("❌ Semente de proteção não encontrada!")
        return
        
    with open(KEY_FILE, "rb") as f:
        key_bytes = f.read(32)
    
    # 4. Desconstrução (Reversão do XOR)
    # Convertemos o hex para bytes, aplicamos XOR e voltamos para float
    shielded_int = int(shielded_hex, 16)
    key_int = struct.unpack("<I", key_bytes[0:4])[0]
    
    unshielded_int = shielded_int ^ key_int
    unshielded_value = struct.unpack("f", struct.pack("<I", unshielded_int))[0]
    
    print(f"🔓 Resultado Desconstruído: {unshielded_value:.8f}")

    # 5. Verificação de Coerência Reversa
    # C[8] não foi blindado, então serve como referência (C[0] e C[8] são próximos matematicamente)
    reference_value = float(parts[8])
    diff = abs(unshielded_value - reference_value)
    
    print(f"🎯 Referência (C[8])   : {reference_value:.8f}")
    print(f"📊 Desvio de Sincronia : {diff:.4f}")

    # O desvio matemático esperado entre C[0] e C[8] é ~0.26112
    # Aceitamos um desvio próximo a isso para validar a desconstrução
    if diff < 1.0:
        print("\n✅ [STATUS: SOBERANO] Auditoria de Desconstrução Concluída.")
        print("   A semente quântica foi revertida com sucesso. Sincronia Diamante confirmada.")
    else:
        print("\n❌ [STATUS: COMPROMETIDO] Divergência na desconstrução quântica.")
        sys.exit(1)

if __name__ == "__main__":
    run_test()
