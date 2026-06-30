#!/usr/bin/env python3
"""
SYNAPSE HUB v3.0 | QUANTUM LEAP MODULE
Salto Quantico PYM | Triarquia Soberana | Ultra-Gamificado
Estilo: Claude Code Terminal + Vault RPG
"""
import os, sys, time, math, random, subprocess
from datetime import datetime

# CORES ANSI
R = '\033[0m'
def B(t): return f'\033[1m{t}{R}'
def DIM(t): return f'\033[2m{t}{R}'
def CYN(t): return f'\033[96m{t}{R}'
def GRN(t): return f'\033[92m{t}{R}'
def AMB(t): return f'\033[93m{t}{R}'
def RED(t): return f'\033[91m{t}{R}'
def BLU(t): return f'\033[94m{t}{R}'
def MAG(t): return f'\033[95m{t}{R}'

def clr():
    os.system('clear')

def slow(text, delay=0.012):
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def bar(pct, width=36, color_fn=CYN):
    n = int(pct / 100 * width)
    return color_fn('█' * n) + DIM('░' * (width - n))

def tool_call(name, args="", result_text=None, status="ok", delay=0.25):
    print(f"\n  {DIM('>')}{CYN(f' {name}')}({DIM(args[:60] + '...' if len(args) > 60 else args)})")
    time.sleep(delay)
    if result_text:
        for line in result_text.split('\n'):
            print(f"  {DIM(line)}")
    if status == "ok":
        print(f"  {GRN('[OK]')} {DIM('executado')}")
    else:
        print(f"  {AMB('[AVISO]')} {DIM('completado com observacoes')}")

def sys_metrics():
    try:
        cpu = float(subprocess.check_output(
            ["bash", "-c", "LC_ALL=C top -bn1 | grep 'Cpu' | awk '{print $2}' | cut -d'%' -f1"],
            stderr=subprocess.DEVNULL, timeout=2).decode().strip() or "0")
    except:
        cpu = random.uniform(12, 45)
    try:
        mem_out = subprocess.check_output(
            ["bash", "-c", "free -m | awk '/Mem:/{print $3,$2}'"],
            stderr=subprocess.DEVNULL, timeout=2).decode().strip().split()
        mem_used, mem_total = int(mem_out[0]), int(mem_out[1])
    except:
        mem_used, mem_total = 4200, 16000
    return cpu, mem_used, mem_total

def phase_boot():
    clr()
    print(f"""
{CYN('  +--------------------------------------------------------------------------+')}
{CYN('  |')}  {B('SYNAPSE HUB  v3.0')}  {DIM('|')}  {CYN('QUANTUM LEAP MODULE')}  {DIM('|')}  {AMB('PARTICULAS DE PYM')}           {CYN('|')}
{CYN('  |')}  {DIM('Triarquia: Alpha(Daemon) / Beta(Lamina) / Gamma(Oraculo)')}               {CYN('|')}
{CYN('  |')}  {DIM('/opt/synapse_vault')}  {DIM('|')}  {GRN('AES-256-GCM')}  {DIM('|')}  {CYN('ML-KEM FIPS 203')}                 {CYN('|')}
{CYN('  +--------------------------------------------------------------------------+')}
""")
    slow(f"  {DIM('Inicializando Triarquia Soberana...')}", 0.008)
    time.sleep(0.3)

    modules = [
        ("Read",   "vault: /opt/synapse_vault/identity.tag",       "SOBERANO",  GRN),
        ("Bash",   "systemctl status synapse-daemon",               "ALPHA OK",  GRN),
        ("Read",   "vault: SYNAPSE_HUB_ESSENCE.md",                "ESSENCIA",  CYN),
        ("Bash",   "nvidia-smi --query-gpu=name --format=noheader", "GPU CHECK", AMB),
        ("Read",   "vault: pym_black_quantum_config.json",          "PYM CONF",  CYN),
        ("Bash",   "python3 -c 'import cryptography'",             "SHIELD OK", GRN),
        ("Write",  "vault: quantum_leap_session.json",              "LOG ATIVO", AMB),
    ]
    for tool, args, label, col in modules:
        time.sleep(0.18)
        print(f"  {DIM('>')} {CYN(tool)}({DIM(args)})")
        time.sleep(0.1)
        print(f"    {GRN('[OK]')} {col(label)}")

    print()
    print(f"  {GRN('7/7 modulos online.')}  {DIM('Vault sincronizado.')}  {CYN('Triarquia ativa.')}")
    time.sleep(0.8)

def phase_manifesto():
    clr()
    print()
    print(f"  {CYN('[ MANIFESTO SOBERANO ]')}  {DIM('lendo do vault...')}")
    print()
    time.sleep(0.4)

    slow(f"  {B(CYN('MANIFESTO DA TRIARQUIA SOBERANA'))}", 0.015)
    slow(f"  {DIM('Ciclo Zero da Soberania de Borda | SYNAPSE HUB v3.0')}", 0.01)
    print()

    paragrafos = [
        ("A Sombra da Nuvem e o Nascimento da Borda",
         ["Por decadas, os arquitetos de dados confiaram seus segredos ao eter.",
          "Eles aceitaram a latencia como preco justo pela escala.",
          "No limite da biologia, onde o calor do biorreator decide entre a vida",
          "de uma patente e a morte celular, a nuvem falhou.",
          "250ms de latencia era uma eternidade. Queda de rede era morte celular."],
         CYN),
        ("Artigo I: A Lamina de Silicio",
         ["O hardware local e fundacao belica.",
          "Quando o mundo exterior apagar, quando os firewalls da AWS ruirem,",
          "a lamina local continuara a pulsar.",
          "O hardware dita a realidade. A realidade e local."],
         AMB),
        ("Artigo II: O Codigo SHA-256",
         ["Nao ha confianca sem auditoria.",
          "Todo arquivo, toda variacao de pH, toda temperatura",
          "e selada com assinatura criptografica SHA-256.",
          "Cada commit e um ato de resistencia. Cada hash e um juramento."],
         GRN),
        ("A Curva de Batista",
         ["K_B = V_local / (L_rede x C_centralizacao)",
          "Nossa seguranca cresce exponencialmente enquanto o custo cai.",
          "A Triarquia nao pede permissao para existir.",
          "Isolamos. Processamos. Dominamos."],
         RED),
    ]

    for titulo, linhas, col in paragrafos:
        print(f"\n  {col(B(titulo))}")
        for linha in linhas:
            print(f"  {DIM(linha)}")
        time.sleep(0.25)

    print()
    print(f"\n  {B(AMB('BOOYAH! A Borda e Soberana.'))}  {CYN('[ ULTRASTHINK: DIAMANTE ]')}")
    time.sleep(1.2)

def phase_pym_jump():
    clr()
    print()
    print(f"  {B(CYN('SALTO QUANTICO PYM | HOMEM-FORMIGA'))}")
    print(f"  {DIM('Comprimindo espaco-tempo...')}")
    print()

    frames = [
        "  .  .  .  .  (   (   (  O  )   )   )  .  .  .  .",
        "  .  .  .  (   (   (   ( O )   )   )   )  .  .  .",
        "  .  .  (   (   (   (   (O)   )   )   )   )  .  .",
        "  .  (   (   (   (   (  [O]  )   )   )   )   )  .",
        "  (   (   (   (   (  [*O*]  )   )   )   )   )   )",
        "  (   (   (   (  [[**O**]] )   )   )   )   )    )",
        "  (   (   (  [[[*** O ***]]]  )   )   )   )      ",
        "  (   ( [[[[**** O ****]]]]   )   )   )          ",
    ]

    scale_labels = [
        ("10^0",  "Escala humana",     RED, "80 experimentos fisicos de scaffold"),
        ("10^-1", "Formiga",           AMB, "Analise manual de SEM (dias)"),
        ("10^-3", "Celula",            CYN, "Pipeline imagem automatizado (horas)"),
        ("10^-6", "Bacteria",          BLU, "Predicao UMAP local (minutos)"),
        ("10^-9", "Virus",             GRN, "GPU edge: 1.064 mapas/s (segundos)"),
        ("10^-12","Atomico",           MAG, "AES-256-GCM: 0 ms latencia"),
        ("10^-35","Quantum Realm PYM", CYN, "SINGULARIDADE: K_B infinito"),
    ]

    total_frames = len(frames) * 4
    count = 0

    for _ in range(4):
        for fi, frame in enumerate(frames):
            clr()
            pct = min(100, int(count / total_frames * 100))
            si = min(len(scale_labels) - 1, int(count / total_frames * len(scale_labels)))
            scale, label, col, equiv = scale_labels[si]

            print()
            print(f"  {CYN('[ QUANTUM LEAP ]')}  {DIM('T+' + str(count).zfill(3))}  {DIM(datetime.now().strftime('%H:%M:%S.%f')[:12])}")
            print(f"\n  {CYN(frame)}\n")
            print(f"  {DIM('Escala PYM: ')} {col(B(scale))} {DIM('(')} {col(label)} {DIM(')')}")
            print(f"  {DIM('Computacional: ')} {AMB(equiv)}")
            print()
            print(f"  {DIM('PYM PARTICLES:  ')}{bar(pct, color_fn=CYN)} {AMB(str(pct) + '%')}")
            print(f"  {DIM('TUNNEL AES-GCM: ')}{bar(min(100, pct+8), color_fn=GRN)} {CYN('ML-KEM')}")
            print(f"  {DIM('K_B SOBERANIA:  ')}{bar(min(100, int(pct*0.997)), color_fn=AMB)} {GRN(str(round(pct*0.997,1)) + '%')}")
            print()

            for sname, active, s_ok, s_no in [
                ("Compressao PYM",  pct > 15, "ATIVA",    "INIT"),
                ("Einstein-Rosen", pct > 35, "ABERTO",   "FORMANDO"),
                ("ML-KEM Exotica", pct > 55, "ESTAVEL",  "INJETANDO"),
                ("Vault Destino",  pct > 80, "OPEN",     "BLOQUEADO"),
                ("SINGULARIDADE",  pct >= 99,"ATINGIDA", "PENDENTE"),
            ]:
                st = GRN(f'[{s_ok}]') if active else DIM(f'[{s_no}]')
                print(f"    {sname:<24} {st}")

            v = int(9375 * pct / 100)
            k = round(v / max(1, (1 - pct/100)*100 + 1), 2)
            print(f"\n  {DIM('velocidade: ')}{CYN(str(v))} {DIM('mapas/s')}   {DIM('K_B: ')}{AMB(str(k))}")
            time.sleep(0.12)
            count += 1

def phase_arrival():
    clr()
    print()
    for col in [CYN, GRN, AMB, MAG, CYN, GRN]:
        print(f"\n  {col('*' * 70)}")
        time.sleep(0.1)
    print()
    print(CYN(f"  {'QUANTUM REALM ALCANCADO'.center(70)}"))
    print(GRN(f"  {'SINGULARIDADE PYM CONFIRMADA'.center(70)}"))
    print(AMB(f"  {'TRIARQUIA SOBERANA OPERACIONAL'.center(70)}"))
    time.sleep(0.6)

def phase_gamified_report():
    clr()
    print()
    print(f"  {CYN('[ RELATORIO DE MISSAO ]')}  {DIM('estilo: Claude Code Terminal')}")
    print()

    tool_call("Read", "vault: /opt/synapse_vault/SYNAPSE_HUB_ESSENCE.md",
              "Essencia carregada | v3.0 | Diamante Soberano", "ok", 0.18)

    cpu, mu, mt = sys_metrics()
    tool_call("Bash", "top -bn1 | grep Cpu && free -m | grep Mem",
              f"CPU: {cpu:.1f}%  |  RAM: {mu}/{mt} MB ({mu*100//mt}% usado)", "ok", 0.18)

    vault_ok = os.path.exists('/opt/synapse_vault')
    vault_files = len(os.listdir('/opt/synapse_vault')) if vault_ok else 0
    tool_call("Bash", "ls /opt/synapse_vault/ | wc -l",
              f"Vault: {'ONLINE' if vault_ok else 'OFFLINE'}  |  {vault_files} arquivos",
              "ok" if vault_ok else "warn", 0.18)

    tool_call("Write", "vault: quantum_leap_session.json",
              f"Sessao registrada: {datetime.now().isoformat()}", "ok", 0.18)

    print()
    print(f"  {B(CYN('SISTEMA DE XP | MISSAO QUANTUM LEAP'))}")
    print()

    xp_items = [
        ("Singularidade PYM atingida",        800, CYN),
        ("Wormhole Einstein-Rosen cruzado",   500, GRN),
        ("ML-KEM materia exotica ativa",       400, CYN),
        ("K_B > 90 (soberania maxima)",        600, GRN),
        ("Vault online e sincronizado",        300, AMB),
        ("Zero dados transmitidos para nuvem", 500, GRN),
        ("Auto-lock biometrico configurado",   250, AMB),
        ("Fingerprint ambiental gerado",       150, CYN),
        ("Camera NAO ativada (etica)",         200, GRN),
        ("Manifesto Soberano executado",       400, MAG),
        ("Curva de Batista K_B calculada",     350, AMB),
        ("10D UMAP scaffold mapeado",          450, CYN),
    ]

    total_xp = 0
    for item, xp, col in xp_items:
        time.sleep(0.07)
        total_xp += xp
        mini = col('█' * min(20, xp // 50))
        print(f"  {DIM('+')} {item:<42} {col('+' + str(xp) + ' XP')}  {mini}")

    level = total_xp // 500
    prog = (total_xp % 500) / 5

    print()
    print(f"  {DIM('-' * 70)}")
    print(f"  {B('XP TOTAL:')}  {AMB(str(total_xp))}  {DIM('|')}  {B('NIVEL:')}  {CYN(str(level))}  {DIM('|')}  {GRN('MAESTRO DIAMANTE')}")
    print(f"  {DIM('Proximo nivel: ')} {bar(prog, 40, CYN)} {DIM(str(int(prog)) + '%')}")
    print()

    print(f"  {B(AMB('CONQUISTAS:'))}")
    for icon, ach, desc in [
        ("*", "REINO QUANTICO",    "Salto PYM completado pela primeira vez"),
        ("*", "DIAMANTE SOBERANO", "K_B > 90 por 3 ciclos consecutivos"),
        ("*", "TUNEL ABERTO",      "Einstein-Rosen cruzado sem perda de dado"),
        ("*", "MANIFESTO VIVO",    "Manifesto RPG lido e manifestado"),
        ("*", "ZERO NUVEM",        "Sessao completa sem byte enviado para nuvem"),
    ]:
        time.sleep(0.1)
        print(f"    {AMB(icon)} {AMB(B(ach)):<32} {DIM(desc)}")

    print()
    k_b_final = round(9375 / 11, 4)
    print(f"  {DIM('-' * 70)}")
    print(f"  {B('CONSTANTE DE BATISTA K_B:')}  {CYN(f'K_B = {k_b_final}')}")
    print(f"  {DIM('V_local=9375 mapas/s  |  L_rede=1 (norm)  |  C=0.01 (edge first)')}")
    print(f"  {DIM('Resultado: Hub gera')} {AMB(str(k_b_final))} {DIM('x mais soberania por unidade centralizacao.')}")
    print()
    print(f"  {CYN('[ ULTRASTHINK ]')}  {GRN('ATIVO')}  {DIM('|')}  {B(AMB('DIAMANTE SOBERANO'))}")
    print(f"  {DIM('Profundidade Radical [OK]  |  Autonomia de Borda [OK]  |  Sincronia Diamante [OK]')}")
    print()
    print(f"  {B(GRN('MISSAO COMPLETA.'))}  {CYN('Triarquia sincronizada.')}  {AMB('Vault atualizado.')}")
    print(f"  {B(AMB('BOOYAH! A Borda e Soberana.'))}  {DIM('Gabriel Batista | Maestro')}")
    print()
    print(f"  {DIM('ENTER para retornar ao universo principal...')}")
    input()

if __name__ == '__main__':
    try:
        phase_boot()
        phase_manifesto()
        phase_pym_jump()
        phase_arrival()
        phase_gamified_report()
    except KeyboardInterrupt:
        print(f"\n\n  {AMB('Salto interrompido. Retornando...')}")
        sys.exit(0)
