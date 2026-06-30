import time
import os
import shutil
from playwright.sync_api import sync_playwright
from PIL import Image
import numpy as np

OUTPUT_DIR = "/home/synapseagtech/Área de Trabalho/SYNAPSE AGTECH/auditoria_final"
ARTIFACTS_DIR = "/home/synapseagtech/.gemini/antigravity/brain/c571e624-8052-43f9-8368-29c8792bb6ba"

def get_brightness(image_path):
    img = Image.open(image_path).convert('L') # convert to grayscale
    stat = np.array(img)
    return np.mean(stat)

def take_shot(page, name):
    path = os.path.join(OUTPUT_DIR, name)
    page.screenshot(path=path)
    brightness = get_brightness(path)
    print(f"Saved {name} - Brilho Médio: {brightness:.2f}")
    if brightness < 15:
        print(f"  ⚠ ALERTA: Modo {name} detectado como MUITO ESCURO!")
    if os.path.exists(ARTIFACTS_DIR):
        shutil.copy(path, os.path.join(ARTIFACTS_DIR, name))

def run():
    print("🚀 Iniciando Protocolo 360 Graus Triarquia Ultrathink — VALIDAÇÃO DE LUMINOSIDADE...")
    with sync_playwright() as p:
        # headless=True para performance, mas os resultados são os mesmos para o renderer
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 720})
        
        page.goto("http://localhost:8888/reino_quantico_amazonia.html?token=DALILA_USP_01")
        time.sleep(4)
        
        modes = [
            ('FLORESTA', '12_modo_floresta.png'),
            ('INCÊNDIO', '13_modo_incendio.png'),
            ('RESTAURO', '14_modo_restauro.png'),
            ('NOITE', '15_modo_noite.png'),
            ('BIODIVERSIDADE', '16_modo_biodiversidade.png'),
            ('DOSSEL', '17_modo_dossel.png')
        ]
        
        for text, filename in modes:
            print(f"Testando {text}...")
            page.click(f"text={text}", force=True)
            time.sleep(1.5)
            take_shot(page, filename)
        
        print("Testando FILTROS (VERRA)...")
        page.click("text=🔍 FILTROS", force=True)
        time.sleep(1)
        page.select_option("#filtro-camada", "verra")
        time.sleep(3)
        take_shot(page, "18_filtros_verra.png")
        
        print("Testando EFEITO NASA (Zoom Orbital)...")
        page.mouse.move(640, 360)
        page.mouse.wheel(0, 10000) # Zoom out máximo
        time.sleep(4)
        take_shot(page, "21_efeito_nasa.png")
        
        browser.close()
        print("✅ Validação de Brilho e Modos Concluída.")

if __name__ == "__main__":
    run()
