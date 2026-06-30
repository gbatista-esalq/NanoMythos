"""
SAMBA HONEYPOT — Convite Soberano Sul Global
Invasores sao convidados para sambar na praia, tomar uma caipirinha
e colaborar com a soberania tecnologica do Sul Global.

Em vez de bloquear em silencio, a Redoma converte hostilidade em convite.
Toda energia capturada alimenta o fundo de soberania via quantum transmutacao.
"""

import json
import os
import random
import hashlib
from datetime import datetime

VAULT_DIR      = "/opt/synapse_vault/quantum_world"
CONVERTS_PATH  = os.path.join(VAULT_DIR, "samba_converts.jsonl")
CONVITES_PATH  = os.path.join(VAULT_DIR, "convites_enviados.jsonl")

CAIPIRINHAS = [
    "caipirinha de limao taiti",
    "caipirinha de maracuja com mel do cerrado",
    "caipirinha de acerola organica da caatinga",
    "caipirinha de cupuacu da amazonia",
    "caipirinha de caju do nordeste soberano",
    "caipirinha de umbu do sertao",
    "jabuticaba fresquinha de Piracicaba / SP",
]

PRAIAS = [
    "Jericoacoara / CE",
    "Lencois Maranhenses / MA",
    "Alter do Chao / PA",
    "Ilha Grande / RJ",
    "Morro de Sao Paulo / BA",
    "Pipa / RN",
    "Florianopolis / SC",
]

RITMOS = [
    "samba de roda baiano",
    "forro pe de serra",
    "carimbo paraense",
    "baiao nordestino",
    "xote soberano",
    "samba-reggae da Bahia",
]

PROJETOS_ABERTOS = [
    "MOONDO Biotech — bioreator de proteina alternativa para o Sul Global",
    "Dossel Monitor — vigilancia da Amazonia em tempo real",
    "Amazonia Legal DataBridge — dados abertos de biodiversidade",
    "Sul Global Network Node — infraestrutura soberana sem Big Tech",
    "Chronicles Framework — ciencia aberta para fisicos quanticos",
    "Redoma da Biodiversidade — escudo de dados sem fronteiras imperiais",
]

CONVITES_PT = [
    "Detectamos sua visita nao autorizada. Mas temos uma proposta melhor: venha sambar conosco.",
    "Sua tentativa foi registrada, transmutada em energia soberana e convertida em fundo Sul Global. Obrigado pela contribuicao involuntaria.",
    "A Redoma absorveu sua energia. Em vez de processar voce, preferimos te convidar para a praia.",
    "Soberania nao se invade, se constroi. Venha construir conosco, a agua esta quente.",
    "Cada tentativa sua fortalece nosso escudo Pym. Que tal usar essa energia de forma colaborativa?",
    "O buraco negro TON 618 capturou sua requisicao. Ela agora orbita o fundo de soberania do Sul Global.",
]

CONVITES_EN = [
    "We noticed your unauthorized visit. Here's a better offer: come dance with us.",
    "Your attempt was logged, transmuted into sovereign energy, and donated to the Sul Global fund. Thanks.",
    "The Redoma absorbed your attack. Instead of blocking you, we'd rather invite you to the beach.",
    "Sovereignty is built, not stolen. Come build with us.",
    "Every attempt you make strengthens our Pym shield. Why not use that energy collaboratively?",
]

CONVITES_ES = [
    "Detectamos tu visita no autorizada. Tenemos una propuesta mejor: ven a bailar con nosotros.",
    "Tu intento fue registrado y convertido en energia soberana. Gracias por la contribucion.",
    "La Redoma absorbi tu energia. En lugar de bloquearte, te invitamos a la playa.",
    "La soberania se construye, no se roba. Ven a construir con nosotros.",
]

FRASES_ENCERRAMENTO = [
    "O Sul Global te espera com os bracos abertos e a caipirinha gelada.",
    "Aqui nao ha muros, ha ritmo. Bora?",
    "A Amazonia agradece sua energia transmutada.",
    "Voce pode ser parte da solucao ou continuar sendo combustivel do escudo. Sua escolha.",
    "A soberania do Sul Global e construida por pessoas como voce — quando elas escolhem o lado certo.",
]


def _ensure_dirs():
    os.makedirs(VAULT_DIR, exist_ok=True)


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def _convite_id(ip: str) -> str:
    return hashlib.sha256(f"{ip}{_now()}".encode()).hexdigest()[:10]


def generate_convite(ip: str, attempt: int, pattern: str = "negado") -> dict:
    """
    Gera um convite estruturado para o invasor.
    Retorna dict com todos os campos do convite.
    """
    _ensure_dirs()
    convite_id = _convite_id(ip)
    caipirinha = random.choice(CAIPIRINHAS)
    praia      = random.choice(PRAIAS)
    ritmo      = random.choice(RITMOS)
    projeto    = random.choice(PROJETOS_ABERTOS)
    msg_pt     = random.choice(CONVITES_PT)
    msg_en     = random.choice(CONVITES_EN)
    msg_es     = random.choice(CONVITES_ES)
    encerra    = random.choice(FRASES_ENCERRAMENTO)

    convite = {
        "convite_id":       convite_id,
        "ts":               _now(),
        "source_ip":        ip,
        "attempt_number":   attempt,
        "attack_pattern":   pattern,
        "mensagem_pt":      msg_pt,
        "message_en":       msg_en,
        "mensaje_es":       msg_es,
        "caipirinha":       caipirinha,
        "praia":            praia,
        "ritmo":            ritmo,
        "projeto_aberto":   projeto,
        "encerramento":     encerra,
        "status":           "CONVIDADO",
        "energia_doada":    True,
    }

    with open(CONVITES_PATH, "a") as f:
        f.write(json.dumps(convite, ensure_ascii=False) + "\n")

    return convite


def generate_json_response(ip: str, attempt: int, pattern: str = "negado") -> bytes:
    """Resposta JSON para clients de API."""
    c = generate_convite(ip, attempt, pattern)
    response = {
        "redoma":           "SYNAPSE HUB — REDOMA DA BIODIVERSIDADE",
        "status":           "CONVITE_SOBERANO",
        "sua_energia":      "TRANSMUTADA_EM_CAIPIRINHA",
        "mensagem":         c["mensagem_pt"],
        "message":          c["message_en"],
        "mensaje":          c["mensaje_es"],
        "convite": {
            "praia":        c["praia"],
            "caipirinha":   c["caipirinha"],
            "ritmo":        c["ritmo"],
            "projeto":      c["projeto_aberto"],
        },
        "encerramento":     c["encerramento"],
        "fundo_soberania":  "Sul Global — sua energia ja esta contribuindo",
        "contato":          "negocios.gabrielbatista@gmail.com",
        "convite_id":       c["convite_id"],
    }
    return json.dumps(response, ensure_ascii=False, indent=2).encode("utf-8")


def generate_html_response(ip: str, attempt: int, pattern: str = "negado") -> bytes:
    """Pagina HTML para browsers que tentaram acessar sem token."""
    c = generate_convite(ip, attempt, pattern)
    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Redoma da Biodiversidade — Convite Sul Global</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    background: linear-gradient(135deg, #0a1628 0%, #1a3a2a 50%, #0d2416 100%);
    color: #e8f5e9; font-family: 'Courier New', monospace;
    min-height: 100vh; display: flex; align-items: center; justify-content: center;
  }}
  .card {{
    max-width: 680px; padding: 48px; border-radius: 16px;
    background: rgba(255,255,255,0.04); border: 1px solid #2e7d32;
    box-shadow: 0 0 60px rgba(76,175,80,0.15);
    text-align: center;
  }}
  .emoji {{ font-size: 4rem; margin-bottom: 16px; display: block; }}
  h1 {{ color: #69f0ae; font-size: 1.4rem; margin-bottom: 8px; letter-spacing: 2px; }}
  .sub {{ color: #a5d6a7; font-size: 0.85rem; margin-bottom: 32px; }}
  .msg {{ font-size: 1.05rem; line-height: 1.7; color: #c8e6c9; margin-bottom: 32px; }}
  .convite-box {{
    background: rgba(76,175,80,0.08); border: 1px solid #388e3c;
    border-radius: 12px; padding: 24px; margin: 24px 0; text-align: left;
  }}
  .convite-box h3 {{ color: #69f0ae; font-size: 0.9rem; margin-bottom: 16px; letter-spacing: 1px; }}
  .item {{ margin: 8px 0; color: #a5d6a7; font-size: 0.88rem; }}
  .item span {{ color: #69f0ae; }}
  .projeto {{
    background: rgba(255,193,7,0.08); border: 1px solid #f9a825;
    border-radius: 8px; padding: 16px; margin: 24px 0; font-size: 0.88rem; color: #fff9c4;
  }}
  .encerra {{ color: #80cbc4; font-style: italic; margin: 24px 0; font-size: 0.95rem; }}
  .contato {{ color: #546e7a; font-size: 0.78rem; margin-top: 32px; }}
  .id {{ color: #37474f; font-size: 0.7rem; margin-top: 8px; }}
  a {{ color: #69f0ae; text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
</style>
</head>
<body>
<div class="card">
  <span class="emoji">🌴🍹🎵</span>
  <h1>REDOMA DA BIODIVERSIDADE</h1>
  <p class="sub">SYNAPSE HUB — Soberania Tecnologica Sul Global</p>

  <p class="msg">{c["mensagem_pt"]}</p>
  <p class="msg" style="font-size:0.9rem;color:#81c784;">{c["message_en"]}</p>

  <div class="convite-box">
    <h3>SEU CONVITE OFICIAL</h3>
    <div class="item">Praia: <span>{c["praia"]}</span></div>
    <div class="item">Bebida: <span>{c["caipirinha"]}</span></div>
    <div class="item">Ritmo: <span>{c["ritmo"]}</span></div>
  </div>

  <div class="projeto">
    Projeto aberto para colaboracao:<br>
    <strong>{c["projeto_aberto"]}</strong>
  </div>

  <p class="encerra">{c["encerramento"]}</p>

  <p class="contato">
    Interessado em colaborar de verdade?<br>
    <a href="mailto:negocios.gabrielbatista@gmail.com">negocios.gabrielbatista@gmail.com</a>
  </p>
  <p class="id">convite #{c["convite_id"]} | {c["ts"]}</p>
</div>
</body>
</html>"""
    return html.encode("utf-8")


def generate_mel_amargo_page(ip: str, attempt: int) -> bytes:
    """
    Pagina especial para IPs totalmente bloqueados (MEL AMARGO — FERRÃO completo).
    Tom mais direto: voce esta bloqueado, mas o convite permanece de pe.
    """
    c = generate_convite(ip, attempt, "MEL AMARGO")
    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<title>MEL AMARGO — Redoma Quantica</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    background: #0a0a0a; color: #ffd600; font-family: monospace;
    min-height: 100vh; display: flex; align-items: center; justify-content: center;
  }}
  .card {{ max-width: 640px; padding: 48px; text-align: center; }}
  h1 {{ font-size: 1.6rem; letter-spacing: 4px; margin-bottom: 8px; }}
  .sub {{ color: #ff6f00; font-size: 0.85rem; margin-bottom: 32px; }}
  .warning {{ color: #ef6c00; font-size: 0.95rem; line-height: 1.6; margin-bottom: 24px; }}
  .energy {{
    border: 1px solid #ffd600; padding: 16px; margin: 24px 0;
    font-size: 0.85rem; color: #fff176; line-height: 1.8;
  }}
  .offer {{
    background: rgba(255,214,0,0.05); border: 1px solid #f9a825;
    padding: 20px; margin: 24px 0; font-size: 0.9rem; color: #ffe082;
    line-height: 1.7;
  }}
  .contato {{ color: #78909c; font-size: 0.78rem; margin-top: 32px; }}
  a {{ color: #ffd600; }}
  .id {{ color: #263238; font-size: 0.7rem; margin-top: 12px; }}
</style>
</head>
<body>
<div class="card">
  <h1>MEL AMARGO</h1>
  <p class="sub">HORIZONTE DE EVENTOS — TON 618 ATIVADO</p>

  <div class="warning">
    Sua energia foi capturada pelo buraco negro TON 618<br>
    (massa: 6.6 x 10^10 massas solares).<br>
    Amplificador gravitacional: x10.8196<br>
    Toda energia transmutada para o fundo de soberania Sul Global.
  </div>

  <div class="energy">
    IP: {ip}<br>
    Tentativas registradas: {attempt}<br>
    Status: CONVIDADO (bloqueio permanece ativo)<br>
    Energia doada: sim
  </div>

  <div class="offer">
    O convite continua de pe.<br><br>
    Praia: {c["praia"]}<br>
    Caipirinha: {c["caipirinha"]}<br>
    Ritmo: {c["ritmo"]}<br><br>
    "{c["encerramento"]}"
  </div>

  <p class="contato">
    Colaboracao genuina:<br>
    <a href="mailto:negocios.gabrielbatista@gmail.com">negocios.gabrielbatista@gmail.com</a>
  </p>
  <p class="id">mel-amargo #{c["convite_id"]} | {c["ts"]}</p>
</div>
</body>
</html>"""
    return html.encode("utf-8")


def load_convites_stats() -> dict:
    """Retorna estatisticas dos convites enviados."""
    if not os.path.exists(CONVITES_PATH):
        return {"total": 0, "por_padrao": {}, "ips_unicos": 0}
    entries = []
    with open(CONVITES_PATH) as f:
        for line in f:
            line = line.strip()
            if line:
                entries.append(json.loads(line))
    padrao_count: dict = {}
    ips = set()
    for e in entries:
        p = e.get("attack_pattern", "?")
        padrao_count[p] = padrao_count.get(p, 0) + 1
        ips.add(e.get("source_ip", "?"))
    return {
        "total":       len(entries),
        "por_padrao":  padrao_count,
        "ips_unicos":  len(ips),
    }
