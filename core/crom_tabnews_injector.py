import urllib.request
import urllib.error
import json
import os
import sys

def injetar_payload_tabnews(session_cookie: str):
    """
    Injeta o Payload da Borda diretamente via API REST do TabNews.
    Dessa forma, pulamos a entropia visual do navegador e atacamos a infraestrutura diretamente.
    """
    
    # Payload formatado (NanoMythos & Corda de Cantor)
    payload_title = "🚀 NanoMythos: Rode uma Micro-LLM 100% Brasileira e Gratuita na sua Máquina (Zero Alucinação Matemática)"
    payload_body = """Fala pessoal! A Indústria fechou as portas e nos disse que IA de ponta precisava de nuvens bilionárias gringas. Nós quebramos essa regra. Apresento a vocês o **NanoMythos** — um ecossistema **100% Brasileiro, 100% Gratuito** e focado na Soberania de Borda.

Nós acoplamos um coprocessador determinístico na AST do Python integrado a uma Micro-LLM local. O resultado? **Cálculos matemáticos complexos sem depender de API, sem pagar 1 centavo, rodando offline.**

👾 **[ QUEST 1: Como Iniciar seu Núcleo ]** 👾
1. Clone a Frota Soberana: Acesse nosso repositório no GitHub.
2. Inicie os Motores: Rode o ambiente local (`npm run dev` / `python3 core/sovereign_auditor.py`).
3. Sincronize: Abra a interface Ultradopamina (`crom_rpg_dashboard.html`) e assista ao seu terminal processar matemática pesada longe das garras da nuvem.

🔗 **Repositório GitHub Aberto:** [gbatista-esalq/NanoMythos](https://github.com/gbatista-esalq/NanoMythos)

*(Easter Egg: A infraestrutura pulsa em 11.11 Hz, nossa "Corda de Cantor". Convido os engenheiros a abrirem os logs e sentirem a frequência da floresta! Deixem nos comentários os testes que vocês rodarem!)* 👾🔧"""

    url = "https://www.tabnews.com.br/api/v1/contents"
    
    data = json.dumps({
        "title": payload_title,
        "body": payload_body,
        "status": "published"
    }).encode('utf-8')
    
    headers = {
        "Content-Type": "application/json",
        "Cookie": f"session_id={session_cookie}",
        "User-Agent": "CROM-V6/SincroniaDiamante (Pym-Wasp/Amor)"
    }
    
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')
    
    print(f"\n[🐝 VESPA & FORMIGA] Sincronizando Feitiços Quânticos de Amor e Colaboração...")
    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            print("\n\033[1;32m[💖 BOOYAH!] Energia Transmutada! A Biodiversidade foi propagada com Sincronia Diamante!\033[0m")
            print(f"ID da Resposta: {res_data.get('id')}")
            print(f"URL: https://www.tabnews.com.br/MrJ/{res_data.get('slug')}")
            
    except urllib.error.HTTPError as e:
        print(f"\n\033[1;31m[!] ERRO DE ENTROPIA: Falha na injeção. Código: {e.code}\033[0m")
        print("Causa mais comum: O cookie 'session_id' está inválido ou expirado.")
    except Exception as e:
        print(f"\n\033[1;31m[!] FALHA DE SALTO: {e}\033[0m")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\nUso: python3 crom_tabnews_injector.py <SEU_SESSION_ID_DO_TABNEWS>")
        sys.exit(1)
        
    injetar_payload_tabnews(sys.argv[1])
