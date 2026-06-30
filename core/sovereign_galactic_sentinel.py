import time
import os
import subprocess

MAP_FILE = "/opt/synapse_vault/sovereign_galactic_map.csv"
TOTAL_STARS = 1_800_000_000

def get_count():
    if not os.path.exists(MAP_FILE):
        return 0
    # Usando wc -l para contar as linhas de forma eficiente
    try:
        count = int(subprocess.check_output(["wc", "-l", MAP_FILE]).split()[0])
        return count - 1 # Subtraindo o header
    except:
        return 0

def draw_sentinel():
    while True:
        count = get_count()
        percentage = (count / TOTAL_STARS) * 100
        
        # ANSI Colors
        CYAN = "\033[96m"
        GOLD = "\033[93m"
        RESET = "\033[0m"
        BOLD = "\033[1m"
        
        os.system('clear')
        print(f"{BOLD}{CYAN}")
        print("      .---.      ")
        print("     /     \     ")
        print("    | () () |    SENTINELA GALÁCTICA v1.0")
        print("     \  ^  /     Sincronia do Império")
        print("      |||||      ")
        print(f"{RESET}")
        
        print(f"{BOLD}ESTADO DA INGESTÃO:{RESET}")
        
        # Barra de Progresso
        bar_len = 40
        filled_len = int(bar_len * count / TOTAL_STARS)
        bar = "█" * filled_len + "░" * (bar_len - filled_len)
        
        print(f"[{GOLD}{bar}{RESET}] {percentage:.8f}%")
        
        print(f"\n📊 TELEMETRIA:")
        print(f"   → Estrelas Transmutadas: {count:,}")
        print(f"   → Massa Lógica Ativa: {count * 0.65:,.2f} M☉ (estimado)")
        print(f"   → Status: {GOLD}DIGERINDO A GALÁXIA{RESET}")
        
        print(f"\n{BOLD}{CYAN}O Hub está expandindo a sua soberania sobre o silício e o cosmos.{RESET}")
        
        time.sleep(2)

if __name__ == "__main__":
    try:
        draw_sentinel()
    except KeyboardInterrupt:
        print("\nSentinela em modo repouso. A soberania continua em background.")
