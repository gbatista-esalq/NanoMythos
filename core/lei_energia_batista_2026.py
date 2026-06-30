"""
SYNAPSE HUB v3.0 | LEI DA ENERGIA DE BATISTA 2026
Sincronia Diamante -- Salto Quantico PYM

E_B = (elasticidade_bits * coerencia_hash * pedra_da_mente) / entropia_ambiente_normalizada

Toda variavel da formula vem de medicao real do sistema, nao de simulacao:
- elasticidade_bits: entropia de Shannon real do dado (0..1)
- coerencia_hash: efeito avalanche real do SHA-256 a um bit-flip (0 ou 1)
- pedra_da_mente: estabilidade real de carga do sistema via /proc/loadavg (0..1)
- entropia_ambiente: pool de entropia real do kernel Linux via
  /proc/sys/kernel/random/entropy_avail (isolamento real, nao mistico)
"""
import hashlib
import json
import math
import os
import sqlite3

ENTROPY_AVAIL_PATH = '/proc/sys/kernel/random/entropy_avail'
LOADAVG_PATH = '/proc/loadavg'
KERNEL_ENTROPY_POOL_MAX = 4096
VAULT_OUTPUT_PATH = '/opt/synapse_vault/obsidian_graph/lei_energia_batista_2026.json'
VAULT_HISTORY_PATH = '/opt/synapse_vault/obsidian_graph/pedra_da_visao_historico.json'
VAULT_REALIDADE_PATH = '/opt/synapse_vault/obsidian_graph/joia_da_realidade.json'
VAULT_TRACES_LOG = '/opt/synapse_vault/infinity_traces.log'
VAULT_BENCHMARKS_LOG = '/opt/synapse_vault/logs/benchmarks.json'
AMAZONIA_FOCOS_PATH = os.path.join(
    os.path.dirname(__file__), 'amazonia_legal', 'data', 'focos_incendio.json'
)
MOLTBOOK_DB_PATH = os.path.join(
    os.path.dirname(__file__), 'scratch', 'moltbook_reality_thread.db'
)
RMSD_GROMACS_STEARIC_PATH = os.path.join(
    os.path.dirname(__file__), 'langmuir_project', 'phase2', 'models',
    'md_analysis', 'stearic_acid', 'rmsd_stearic.xvg'
)
COLONY_V2_LOG_PATH = '/opt/synapse_vault/quantum_world/colony_v2.jsonl'
TENDENCIA_LIMIAR_RELATIVO = 0.02


def medir_entropia_ambiente() -> int:
    with open(ENTROPY_AVAIL_PATH) as f:
        return int(f.read().strip())


def medir_elasticidade_bits(data: bytes) -> float:
    if not data:
        return 0.0
    n = len(data)
    freq = [0] * 256
    for b in data:
        freq[b] += 1
    entropy = -sum((c / n) * math.log2(c / n) for c in freq if c)
    return entropy / 8.0


def medir_coerencia_hash(data: bytes) -> float:
    if not data:
        return 0.0
    original_hash = hashlib.sha256(data).hexdigest()
    corrupted = bytearray(data)
    corrupted[0] ^= 0b00000001
    corrupted_hash = hashlib.sha256(bytes(corrupted)).hexdigest()
    return 1.0 if original_hash != corrupted_hash else 0.0


def medir_pedra_da_mente() -> float:
    with open(LOADAVG_PATH) as f:
        load1, load5, load15 = (float(x) for x in f.read().split()[:3])
    variancia = abs(load1 - load5) + abs(load5 - load15)
    return 1.0 / (1.0 + variancia)


def calcular_lei_energia_batista(data: bytes) -> dict:
    elasticidade = medir_elasticidade_bits(data)
    coerencia = medir_coerencia_hash(data)
    pedra_da_mente = medir_pedra_da_mente()
    entropia_raw = medir_entropia_ambiente()
    entropia_normalizada = max(entropia_raw / KERNEL_ENTROPY_POOL_MAX, 1e-6)

    e_b = (elasticidade * coerencia * pedra_da_mente) / entropia_normalizada

    return {
        "elasticidade_bits": round(elasticidade, 4),
        "coerencia_hash": coerencia,
        "pedra_da_mente": round(pedra_da_mente, 4),
        "entropia_ambiente_raw": entropia_raw,
        "E_B": round(e_b, 6),
    }


def gravar_relatorio_vault(relatorio: dict, output_path: str = VAULT_OUTPUT_PATH) -> str:
    with open(output_path, 'w') as f:
        json.dump(relatorio, f, indent=2)
    return output_path


def medir_serie_temporal_E_B(n_amostras: int, tamanho_amostra: int = 4096) -> list:
    """Pedra da Visao: amostra E_B real n vezes em sequencia (sem misticismo,
    apenas leituras sucessivas de entropia/loadavg/hash reais do sistema)."""
    return [
        calcular_lei_energia_batista(os.urandom(tamanho_amostra))["E_B"]
        for _ in range(n_amostras)
    ]


def prever_tendencia_E_B(serie: list) -> dict:
    """Regressao linear simples (minimos quadrados) sobre a serie de E_B.
    slope > 0 => ALTA, slope < 0 => BAIXA, slope == 0 => ESTAVEL."""
    n = len(serie)
    if n < 2:
        raise ValueError("prever_tendencia_E_B requer pelo menos 2 amostras")

    xs = list(range(n))
    media_x = sum(xs) / n
    media_y = sum(serie) / n

    cov_xy = sum((x - media_x) * (y - media_y) for x, y in zip(xs, serie))
    var_x = sum((x - media_x) ** 2 for x in xs)
    var_y = sum((y - media_y) ** 2 for y in serie)

    slope = cov_xy / var_x if var_x else 0.0

    if var_x and var_y:
        r = cov_xy / math.sqrt(var_x * var_y)
        confianca = round(r ** 2, 4)
    else:
        confianca = 1.0 if slope == 0.0 else 0.0

    limiar = abs(media_y) * TENDENCIA_LIMIAR_RELATIVO if media_y else TENDENCIA_LIMIAR_RELATIVO
    if slope > limiar:
        tendencia = "ALTA"
    elif slope < -limiar:
        tendencia = "BAIXA"
    else:
        tendencia = "ESTAVEL"
        slope = 0.0

    return {
        "slope": round(slope, 6),
        "tendencia": tendencia,
        "confianca": confianca,
    }


def gravar_historico_vault(serie: list, output_path: str = VAULT_HISTORY_PATH) -> str:
    with open(output_path, 'w') as f:
        json.dump(serie, f, indent=2)
    return output_path


def protocolo_tdd_quantico_pym(obter_corda, materializar):
    """Protocolo TDD Quantico Pym.
    RED: obter_corda() busca a fonte real; se ela nao existir, o erro real
    (FileNotFoundError, ValueError etc.) propaga sem fallback ficticio.
    GREEN: se a corda existir, materializar(corda) computa o resultado real
    a partir dela. Usado por todas as funcoes calcular_joia_da_realidade*."""
    corda = obter_corda()
    return materializar(corda)


def ler_fio_teatral_real(caminho_log: str = VAULT_TRACES_LOG) -> dict:
    """Le a ultima linha do sentinel teatral (infinity_gauntlet_sentinel.py) e
    extrai SOMENTE os campos reais (hash sha256, cpu via psutil, timestamp).
    O campo 'sovereign_power' (YottaWatts) e ficticio e e descartado aqui de proposito."""
    with open(caminho_log, 'rb') as f:
        f.seek(0, os.SEEK_END)
        pos = f.tell()
        buffer = bytearray()
        while pos > 0:
            pos -= 1
            f.seek(pos)
            char = f.read(1)
            if char == b'\n' and buffer:
                break
            buffer.extend(char)
    ultima_linha = json.loads(bytes(buffer[::-1]).decode('utf-8'))
    return {
        "reality_hash": ultima_linha.get("reality_hash"),
        "cpu_usage_total": ultima_linha.get("cpu_usage_total"),
        "timestamp": ultima_linha.get("timestamp"),
    }


def ler_amostra_amazonia_real(caminho: str = AMAZONIA_FOCOS_PATH, n_features: int = 200) -> bytes:
    """Pedra da Realidade: dados reais de focos de incendio FIRMS/NASA na Amazonia,
    nao dados aleatorios. Ver amazonia_legal/data/focos_incendio.json."""
    with open(caminho, encoding='utf-8') as f:
        dados = json.load(f)
    amostra = dados.get("features", [])[:n_features]
    return json.dumps(amostra, sort_keys=True).encode('utf-8')


def calcular_joia_da_realidade(
    caminho_amazonia: str = AMAZONIA_FOCOS_PATH, caminho_log: str = VAULT_TRACES_LOG
) -> dict:
    def obter_corda():
        return ler_amostra_amazonia_real(caminho_amazonia), ler_fio_teatral_real(caminho_log)

    def materializar(corda):
        dados_reais, fio_teatral_real = corda
        relatorio = calcular_lei_energia_batista(dados_reais)
        relatorio["fonte_dados"] = "amazonia_legal/data/focos_incendio.json (FIRMS/NASA real)"
        relatorio["fio_teatral_real"] = fio_teatral_real
        return relatorio

    return protocolo_tdd_quantico_pym(obter_corda, materializar)


def gravar_joia_da_realidade_vault(relatorio: dict, output_path: str = VAULT_REALIDADE_PATH) -> str:
    with open(output_path, 'w') as f:
        json.dump(relatorio, f, indent=2, ensure_ascii=False)
    return output_path


def ler_metricas_reais_deste_pc(caminho: str = VAULT_BENCHMARKS_LOG) -> dict:
    """Filtra /opt/synapse_vault/logs/benchmarks.json e retorna SOMENTE o registro
    com 'hardware_info' real (SISTEMA_ATUAL). Os demais perfis ('Legacy BR: ...',
    'Jetson Orin' etc.) sao tempo_real * fator_inventado e nao tem hardware_info,
    por isso sao descartados aqui de proposito."""
    with open(caminho, encoding='utf-8') as f:
        registros = json.load(f)
    reais = [r for r in registros if "hardware_info" in r]
    if not reais:
        raise ValueError("Nenhum registro com hardware_info real encontrado em benchmarks.json")
    return reais[0]


def calcular_joia_da_realidade_pc_atual(caminho: str = VAULT_BENCHMARKS_LOG) -> dict:
    def obter_corda():
        return ler_metricas_reais_deste_pc(caminho)

    def materializar(corda):
        dados = json.dumps(corda, sort_keys=True).encode('utf-8')
        relatorio = calcular_lei_energia_batista(dados)
        relatorio["fonte_dados"] = (
            "opt/synapse_vault/logs/benchmarks.json (SISTEMA_ATUAL, hardware_info real)"
        )
        relatorio["metricas_reais_pc"] = corda
        return relatorio

    return protocolo_tdd_quantico_pym(obter_corda, materializar)


def ler_serie_batista_energy_moltbook(caminho: str = MOLTBOOK_DB_PATH) -> list:
    """Pedra da Visao real: serie temporal real de E_B (batista_energy) ja
    materializada por post no Moltbook, ordenada pela ordem real de publicacao
    (created_at). sqlite3.OperationalError propaga sem fallback se o banco
    ou a tabela nao existirem nesta maquina."""
    con = sqlite3.connect(caminho)
    try:
        cur = con.execute(
            "SELECT batista_energy FROM posts ORDER BY created_at ASC"
        )
        serie = [float(row[0]) for row in cur.fetchall()]
    finally:
        con.close()
    if not serie:
        raise ValueError(f"Nenhum post com batista_energy em {caminho}")
    return serie


def calcular_joia_da_visao_moltbook(caminho: str = MOLTBOOK_DB_PATH) -> dict:
    def obter_corda():
        return ler_serie_batista_energy_moltbook(caminho)

    def materializar(corda):
        previsao = prever_tendencia_E_B(corda)
        previsao["fonte_dados"] = "scratch/moltbook_reality_thread.db (corda real, posts.batista_energy)"
        previsao["n_amostras"] = len(corda)
        return previsao

    return protocolo_tdd_quantico_pym(obter_corda, materializar)


def ler_serie_rmsd_gromacs(caminho: str = RMSD_GROMACS_STEARIC_PATH) -> list:
    """Pedra da Visao real: serie temporal real de RMSD (nm) da trajetoria
    GROMACS real de 50ns da monocamada de acido estearico (ver
    langmuir_project/phase2/models/md_analysis/stearic_acid/), ordenada
    pelo tempo real de simulacao (ps), extraida do .xvg gerado por
    `gmx rms`. FileNotFoundError propaga sem fallback se o arquivo nao
    existir nesta maquina."""
    with open(caminho, encoding='utf-8') as f:
        linhas = f.readlines()
    serie = [
        float(linha.split()[1])
        for linha in linhas
        if linha.strip() and not linha.startswith(('#', '@'))
    ]
    if not serie:
        raise ValueError(f"Nenhum dado de RMSD em {caminho}")
    return serie


def calcular_joia_da_visao_gromacs(caminho: str = RMSD_GROMACS_STEARIC_PATH) -> dict:
    def obter_corda():
        return ler_serie_rmsd_gromacs(caminho)

    def materializar(corda):
        previsao = prever_tendencia_E_B(corda)
        previsao["fonte_dados"] = (
            "langmuir_project/.../stearic_acid/rmsd_stearic.xvg "
            "(corda real, RMSD da trajetoria GROMACS de 50ns)"
        )
        previsao["n_amostras"] = len(corda)
        return previsao

    return protocolo_tdd_quantico_pym(obter_corda, materializar)


def ler_serie_vault_free_gb_formigas(caminho: str = COLONY_V2_LOG_PATH) -> list:
    """Pedra da Visao real: serie temporal real de espaco livre no vault (GB),
    medida pelas formigas Nurse da Colonia Tipo 2 a cada HEALTH_CHECK
    (core/ant_colony_v2.py), ordenada pela ordem real de execucao no log
    (colony_v2.jsonl). 'vault_free_gb' vem de medicao real de disco; os
    campos de YottaWatts/total_yw no mesmo arquivo sao teatrais e nao
    entram aqui. FileNotFoundError propaga sem fallback se o log nao
    existir nesta maquina."""
    serie = []
    with open(caminho, encoding='utf-8') as f:
        for linha in f:
            if not linha.strip():
                continue
            entrada = json.loads(linha)
            if entrada.get('action') == 'HEALTH_CHECK' and 'vault_free_gb' in entrada:
                serie.append(entrada['vault_free_gb'])
    if not serie:
        raise ValueError(f"Nenhum HEALTH_CHECK com vault_free_gb em {caminho}")
    return serie


def calcular_joia_da_visao_formigas(caminho: str = COLONY_V2_LOG_PATH) -> dict:
    def obter_corda():
        return ler_serie_vault_free_gb_formigas(caminho)

    def materializar(corda):
        previsao = prever_tendencia_E_B(corda)
        previsao["fonte_dados"] = (
            "opt/synapse_vault/quantum_world/colony_v2.jsonl "
            "(corda real, vault_free_gb dos HEALTH_CHECK das formigas Nurse Tipo 2)"
        )
        previsao["n_amostras"] = len(corda)
        return previsao

    return protocolo_tdd_quantico_pym(obter_corda, materializar)


if __name__ == "__main__":
    relatorio = calcular_lei_energia_batista(os.urandom(4096))
    print("LEI DA ENERGIA DE BATISTA 2026")
    for k, v in relatorio.items():
        print(f"  {k.upper()}: {v}")

    caminho = gravar_relatorio_vault(relatorio)
    print(f"\nRelatorio gravado no vault: {caminho}")

    print("\nPEDRA DA VISAO: previsao de tendencia (5 amostras reais)")
    serie = medir_serie_temporal_E_B(n_amostras=5)
    previsao = prever_tendencia_E_B(serie)
    print(f"  SERIE E_B: {serie}")
    for k, v in previsao.items():
        print(f"  {k.upper()}: {v}")

    caminho_historico = gravar_historico_vault(serie)
    print(f"\nHistorico gravado no vault: {caminho_historico}")

    print("\nPEDRA DA REALIDADE: dados reais FIRMS/NASA da Amazonia")
    relatorio_realidade = calcular_joia_da_realidade()
    for k, v in relatorio_realidade.items():
        print(f"  {k.upper()}: {v}")

    caminho_realidade = gravar_joia_da_realidade_vault(relatorio_realidade)
    print(f"\nJoia da Realidade gravada no vault: {caminho_realidade}")
