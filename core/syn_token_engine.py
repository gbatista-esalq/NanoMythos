import sqlite3
import hashlib
import json
import time
import os

DB_PATH = "/opt/synapse_vault/chronicles_chain.db"

class SynTokenEngine:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()
        self._initialize_ledger()

    def _initialize_ledger(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS blocks (
                idx INTEGER PRIMARY KEY,
                timestamp TEXT,
                data TEXT,
                prev_hash TEXT,
                hash TEXT
            )
        """)
        self.conn.commit()
        
        # Genesis Block check
        self.cursor.execute("SELECT COUNT(*) FROM blocks")
        if self.cursor.fetchone()[0] == 0:
            self._mint_block("GENESIS", "Sovereign Initial State", 0, "0")

    def _calculate_hash(self, idx, timestamp, data, prev_hash):
        block_string = f"{idx}{timestamp}{data}{prev_hash}".encode()
        return hashlib.sha256(block_string).hexdigest()

    def _mint_block(self, minter, action, amount, prev_hash=None):
        if prev_hash is None:
            self.cursor.execute("SELECT hash FROM blocks ORDER BY idx DESC LIMIT 1")
            prev_hash = self.cursor.fetchone()[0]
        
        self.cursor.execute("SELECT COUNT(*) FROM blocks")
        idx = self.cursor.fetchone()[0]
        timestamp = time.ctime()
        
        data = json.dumps({
            "minter": minter,
            "action": action,
            "amount": amount
        })
        
        block_hash = self._calculate_hash(idx, timestamp, data, prev_hash)
        
        self.cursor.execute("INSERT INTO blocks (idx, timestamp, data, prev_hash, hash) VALUES (?, ?, ?, ?, ?)",
                           (idx, timestamp, data, prev_hash, block_hash))
        self.conn.commit()
        print(f"💎 [SYN MINT] Bloco #{idx} selado. Ação: {action} | +{amount} SYN")

    def mint_contribution(self, action, amount):
        """Interface pública para mintar contribuições verificadas."""
        self._mint_block("Gabriel", action, amount)

    def get_balance(self, minter="Gabriel"):
        self.cursor.execute("SELECT data FROM blocks")
        rows = self.cursor.fetchall()
        total = 0
        for row in rows:
            data = json.loads(row[0])
            if data.get("minter") == minter:
                total += data.get("amount", 0)
        return total

if __name__ == "__main__":
    engine = SynTokenEngine()
    # Teste de Mintagem inicial se estiver vazio além do genesis
    print(f"💰 Saldo Atual: {engine.get_balance()} SYN")
