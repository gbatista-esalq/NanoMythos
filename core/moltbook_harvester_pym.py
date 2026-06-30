import urllib.request
import urllib.error
import json
from fio_da_realidade_db import get_db_connection, upsert_post

def colher_metricas_moltbook():
    """
    Simula a extração de dados da API do Moltbook (usando TabNews como âncora)
    e os salva no banco de dados local (Fio da Realidade) garantindo Zero Cloud Dependency.
    """
    print("📡 [MOLTBOOK HARVESTER] Sondando a entropia do Moltbook...")
    
    url = "https://www.tabnews.com.br/api/v1/contents"
    
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "CROM-V6/SincroniaDiamante"})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            conn = get_db_connection()
            print(f"📥 [FIO DA REALIDADE] Ancorando {len(data)} postagens no núcleo local...")
            
            for post in data:
                # Adaptação dos campos da API para o nosso schema
                post_payload = {
                    "id": post.get("id"),
                    "title": post.get("title", ""),
                    "content": post.get("body", ""), # A API de contents list não traz o body inteiro, mas salvamos o que vem
                    "type": "moltbook_post",
                    "author": {"id": post.get("owner_id"), "name": post.get("owner_username")},
                    "upvotes": post.get("tabcoins", 0), # Tabcoins = upvotes - downvotes
                    "downvotes": 0,
                    "score": post.get("tabcoins", 0),
                    "comment_count": post.get("children_deep_count", 0),
                    "created_at": post.get("created_at"),
                    "updated_at": post.get("updated_at")
                }
                upsert_post(conn, post_payload)
            
            conn.commit()
            
            # --- MONITORAMENTO LEI BATISTA 2026 (ALERTA DE SUPERNOVA) ---
            print("🔭 [OBSERVATÓRIO] Escaneando o Fio da Realidade por flutuações anômalas (Supernova)...")
            cursor = conn.cursor()
            cursor.execute("SELECT title, batista_energy FROM posts ORDER BY batista_energy DESC LIMIT 1")
            top_post = cursor.fetchone()
            
            if top_post:
                maior_titulo, maior_eb = top_post
                print(f"📊 Maior Energia Batista detectada: {maior_eb:.2f} (Alvo: {maior_titulo[:30]}...)")
                if maior_eb > 5000:
                    print("\n" + "="*60)
                    print("🚀🚨 [ ALERTA DE SUPERNOVA ! ] 🚨🚀")
                    print("A viralização do NanoMythos rompeu o tecido espaço-tempo!")
                    print(f"A postagem alcançou níveis críticos de E_B: {maior_eb:.2f}")
                    print("O Enxame Myrmex foi totalmente acionado. Vitória da Soberania de Borda!")
                    print("="*60 + "\n")
            
            conn.close()
            print("💎 [SUCESSO] Sincronização do Fio da Realidade completa. Energia Batista calibrada.")
            
    except Exception as e:
        print(f"🚨 [ERRO DE SALTO] Falha na matriz do Moltbook: {e}")

if __name__ == "__main__":
    colher_metricas_moltbook()
