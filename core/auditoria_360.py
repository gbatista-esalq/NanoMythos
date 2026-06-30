from playwright.sync_api import sync_playwright
import time
import os

# Cria pasta para os frames de auditoria
os.makedirs("audit_frames", exist_ok=True)

# Defina a sua URL de teste (Pode ser o localhost ou o Cloudflare Tunnel)
URL_ALVO = "http://localhost:8888/ui/reino_quantico_amazonia.html?token=DALILA_USP_01"

def iniciar_auditoria_360():
    print("\n[🤖] ANTIGRAVITY AGENT: INICIANDO TESTE DE ESTRESSE (FRAME A FRAME)...")
    
    with sync_playwright() as p:
        # Detecta se há display (para o usuário) ou se roda headless (para o agente)
        is_headless = os.environ.get("HEADLESS", "false").lower() == "true"
        
        print(f"[#] Lançando navegador (Headless: {is_headless})...")
        browser = p.chromium.launch(headless=is_headless) 
        context = browser.new_context(viewport={'width': 1280, 'height': 720})
        page = context.new_page()

        # 🚨 O DETECTOR DE ENTROPIA: Escuta e relata QUALQUER erro vermelho no console
        page.on("console", lambda msg: print(f"[LOG REDOMA] {msg.type.upper()}: {msg.text}"))
        page.on("pageerror", lambda err: print(f"[ERR REDOMA] ERROR: {err}"))

        print("\n[1] 🛡️ Infiltrando o Titanium Gate...")
        try:
            page.goto(URL_ALVO, wait_until="networkidle")
        except Exception as e:
            print(f"❌ Falha ao carregar URL: {e}")
            browser.close()
            return

        print("[#] Aguardando inicialização do Three.js...")
        page.wait_for_timeout(3000) 
        page.screenshot(path="audit_frames/01_boot_inicial.png")

        print("[2] 🔥 Disparando Botão: Focos de Incêndio (Brasil/Amazônia)...")
        page.click(".btn.fi") 
        page.wait_for_timeout(1500)
        page.screenshot(path="audit_frames/02_focos_ativos.png")

        print("[3] 🌳 Disparando Botão: Módulo DOSSEL (Soberania Verde)...")
        page.click(".btn.do")
        page.wait_for_timeout(1500)
        page.screenshot(path="audit_frames/03_modo_dossel.png")

        print("[4] 🐆 Disparando Botão: Biodiversidade (Sauim-de-Coleira)...")
        page.click(".btn.bi")
        page.wait_for_timeout(1500)
        page.screenshot(path="audit_frames/04_biodiversidade.png")

        print("[5] 🎥 Disparando Botão: Sistema de Gravação...")
        page.click("#rec-btn")
        page.wait_for_timeout(2000) 
        page.screenshot(path="audit_frames/05_gravacao_ativa.png")
        # Parar gravação
        page.click("#rec-btn")

        print("[6] 📄 Simulando Inspeção de Quadrante (NetFlora)...")
        # No modo Dossel, clicar no solo (aproximadamente centro)
        page.click(".btn.do") # Garantir que está no modo dossel
        page.wait_for_timeout(500)
        page.mouse.click(640, 400) # Clica numa área central da floresta
        page.wait_for_timeout(1500)
        page.screenshot(path="audit_frames/06_painel_dossel_ativo.png")

        print("\n[✅] AUDITORIA CONCLUÍDA. VERIFIQUE A PASTA 'audit_frames'.")
        print("[✅] SE NÃO HOUVE ERROS DE CONSOLE, O SISTEMA É IMORTAL.")
        browser.close()

if __name__ == "__main__":
    iniciar_auditoria_360()
