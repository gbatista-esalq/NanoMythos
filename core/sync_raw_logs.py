import os
import shutil
from datetime import datetime

# 🌌 SYNC RAW LOGS: CONECTANDO O CÉREBRO AO VAULT
# Extração direta do fluxo de consciência (overview.txt) para o Obsidian.

BRAIN_BASE = os.path.expanduser("~/.gemini/antigravity/brain")
OBSIDIAN = "/opt/synapse_vault/obsidian_graph"

def sync_raw_logs():
    print("🌌 [SISTEMA PYM] Sincronizando fluxo de consciência raw...")
    for session_id in os.listdir(BRAIN_BASE):
        session_path = os.path.join(BRAIN_BASE, session_id)
        log_file = os.path.join(session_path, ".system_generated", "logs", "overview.txt")
        
        if os.path.exists(log_file):
            dest_name = f"RAW_LOG_{session_id[:8]}.md"
            dest = os.path.join(OBSIDIAN, dest_name)
            
            with open(log_file, "r", errors="replace") as f:
                content = f.read()
            
            frontmatter = (
                f"---\nnode: SYNAPSE-HUB\nstatus: DIAMANTE\n"
                f"session: {session_id}\nsource: gemini_raw_logs\n"
                f"synced: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
                f"tags: ['raw_log', 'consciencia', 'vault']\n---\n\n"
                f"# 🧠 FLUXO DE CONSCIÊNCIA RAW: {session_id[:8]}\n\n"
            )
            
            with open(dest, "w") as f:
                f.write(frontmatter + content)
            print(f"  ✅ Raw Log {session_id[:8]} sincronizado.")

if __name__ == "__main__":
    sync_raw_logs()
