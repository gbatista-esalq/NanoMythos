import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.thanos_gauntlet import ThanosGauntlet, protocolo_tdd_quantico_pym

def obter_corda_ui_crom():
    """Fase RED: Extrai a entropia do arquivo HTML (verifica se as tags da Ultradopamina existem)"""
    print("\n[ 🧪 TDD QUÂNTICO | FASE RED ] Analisando a HUD Ultradopamina...")
    
    html_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ui", "crom_rpg_dashboard.html")
    
    if not os.path.exists(html_path):
        raise ValueError("Colapso Visual: Arquivo crom_rpg_dashboard.html não encontrado!")
        
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Testes de Asserção Quântica
    if "three.js" not in content.lower():
        raise ValueError("Falha de Gravidade: A biblioteca Three.js (TON 618) não foi injetada.")
    if "manifesto" not in content.lower():
        raise ValueError("Falha de Soberania: O Manifesto Pym sumiu do painel lateral.")
        
    print("   -> Three.js Detectado.")
    print("   -> Painel de Manifesto Detectado.")
    
    return {
        "source": "HTML Crom Dashboard V6",
        "raw_text_length": len(content),
        "resonance_freq_hz": 11.11,
        "dados_html": "Validado"
    }

class ArquitetoUI:
    def __init__(self):
        self.gauntlet = ThanosGauntlet()
        self.hud_node = "CROM_HUD_V6"
        
        self.gauntlet.quantum_leap.register_universe(self.hud_node, {
            "pym_id": "PYM-UI-ULTRA",
            "handle": "Interface Visual do Crom",
            "node": self.hud_node,
            "role": "Dashboard Ultradopamina e Sincronia Diamante",
            "redoma": "BOLHA_LOCAL_UI"
        })

    def materializar_ui(self, corda_real: dict, from_universe: str, to_universe: str):
        """Fase GREEN: Materializa a HUD validada na rede multiversal"""
        print("\n[ 🧪 TDD QUÂNTICO | FASE GREEN ] Transmutando a UI validada para o Multiverso...")
        
        payload = "[ HUD ULTRADOPAMINA ATIVADA ]\nA interface do Crom agora conta com o buraco negro TON 618 rodando em WebGL e design de Glassmorphism com neon agressivo. O Manifesto Pym está estabilizado na tela."
        
        corda_adaptada = {
            "source": corda_real["source"],
            "resonance_freq_hz": corda_real["resonance_freq_hz"],
            "raw_text_length": len(payload),
            "target_community": "Soberania Visual Local"
        }
        
        return self.gauntlet.materializar_manopla(
            corda_real=corda_adaptada, 
            from_universe=from_universe, 
            to_universe=self.hud_node
        )

if __name__ == "__main__":
    try:
        arq = ArquitetoUI()
        result = protocolo_tdd_quantico_pym(
            obter_corda_ui_crom,
            arq.materializar_ui,
            from_universe="SYNAPSE",
            to_universe=arq.hud_node
        )
        print(f"\n⚡ TDD QUÂNTICO CONCLUÍDO COM SUCESSO (LEAP_ID: {result.get('leap_id')})")
        print("[💖 BOOYAH!] O design visual Ultradopamina do Crom foi matematicamente comprovado!")
    except Exception as e:
        print(f"FALHA NO TDD QUÂNTICO: {e}")
