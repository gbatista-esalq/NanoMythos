import os
import shutil
import json
from datetime import datetime

BRAIN_BASE = os.path.expanduser("~/.gemini/antigravity/brain")
OBSIDIAN = "/opt/synapse_vault/obsidian_graph"
SYNC_MD = os.path.join(OBSIDIAN, "sync.md")

def timestamp_to_date(ts_ms):
    try:
        return datetime.fromtimestamp(ts_ms / 1000).strftime("%Y-%m-%d %H:%M")
    except Exception:
        return "?"

def sync_session(session_id, session_path):
    docs_imported = []
    for fname in os.listdir(session_path):
        if not fname.endswith(".md") or fname.endswith((".resolved", ".metadata.json")):
            continue
        src = os.path.join(session_path, fname)
        dest_name = f"brain_{session_id[:8]}_{fname}"
        dest = os.path.join(OBSIDIAN, dest_name)
        src_mtime = os.path.getmtime(src)
        if os.path.exists(dest) and os.path.getmtime(dest) >= src_mtime:
            continue
        with open(src, "r", errors="replace") as f:
            content = f.read()
        frontmatter = (
            f"---\nnode: SYNAPSE-HUB\nstatus: DIAMANTE\n"
            f"session: {session_id}\nsource: gemini_brain\n"
            f"synced: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
            f"tags: ['brain', 'sessao', 'contexto']\n---\n\n"
        )
        with open(dest, "w") as f:
            f.write(frontmatter + content)
        docs_imported.append(fname)
        print(f"  ✅ {fname} → {dest_name}")
    return docs_imported

def update_sync_index(sessions_synced):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        "---",
        "node: SYNAPSE-HUB",
        "status: DIAMANTE",
        "tags: ['sync', 'brain', 'obsidian']",
        "---",
        "",
        "# 🔄 Brain → Obsidian Sync Index",
        f"**Última atualização:** {now}",
        "",
        "| Sessão | Documentos | Última Sync |",
        "|--------|-----------|-------------|",
    ]
    for s in sessions_synced:
        lines.append(f"| `{s['id'][:8]}` | {s['count']} docs | {s['time']} |")
    lines.append("")
    lines.append("*Gerado automaticamente por sync_brain_to_obsidian.py*")
    with open(SYNC_MD, "w") as f:
        f.write("\n".join(lines) + "\n")

if __name__ == "__main__":
    if not os.path.exists(BRAIN_BASE):
        print("Brain path não encontrado.")
        exit(0)

    sessions_synced = []
    for session_id in os.listdir(BRAIN_BASE):
        session_path = os.path.join(BRAIN_BASE, session_id)
        if not os.path.isdir(session_path):
            continue
        docs = sync_session(session_id, session_path)
        if docs:
            sessions_synced.append({
                "id": session_id,
                "count": len(docs),
                "time": datetime.now().strftime("%Y-%m-%d %H:%M")
            })

    update_sync_index([
        {"id": sid, "count": len(os.listdir(os.path.join(BRAIN_BASE, sid))), "time": datetime.now().strftime("%Y-%m-%d %H:%M")}
        for sid in os.listdir(BRAIN_BASE)
        if os.path.isdir(os.path.join(BRAIN_BASE, sid))
    ])
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] Sync completo.")
