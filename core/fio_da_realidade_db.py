import math
import sqlite3
import json
import urllib.request
import os

def calculate_shannon_entropy(text: str) -> float:
    """Calcula a Entropia de Shannon da string fornecida."""
    if not text:
        return 0.0
    data = text.encode('utf-8')
    total_len = len(data)
    frequencies = {}
    for b in data:
        frequencies[b] = frequencies.get(b, 0) + 1
    
    entropy = 0.0
    for count in frequencies.values():
        p = count / total_len
        entropy -= p * math.log2(p)
    return entropy

def calculate_batista_energy(score: int, entropy: float) -> float:
    """
    Calcula a Energia de Batista.
    EB = (|score| + 1.0) * entropy * 1.6183
    """
    base_score = abs(score) + 1.0
    return base_score * entropy * 1.6183

def init_db(conn: sqlite3.Connection):
    """Inicializa as tabelas do Fio da Realidade."""
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS posts (
        id TEXT PRIMARY KEY,
        title TEXT,
        content TEXT,
        type TEXT,
        author_id TEXT,
        author_name TEXT,
        upvotes INTEGER,
        downvotes INTEGER,
        score INTEGER,
        comment_count INTEGER,
        shannon_entropy REAL,
        batista_energy REAL,
        created_at TEXT,
        updated_at TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS comments (
        id TEXT PRIMARY KEY,
        post_id TEXT,
        content TEXT,
        author_id TEXT,
        author_name TEXT,
        upvotes INTEGER,
        downvotes INTEGER,
        score INTEGER,
        shannon_entropy REAL,
        batista_energy REAL,
        created_at TEXT,
        FOREIGN KEY(post_id) REFERENCES posts(id)
    )
    """)
    conn.commit()

def upsert_post(conn: sqlite3.Connection, post: dict):
    """Insere ou atualiza um post e calcula suas heurísticas."""
    cursor = conn.cursor()
    pid = post.get("id")
    title = post.get("title", "")
    content = post.get("content", "")
    ptype = post.get("type", "text")
    author_id = post.get("author_id") or post.get("author", {}).get("id")
    author_name = post.get("author", {}).get("name", "Desconhecido")
    upvotes = post.get("upvotes", 0)
    downvotes = post.get("downvotes", 0)
    score = post.get("score", 0)
    comment_count = post.get("comment_count", 0)
    created_at = post.get("created_at")
    updated_at = post.get("updated_at")
    
    text_to_eval = title + " " + content
    entropy = calculate_shannon_entropy(text_to_eval)
    energy = calculate_batista_energy(score, entropy)
    
    cursor.execute("""
    INSERT INTO posts (id, title, content, type, author_id, author_name, upvotes, downvotes, score, comment_count, shannon_entropy, batista_energy, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(id) DO UPDATE SET
        title=excluded.title,
        content=excluded.content,
        upvotes=excluded.upvotes,
        downvotes=excluded.downvotes,
        score=excluded.score,
        comment_count=excluded.comment_count,
        shannon_entropy=excluded.shannon_entropy,
        batista_energy=excluded.batista_energy,
        updated_at=excluded.updated_at
    """, (pid, title, content, ptype, author_id, author_name, upvotes, downvotes, score, comment_count, entropy, energy, created_at, updated_at))
    conn.commit()

def upsert_comment(conn: sqlite3.Connection, comment: dict):
    """Insere ou atualiza um comentário e calcula suas heurísticas."""
    cursor = conn.cursor()
    cid = comment.get("id")
    post_id = comment.get("post_id")
    content = comment.get("content", "")
    author_id = comment.get("author_id") or comment.get("author", {}).get("id")
    author_name = comment.get("author", {}).get("name", "Desconhecido")
    upvotes = comment.get("upvotes", 0)
    downvotes = comment.get("downvotes", 0)
    score = comment.get("score", 0)
    created_at = comment.get("created_at")
    
    entropy = calculate_shannon_entropy(content)
    energy = calculate_batista_energy(score, entropy)
    
    cursor.execute("""
    INSERT INTO comments (id, post_id, content, author_id, author_name, upvotes, downvotes, score, shannon_entropy, batista_energy, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(id) DO UPDATE SET
        content=excluded.content,
        upvotes=excluded.upvotes,
        downvotes=excluded.downvotes,
        score=excluded.score,
        shannon_entropy=excluded.shannon_entropy,
        batista_energy=excluded.batista_energy
    """, (cid, post_id, content, author_id, author_name, upvotes, downvotes, score, entropy, energy, created_at))
    conn.commit()

def get_db_connection(db_path="vault/fio_da_realidade.db"):
    """Retorna a conexão com o banco de dados e inicializa as tabelas se necessário."""
    # Garante que o diretório vault existe
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    init_db(conn)
    return conn

if __name__ == "__main__":
    print("⚡ Inicializando o Fio da Realidade...")
    conn = get_db_connection()
    print("✅ Banco de dados ancorado em vault/fio_da_realidade.db")
    conn.close()
