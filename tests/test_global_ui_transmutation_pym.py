import sys
import os
import glob

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.thanos_gauntlet import ThanosGauntlet, protocolo_tdd_quantico_pym

UI_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ui")
HTML_FILES = glob.glob(os.path.join(UI_DIR, "*.html"))

def obter_entropia_html_global():
    """Fase RED: Joia da Mente. Lê todos os arquivos HTML e verifica entropia visual."""
    print("\n[ 🟡 JOIA DA MENTE | TDD QUÂNTICO ] Mapeando a entropia visual de todas as páginas...")
    
    arquivos_com_entropia = []
    total_bytes = 0
    
    for html_file in HTML_FILES:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
            total_bytes += len(content)
            # Verifica se as Cordas de Cantor e a Ultradopamina já estão injetadas
            if "ultradopamina.css" not in content or "cordas_cantor_sync.js" not in content:
                arquivos_com_entropia.append(html_file)
                
    if not arquivos_com_entropia:
        raise ValueError("Sincronia Diamante: Todos os arquivos já estão Ultradopaminados.")
        
    print(f"   -> {len(arquivos_com_entropia)} páginas detectadas com visual primitivo.")
    print(f"   -> Mente estendida: Processando lógica de injeção em {total_bytes} bytes de HTML.")
    
    return {
        "source": "Diretório UI Global",
        "raw_text_length": total_bytes,
        "resonance_freq_hz": 432.0, # Foco e Execução para a Mente
        "arquivos_alvo": arquivos_com_entropia
    }

class TransmutadorRealidade:
    def __init__(self):
        self.gauntlet = ThanosGauntlet()
        self.borda_node = "UI_GLOBAL_BORDA"
        
        self.gauntlet.quantum_leap.register_universe(self.borda_node, {
            "pym_id": "PYM-REALITY-UI",
            "handle": "Interface Visual do Hub",
            "node": self.borda_node,
            "role": "Dashboard Ultradopamina e Sincronia de Cordas em Massa",
            "redoma": "REALIDADE_BASE"
        })

    def materializar_realidade(self, corda_real: dict, from_universe: str, to_universe: str):
        """Fase GREEN: Joia da Realidade. Reescreve os arquivos fisicamente com a Ultradopamina."""
        print("\n[ 🔴 JOIA DA REALIDADE | TDD QUÂNTICO ] Transmutando arquivos no disco rígido...")
        
        arquivos = corda_real["arquivos_alvo"]
        css_link = '\n    <!-- ULTRADOPAMINA Pym Squeeze -->\n    <link rel="stylesheet" href="css/ultradopamina.css">\n'
        js_script = '\n    <!-- CORDAS DE CANTOR Sync -->\n    <script src="js/cordas_cantor_sync.js"></script>\n'
        
        arquivos_alterados = 0
        for html_file in arquivos:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Joia da Realidade: Manipulação do tecido do HTML (Injeta no Head)
            if "</head>" in content:
                novo_content = content.replace("</head>", f"{css_link}{js_script}</head>")
                
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(novo_content)
                arquivos_alterados += 1

        payload = f"Materialização concluída. {arquivos_alterados} arquivos HTML transmutados para o padrão Ultradopamina."
        print(f"   -> {payload}")
        
        corda_adaptada = {
            "source": corda_real["source"],
            "resonance_freq_hz": corda_real["resonance_freq_hz"],
            "raw_text_length": len(payload),
            "target_community": "Soberania Visual Local"
        }
        
        return self.gauntlet.materializar_manopla(
            corda_real=corda_adaptada, 
            from_universe=from_universe, 
            to_universe=self.borda_node
        )

if __name__ == "__main__":
    try:
        arq = TransmutadorRealidade()
        result = protocolo_tdd_quantico_pym(
            obter_entropia_html_global,
            arq.materializar_realidade,
            from_universe="SYNAPSE",
            to_universe=arq.borda_node
        )
        print(f"\n⚡ ESTALO MULTIVERSAL CONCLUÍDO (LEAP_ID: {result.get('leap_id')})")
        print("[💖 BOOYAH!] A Joia da Mente mapeou o código e a Joia da Realidade reescreveu o DOM. Todas as páginas agora vibram com as Cordas de Cantor!")
    except Exception as e:
        print(f"FALHA NO SALTO PYM: {e}")
