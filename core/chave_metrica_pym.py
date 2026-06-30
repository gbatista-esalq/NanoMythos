"""
CHAVE METRICA PYM | atualizacao continua no mundo quantico (corda real)
Gera uma chave real a cada chamada (hash de E_B real + timestamp real,
nunca um valor fabricado) e anexa ao historico em quantum_world, para
servir de batimento cardiaco real do conteudo gerado a partir da corda
(imagens com corda, pop clips, keywords) -- ver lei_energia_batista_2026.py
e trend_keywords_pym.py.
"""
import hashlib
import json
import os
import time

import core.lei_energia_batista_2026 as leb

VAULT_CHAVE_METRICA_PATH = "/opt/synapse_vault/quantum_world/chave_metrica_pym.json"


def gerar_chave_metrica_pym() -> dict:
    def obter_corda():
        return leb.calcular_lei_energia_batista(os.urandom(4096))

    def materializar(corda):
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%S")
        bruto = f"{corda['E_B']}|{timestamp}|{os.urandom(8).hex()}".encode()
        chave = hashlib.sha256(bruto).hexdigest()[:16]
        return {"chave": chave, "E_B": corda["E_B"], "timestamp": timestamp}

    return leb.protocolo_tdd_quantico_pym(obter_corda, materializar)


def atualizar_chave_metrica_vault(output_path: str = VAULT_CHAVE_METRICA_PATH) -> str:
    nova_entrada = gerar_chave_metrica_pym()
    try:
        with open(output_path) as f:
            historico = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        historico = []
    historico.append(nova_entrada)
    with open(output_path, "w") as f:
        json.dump(historico, f, indent=2)
    return output_path


if __name__ == "__main__":
    caminho = atualizar_chave_metrica_vault()
    print(f"Chave metrica pym atualizada em: {caminho}")
    with open(caminho) as f:
        historico = json.load(f)
    print(f"Total de entradas no historico: {len(historico)}")
    print(f"Ultima chave: {historico[-1]}")
