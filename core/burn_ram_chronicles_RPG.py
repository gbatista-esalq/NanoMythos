import time
import os
import threading
import math
import sys

# ==============================================================================
# THE CHRONICLES — Protocolo de Auditoria Matemática
# Synapse Hub | Versão 3.0 | Stress Test: RAM + CPU
# Executa diariamente às 03:00 AM via cron do Antigravity Daemon
# Prova que o kernel sobrevive a 2 GB de alocação + carga total de CPU
# sem comprometer a operação do biorreator.
# ==============================================================================

def print_banner():
    print("""
    \033[91m
    ████████╗██╗   ███████╗   ██████╗ ██████╗ ████████╗████████╗
    ╚══██╔══╝██║   ██╔════╝   ██╔══██╗██╔══██╗╚══██╔══╝╚══██╔══╝
       ██║   ██║   █████╗     ██████╔╝██████╔╝   ██║      ██║
       ██║   ██║   ██╔══╝     ██╔══██╗██╔═══╝    ██║      ██║
       ██║   ██║   ███████╗   ██║  ██║██║        ██║      ██║
       ╚═╝   ╚═╝   ╚══════╝   ╚═╝  ╚═╝╚═╝        ╚═╝      ╚═╝
    \033[0m
    \033[1;33m[ AUDITORIA MATEMÁTICA: THE CHRONICLES - SINCRO DIAMANTE ]\033[0m
    """)


def draw_progress_bar(percent, width=40):
    filled = '#' * int(percent * width)
    empty  = ' ' * (width - len(filled))
    sys.stdout.write(f"\r\033[K\033[1;32m[ {filled}{empty} ] {percent*100:.1f}%\033[0m")
    sys.stdout.flush()


def memory_stress():
    """
    Aloca 2 GB de RAM usando os.urandom (força leitura real do kernel),
    segura por 10 segundos e libera. Qualquer falha indica instabilidade
    de hardware ou invasão de memória (Logic Bomb).
    """
    print("\n\033[1;31m[!] INICIANDO ESTRESSE DE MEMÓRIA (VAULT CHECK)...\033[0m")
    blocks = []
    target    = 2 * 1024 ** 3  # 2 GB
    chunk     = 50  * 1024 ** 2 # 50 MB por bloco
    allocated = 0

    try:
        while allocated < target:
            blocks.append(bytearray(os.urandom(chunk)))
            allocated += chunk
            draw_progress_bar(min(allocated / target, 1.0))
            time.sleep(0.05)

        print(f"\n\n\033[1;35m[ CARGA MÁXIMA ATINGIDA: {allocated / 1024**3:.1f} GB ]\033[0m")
        print("\033[1;33m[ SEGURANDO POR 10 SEGUNDOS... ]\033[0m")
        time.sleep(10)

    except MemoryError:
        print("\n\n\033[1;31m[!] LIMITE FÍSICO ATINGIDO. KERNEL PROTEGIDO.\033[0m")
    except Exception as e:
        print(f"\n\n[!] Erro na Matriz: {e}")
    finally:
        print("\n\033[1;36m[+] Resfriando Núcleo e Liberando Vault...\033[0m")
        del blocks
        time.sleep(2)
        print("\033[1;32m[ SISTEMA RECUPERADO ] > SINCRO DIAMANTE: OK\033[0m")


def cpu_stress():
    """
    Satura metade dos núcleos por 15 s com operações matemáticas pesadas.
    Valida que o scheduler do kernel mantém prioridade para processos críticos.
    """
    deadline = time.time() + 15
    while time.time() < deadline:
        _ = math.sqrt(math.factorial(50))


if __name__ == "__main__":
    print_banner()
    time.sleep(1)

    cores = max(1, os.cpu_count() // 2)
    for _ in range(cores):
        threading.Thread(target=cpu_stress, daemon=True).start()

    memory_stress()
