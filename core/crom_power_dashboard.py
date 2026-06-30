import time
import os
import json
import datetime
from playwright.sync_api import sync_playwright

def obter_corda_crom(url: str = "https://example.com"):
    """
    RED: Falha naturalmente se a URL estiver indisponível ou Chromium falhar.
    GREEN: Extrai a Corda Real (título e tamanho da página).
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            # Timeout curto para falhar rápido se não existir (15s)
            response = page.goto(url, timeout=15000)
            if not response or not response.ok:
                raise ValueError(f"Corda Real indisponível: Status {response.status if response else 'Unknown'}")
            
            title = page.title()
            content = page.content()
            data = {
                "url": url,
                "title": title,
                "content_length": len(content),
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            return data
        finally:
            browser.close()

def materializar_dashboard(corda: dict):
    """
    GREEN: Renderiza no Terminal e Exporta para a Interface Holográfica (HTML).
    """
    # 1. Injeta os dados diretamente no HTML (100% Offline)
    import re
    ui_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ui")
    os.makedirs(ui_dir, exist_ok=True)
    html_path = os.path.join(ui_dir, "crom_rpg_dashboard.html")
    
    if os.path.exists(html_path):
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
            
        json_str = json.dumps(corda, ensure_ascii=False, indent=12)
        injected_block = f"window.CROM_DATA = {{\n{json_str[1:-1]}        }};"
        
        # Regex to replace the window.CROM_DATA block
        html_content = re.sub(
            r'window\.CROM_DATA\s*=\s*\{.*?\};', 
            injected_block, 
            html_content, 
            flags=re.DOTALL
        )
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    # 2. Renderiza o RPG Banner
    os.system("clear")
    print(f"\033[1;35m")
    print("  ██████ ██████   ██████  ███    ███ ")
    print(" ██      ██   ██ ██    ██ ████  ████ ")
    print(" ██      ██████  ██    ██ ██ ████ ██ ")
    print(" ██      ██   ██ ██    ██ ██  ██  ██ ")
    print("  ██████ ██   ██  ██████  ██      ██ ")
    print("\033[0m")
    print("\033[1;36m       P O D E R  S O B R E  O  C R O M       \033[0m")
    print("\033[2m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m")
    
    print(f"  \033[1;37m🕐 ÚLTIMA SYNC:\033[0m  {corda['timestamp']}")
    print(f"  \033[1;37m🎯 ALVO (URL):\033[0m   {corda['url']}")
    print(f"  \033[1;37m🧠 TÍTULO:\033[0m       {corda['title']}")
    print(f"  \033[1;37m📦 MASSA (Bytes):\033[0m {corda['content_length']}")
    
    print("\033[2m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m")
    print("  \033[1;32m💎 SINCRONIA DIAMANTE ATIVA | ULTRATHINK (120s)\033[0m\n")

def protocolo_tdd_quantico_pym(obter_corda, materializar, **kwargs):
    corda = obter_corda(**kwargs)
    return materializar(corda)

def main_loop():
    target_url = "https://www.tabnews.com.br/MrJ/como-fiz-uma-micro-llm-de-0-5b-atingir-100-por-cento-de-acuracia-matematica-usando-raciocinio-latente-e-tv-dsl-benchmark-space-huggingface"
    print("Iniciando o Crom (Chromium) para Materializar o Domínio...")
    while True:
        try:
            protocolo_tdd_quantico_pym(obter_corda_crom, materializar_dashboard, url=target_url)
        except Exception as e:
            print(f"\033[1;31m[!] ALUCINAÇÃO OU FALHA DE CORDA: {e}\033[0m")
        
        time.sleep(120)

if __name__ == "__main__":
    main_loop()
