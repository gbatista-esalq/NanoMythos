import sqlite3
import pytest
from core.fio_da_realidade_db import calculate_shannon_entropy, calculate_batista_energy, init_db, upsert_post, upsert_comment

def test_calculate_shannon_entropy_empty():
    assert calculate_shannon_entropy("") == 0.0
    assert calculate_shannon_entropy(None) == 0.0

def test_calculate_shannon_entropy_homogeneous():
    assert calculate_shannon_entropy("AAAAAA") == 0.0

def test_calculate_shannon_entropy_random():
    # Uma string mais complexa deve ter entropia > 0
    entropy = calculate_shannon_entropy("A random string with varying characters!")
    assert entropy > 0.0

def test_calculate_batista_energy():
    entropy = 2.0
    score = 10
    # base_score = 10 + 1.0 = 11.0
    # EB = 11.0 * 2.0 * 1.6183 = 35.6026
    energy = calculate_batista_energy(score, entropy)
    assert abs(energy - 35.6026) < 0.0001

def test_calculate_batista_energy_negative_score():
    entropy = 1.5
    score = -5
    # base_score = |-5| + 1.0 = 6.0
    # EB = 6.0 * 1.5 * 1.6183 = 14.5647
    energy = calculate_batista_energy(score, entropy)
    assert abs(energy - 14.5647) < 0.0001

@pytest.fixture
def db_conn():
    conn = sqlite3.connect(":memory:")
    init_db(conn)
    yield conn
    conn.close()

def test_database_schema(db_conn):
    cursor = db_conn.cursor()
    # Verifica se as tabelas foram criadas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    assert "posts" in tables
    assert "comments" in tables

def test_upsert_post(db_conn):
    post = {
        "id": "post_1",
        "title": "Quantum Post",
        "content": "Test content for reality thread.",
        "type": "text",
        "author": {"id": "user_1", "name": "Eniripsa"},
        "score": 42
    }
    upsert_post(db_conn, post)
    
    cursor = db_conn.cursor()
    cursor.execute("SELECT title, batista_energy FROM posts WHERE id='post_1'")
    row = cursor.fetchone()
    assert row is not None
    assert row[0] == "Quantum Post"
    assert row[1] > 0.0

def test_upsert_comment(db_conn):
    # Primeiro, cria o post para respeitar a chave estrangeira
    post = {"id": "post_1", "title": "Quantum Post"}
    upsert_post(db_conn, post)
    
    comment = {
        "id": "comment_1",
        "post_id": "post_1",
        "content": "A very insightful comment.",
        "author": {"id": "user_2", "name": "Sentinel"},
        "score": 15
    }
    upsert_comment(db_conn, comment)
    
    cursor = db_conn.cursor()
    cursor.execute("SELECT content, shannon_entropy FROM comments WHERE id='comment_1'")
    row = cursor.fetchone()
    assert row is not None
    assert row[0] == "A very insightful comment."
    assert row[1] > 0.0
