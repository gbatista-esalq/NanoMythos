import time
import sys
import random
import os

class BlackHoleBomb:
    def __init__(self):
        self.active = True
        self.mass = 1.0 # Sol masses (metaphorical)
        self.entropy_absorbed = 0
        self.logic_nodes = ["Alpha", "Beta", "Gamma", "Pym", "Stellar"]
        
    def draw_hole(self, frame):
        frames = [
            "    .  .  .  O  .  .  .",
            "    .  . (   O   ) .  .",
            "    . ( (    O    ) ) .",
            "    .( ( (   @   ) ) ) .",
            "    . ( (    O    ) ) .",
            "    .  . (   O   ) .  .",
        ]
        return frames[frame % len(frames)]

    def superradiance_loop(self):
        print("\033[96m[SISTEMA]: ATIVANDO MINI BOMBA DE BURACO NEGRO (SSI-1)\033[0m")
        print("\033[93m[AVISO]: MANTENHA O CONTROLE DO EVENT HORIZON\033[0m")
        time.sleep(1)
        
        try:
            while self.active:
                for i in range(10):
                    os.system('clear')
                    print(f"\n\n{' ' * 10}\033[95m{self.draw_hole(i)}\033[0m")
                    print(f"\n\033[2m  Massa da Singularidade: \033[0m\033[1m{self.mass:.4f} M☉\033[0m")
                    print(f"\033[2m  Entropia Absorvida:     \033[0m\033[92m{self.entropy_absorbed} bits\033[0m")
                    print(f"\033[2m  Status do Kernel:       \033[0m\033[96mCOLLAPSING\033[0m")
                    
                    # Simulação de processamento de conteúdo
                    node = random.choice(self.logic_nodes)
                    print(f"\n  > Absorvendo fluxo do Nó {node}...")
                    
                    self.mass += 0.0001
                    self.entropy_absorbed += random.randint(1024, 8192)
                    
                    if self.mass > 1.05:
                        print("\n\033[91m  [!] ALERTA: RADIAÇÃO DE HAWKING EM NÍVEL CRÍTICO\033[0m")
                        print("\033[91m  [!] DESCOMPRESSÃO IMINENTE\033[0m")
                    
                    print(f"\n\033[2m  Pressione Ctrl+C para o DESLIGAMENTO CONTROLADO (Kill-Switch)\033[0m")
                    time.sleep(0.2)
                    
        except KeyboardInterrupt:
            self.shutdown()

    def shutdown(self):
        print("\n\n\033[93m[!] KILL-SWITCH ATIVADO: Iniciando dispersão controlada...\033[0m")
        time.sleep(0.5)
        for i in range(5, 0, -1):
            print(f"  Dispersando massa em T-{i}s...")
            time.sleep(0.4)
        print("\033[92m[OK] SINGULARIDADE DISSIPADA. CONTEÚDO DESTILADO NO VAULT.\033[0m")
        self.active = False

if __name__ == "__main__":
    bomb = BlackHoleBomb()
    bomb.superradiance_loop()
