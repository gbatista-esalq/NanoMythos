import subprocess
import time
import os

def run_command(cmd):
    try:
        return subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode().strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e.output.decode().strip()}"

def _detect_blackwell_no_gsp():
    """RTX 5000 (Blackwell) com driver <595 carrega /dev/nvidia0 mas GSP firmware está ausente."""
    info_path = "/proc/driver/nvidia/gpus"
    try:
        import glob
        for info_file in glob.glob(f"{info_path}/*/information"):
            with open(info_file) as f:
                content = f.read()
            if "RTX 50" in content or "GB1" in content or "GB2" in content:
                return True
    except Exception:
        pass
    return False

def stabilize_gpu():
    print("🛡️  Iniciando Protocolo de Estabilização de GPU...")

    # 1. Verificar se o nvidia-smi responde
    if subprocess.call("command -v nvidia-smi", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
        print("ℹ️  nvidia-smi não encontrado. Ignorando estabilização de hardware (Modo Simulação).")
        return True

    check = run_command("nvidia-smi -L")
    if "Error" in check or "No devices" in check:
        if _detect_blackwell_no_gsp():
            print("❌ GPU RTX 5000 (Blackwell) detectada — driver 580 não inclui firmware GSP.")
            print("🔧 FIX: sudo apt install nvidia-driver-595 nvidia-utils-595 -y && sudo reboot")
        else:
            print("ℹ️  Hardware NVIDIA não detectado pelo driver. Pulando estabilização.")
        return True # Retorna True para não travar o daemon

    print(f"✅ GPU Detectada: {check}")

    # 2. Ativar Modo de Persistência (Impede que o driver descarregue)
    print("📡 Ativando Persistence Mode...")
    os.system("sudo nvidia-smi -pm 1")

    # 3. Configurar Gerenciamento de Energia (Evitar 'Power Spikes' instáveis)
    # 0 = Prefer Maximum Performance (Mais estável para drivers instáveis)
    print("⚡ Configurando Performance Mode (Prefer Maximum Performance)...")
    os.system("sudo nvidia-smi -p 0")

    # 4. Limitar Clock se necessário (Opcional, para evitar crash térmico)
    # print("🌡️  Limitando clocks para estabilidade térmica...")
    # os.system("sudo nvidia-smi -lgc 300,1500") # Exemplo de trava de clock

    print("💎 GPU Estabilizada. Sincro Diamante Ativa.")
    return True

if __name__ == "__main__":
    stabilize_gpu()
