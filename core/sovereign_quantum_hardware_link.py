from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2
from qiskit import QuantumCircuit
import hashlib
import os

# 🛡️ PROTOCOLO DE ACESSO SOBERANO (v2.1)
# Para ativar: export IBM_QUANTUM_TOKEN="seu_token" no terminal
IBM_TOKEN = os.environ.get("IBM_QUANTUM_TOKEN")

def generate_true_quantum_entropy(num_bits=64):
    print(f"🌌 [SOVEREIGN QUANTUM LINK] Conectando ao Hardware Real da IBM...")
    
    if not IBM_TOKEN:
        print("❌ ERRO: Token não encontrado no ambiente. Execute: export IBM_QUANTUM_TOKEN='seu_token'")
        return None

    try:
        # 1. Autenticação e Seleção do Backend (Hardware Real)
        service = QiskitRuntimeService(channel="ibm_quantum", token=IBM_TOKEN)
        backend = service.least_busy(operational=True, simulator=False)
        print(f"   → Backend Selecionado: {backend.name}")
        
        # 2. Construção do Circuito (Hadamard + Medição)
        qc = QuantumCircuit(1, 1)
        qc.h(0)
        qc.measure(0, 0)
        
        # 3. Execução no Hardware Real (shots = num_bits para 64 colapsos)
        print(f"   → Enviando Job para o {backend.name}... Fila Global ativada.")
        sampler = SamplerV2(backend)
        job = sampler.run([qc], shots=num_bits)
        
        print(f"   → Job ID: {job.job_id()} (Verificável no Dashboard IBM)")
        result = job.result()
        
        # 4. Extração de Bitstrings (Correção da Auditoria)
        # SamplerV2 retorna um BitArray. Acessamos a string de bits bruta.
        pub_result = result[0]
        bit_data = pub_result.data.c # Acessa o registro clássico 'c'
        
        # Convertendo o BitArray em uma string de 0s e 1s
        quantum_bits = "".join([str(bit) for bit in bit_data.get_bitstrings()])
        
        print(f"✅ Colapso de Função de Onda Real: {quantum_bits[:16]}...")
        return quantum_bits

    except Exception as e:
        print(f"❌ FALHA NA CONEXÃO QUÂNTICA: {str(e)}")
        return None

def seal_sovereign_genetic_pin_real(dna_seed):
    q_entropy = generate_true_quantum_entropy(64)
    
    if q_entropy:
        combined = dna_seed + q_entropy
        final_hash = hashlib.blake2b(combined.encode(), digest_size=8).hexdigest()
        pin = str(int(final_hash, 16))[:8]
        print(f"💎 PIN GENÉTICO (REAL QUANTUM HARDWARE): {pin}")
        return pin
    return None

if __name__ == "__main__":
    dna_sample = "ATGC_MOONDO_REAL_DNA_SEQ_001"
    seal_sovereign_genetic_pin_real(dna_sample)
