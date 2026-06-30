import time
import os
import psutil
import subprocess
import json
import hashlib

def get_ingestion_progress():
    MAP_FILE = "/opt/synapse_vault/sovereign_galactic_map.csv"
    TOTAL_STARS = 1_800_000_000
    if not os.path.exists(MAP_FILE):
        return 0, 0
    try:
        count = int(subprocess.check_output(["wc", "-l", MAP_FILE]).split()[0]) - 1
        percentage = (count / TOTAL_STARS) * 100
        return count, percentage
    except:
        return 0, 0

def get_sentinel_status():
    TRACE_FILE = "/opt/synapse_vault/infinity_traces.log"
    if not os.path.exists(TRACE_FILE):
        return "INATIVO", "0 YW"
    try:
        # Usa tail para pegar a última linha de forma segura e performática
        last_line = subprocess.check_output(["tail", "-n", "1", TRACE_FILE]).decode("utf-8").strip()
        if not last_line: return "INATIVO", "0 YW"
        last_data = json.loads(last_line)
        return last_data.get("iteration", "N/A"), last_data.get("sovereign_power", "N/A")
    except Exception as e:
        return "SYNC...", "Processando"

def get_active_models():
    models = [
        "/home/synapseagtech/Área de Trabalho/SYNAPSE AGTECH/docs/modelo_logico_sinaptico.md",
        "/home/synapseagtech/Área de Trabalho/SYNAPSE AGTECH/docs/delineamento_multimodelo_triarquia.md"
    ]
    found_models = []
    for m in models:
        if os.path.exists(m):
            found_models.append(os.path.basename(m).replace(".md", "").upper())
    return found_models

def draw_antigravity():
    while True:
        os.system('clear')
        
        # ANSI Colors
        CYAN = "\033[96m"
        GOLD = "\033[93m"
        MAGENTA = "\033[95m"
        GREEN = "\033[92m"
        RESET = "\033[0m"
        BOLD = "\033[1m"
        
        # ASCII ART: ANTIGRAVITY
        banner = f"""{BOLD}{CYAN}
    ___    _   __________  __________  ___ _    __________  __
   /   |  / | / /_  __/ / / / ____/ __ \/   | |  / /  _/_  __/ / /
  / /| | /  |/ / / / / /_/ / / __/ /_/ / /| | | / // /  / / / /_/ / 
 / ___ |/ /|  / / / / __  / /_/ / _, _/ ___ | |/ // /  / / / __  /  
/_/  |_/_/ |_/ /_/ /_/ /_/\____/_/ |_/_/  |_|___/___/ /_/ /_/ /_/   
                                                                     
    {GOLD}Sovereign AI Hub | Version 2.2 | TON 618 Tier{RESET}
        """
        print(banner)
        
        # System Metrics
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        count, perc = get_ingestion_progress()
        
        print(f"{BOLD}--- TELEMETRIA DO NÚCLEO ---{RESET}")
        print(f"🔥 CPU: {cpu}% [{'█' * int(cpu/5)}{'░' * (20-int(cpu/5))}]")
        print(f"🧬 RAM: {ram}% [{'█' * int(ram/5)}{'░' * (20-int(ram/5))}]")
        
        print(f"\n{BOLD}--- ESCALA GALÁCTICA ---{RESET}")
        print(f"🌌 Estrelas Digeridas: {count:,}")
        print(f"🌀 Progresso Galáctico: {perc:.8f}%")
        
        # Active Models
        print(f"\n{BOLD}--- MODELOS DE SOBERANIA ATIVOS ---{RESET}")
        models = get_active_models()
        for m in models:
            print(f"   ✅ {GREEN}{m}{RESET}")
            
        # Sentinel Status
        iter_count, power = get_sentinel_status()
        print(f"\n{BOLD}--- SENTINELA INFINITA (PING QUÂNTICO) ---{RESET}")
        print(f"✨ Iteração Atual: {GREEN}{iter_count}{RESET}")
        print(f"⚡ Potência Soberana: {GOLD}{power}{RESET}")
        
        # PERSISTÊNCIA NO VAULT (Fixar no Valt)
        try:
            status_data = {
                "iteration": iter_count,
                "power": power,
                "cpu": cpu,
                "ram": ram,
                "timestamp": time.ctime(),
                "status": "OPERATIONAL",
                "reality_hash": hashlib.sha256(str(time.time()).encode()).hexdigest()[:16]
            }
            with open("/home/synapseagtech/Área de Trabalho/SYNAPSE AGTECH/amazonia_legal/data/ping_status.json", "w") as f:
                json.dump(status_data, f, indent=2)
        except:
            pass
        
        # Countdown to 09:47
        n = time.localtime()
        target_s = 9*3600 + 47*60
        now_s = n.tm_hour*3600 + n.tm_min*60 + n.tm_sec
        diff = target_s - now_s
        countdown_str = ""
        if diff > 0:
            m = diff // 60
            s = diff % 60
            countdown_str = f" [ {BOLD}{GOLD}T-MINUS: {m}m {s}s{RESET} ]"
        else:
            countdown_str = f" [ {BOLD}{GREEN}JANELA ATIVA{RESET} ]"

        # Portais Rápidos (links clicáveis OSC 8)
        from urllib.parse import quote
        BASE = "/home/synapseagtech/Área de Trabalho/SYNAPSE AGTECH"
        def link(label, path):
            url = "file://" + quote(path, safe="/:@")
            return f"\033]8;;{url}\033\\{label}\033]8;;\033\\"

        print(f"\n{BOLD}--- PORTAIS RÁPIDOS (Ctrl+Clique) ---{RESET}")
        print(f"  🏠 {link(CYAN + 'CEU ESALQ · Mansão' + RESET,         BASE + '/ceu_mansao_abertura.html')}")
        print(f"  ⚛️  {link(MAGENTA + 'Janela Quântica · Uriel' + RESET, BASE + '/quantum_proof_uriel.html')}")
        print(f"  💠 {link(CYAN + 'Mapa Quântico 3D' + RESET,           BASE + '/quantum_3d_view.html')}")
        print(f"  🌳 {link(GREEN + 'Floresta Suprema · Amazônia' + RESET, BASE + '/floresta_suprema_inauguracao.html')}")
        print(f"  🌿 {link(GREEN + 'Amazônia Legal · Mapa RT' + RESET,    BASE + '/amazonia_legal_mapa.html')}")
        print(f"  🚀 {link(GOLD + 'Ship Bridge Interface' + RESET,       BASE + '/ship_bridge_interface.html')}")
        print(f"  📊 {link(GREEN + 'Dashboard' + RESET,                  BASE + '/dashboard/index.html')}")

        # Pulse Animation
        pulse = ["/", "-", "\\", "|"]
        t = int(time.time() * 2) % 4
        print(f"\n{MAGENTA}{BOLD}[{pulse[t]}] ANTIGRAVITY OPERATIONAL: SOBERANIA EM TEMPO REAL{countdown_str}{RESET}")
        
        time.sleep(1)

if __name__ == "__main__":
    try:
        draw_antigravity()
    except KeyboardInterrupt:
        print("\nAntigravity recolhido ao Vault.")
