import pytest
import os
import sqlite3
import sys

# Adiciona o diretório 'core' ao path para resolver os imports internos do Salto Quântico Pym
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "core"))

from core.fio_da_realidade_db import upsert_post, get_db_connection, calculate_batista_energy
from core.salto_dimensional_pym import realizar_salto_dimensional

DB_PATH = "vault/fio_da_realidade.db"

@pytest.fixture
def db_conn():
    # Setup test DB
    conn = get_db_connection(DB_PATH)
    yield conn
    # Teardown (limpar os dados gerados pelo ataque DDoS para não poluir o DB real)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM posts WHERE id LIKE 'stress_post_%'")
    conn.commit()
    conn.close()

def test_ddos_entropia(db_conn):
    """Cenário 1: Mass Ingestion. Injetar 1000 posts simultâneos para testar estabilidade do Fio da Realidade."""
    for i in range(1000):
        post = {
            "id": f"stress_post_{i}",
            "title": f"DDoS Post {i}",
            "content": "Hack the planet. Teste de carga com entropia massiva.",
            "score": i
        }
        upsert_post(db_conn, post)
    
    cursor = db_conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM posts WHERE id LIKE 'stress_post_%'")
    count = cursor.fetchone()[0]
    assert count == 1000

def test_toxic_payload_anomaly():
    """Cenário 2: Payloads Tóxicos. Injetar entropia negativa e score extremo."""
    # A entropia de Shannon em texto normal é positiva, mas um ataque poderia forçar
    # parâmetros via interface. O teste garante que o motor matemático absorve sem crachar.
    energy = calculate_batista_energy(score=999999999, entropy=-50.0)
    assert energy < 0

def test_pym_jump_spam():
    """Cenário 3: Colisão de Saltos. Disparar 50 saltos seguidos para tentar corromper o Ledger e as Chaves Kyber."""
    for i in range(50):
        realizar_salto_dimensional()
        
    # Verificar se o artefato JSON de telemetria resistiu
    assert os.path.exists("vault/salto_dimensional_11_11.json")
    
    # O Ledger Mestre do auditor deve permanecer íntegro
    assert os.path.exists("/opt/synapse_vault/sovereign_ledger.md")
