from playwright.sync_api import sync_playwright
import time
import os
import shutil

OUTPUT_DIR = "/home/synapseagtech/Área de Trabalho/SYNAPSE AGTECH/auditoria_final"
ARTIFACTS_DIR = "/home/synapseagtech/.gemini/antigravity/brain/c571e624-8052-43f9-8368-29c8792bb6ba"

def take_shot(page, name):
    path = os.path.join(OUTPUT_DIR, name)
    page.screenshot(path=path)
    if os.path.exists(ARTIFACTS_DIR):
        shutil.copy(path, os.path.join(ARTIFACTS_DIR, name))
    print(f"Saved {name}")

def run():
    # Headless=False para que o Maestro veja rodando "em tela"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page(viewport={"width": 1280, "height": 720})
        
        # Load page
        page.goto("http://localhost:8888/reino_quantico_amazonia.html?token=DALILA_USP_01")
        time.sleep(3)
        
        # Abrir painel de filtros
        page.click("#btn-filtros")
        time.sleep(1)
        
        # Selecionar VERRA
        page.select_option("#filtro-camada", "verra")
        time.sleep(3) # Tempo para processar o JSON 3D
        take_shot(page, "08_camada_verra.png")
        
        # Selecionar TIs (FUNAI)
        page.select_option("#filtro-camada", "ti")
        time.sleep(4) # JSON pesado
        take_shot(page, "09_camada_tis.png")
        
        # Selecionar UCs
        page.select_option("#filtro-camada", "uc")
        time.sleep(4)
        take_shot(page, "10_camada_ucs.png")
        
        # Voltar ao normal
        page.select_option("#filtro-camada", "none")
        time.sleep(1)
        
        # Teste final IA Generativa + Fogo
        page.click(".btn.fi")
        time.sleep(1)
        page.click("#btn-gen")
        time.sleep(1)
        page.click(".gp-action-btn")
        time.sleep(1.5)
        take_shot(page, "11_stress_total.png")
        
        time.sleep(2)
        browser.close()

if __name__ == "__main__":
    run()
