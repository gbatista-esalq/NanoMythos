import os
import re
import json

# 📊 SIGMA MONITOR (σ): CALCULATING GRAPH DENSITY
DOCS_DIR = "/home/synapseagtech/Área de Trabalho/SYNAPSE AGTECH/docs"
VAULT_DIR = "/opt/synapse_vault/obsidian_graph"

def calculate_sigma():
    print("📊 [SIGMA MONITOR] Calculando densidade do grafo de conhecimento...")
    
    files = [f for f in os.listdir(DOCS_DIR) if f.endswith('.md')]
    nodes = len(files)
    links = 0
    
    link_pattern = re.compile(r'\[\[(.*?)\]\]')
    
    for filename in files:
        with open(os.path.join(DOCS_DIR, filename), 'r') as f:
            content = f.read()
            found_links = link_pattern.findall(content)
            links += len(found_links)
            
    # Densidade de Grafo Não-Direcionado: D = 2L / (N * (N-1))
    if nodes > 1:
        density = (2 * links) / (nodes * (nodes - 1))
    else:
        density = 0
        
    sigma_report = {
        "nodes": nodes,
        "links": links,
        "sigma_density": f"{density:.4f}",
        "status": "CONECTADO" if density > 0.05 else "FRAGMENTADO",
        "timestamp": os.popen('date').read().strip()
    }
    
    output_path = os.path.join(VAULT_DIR, "sigma_density.json")
    with open(output_path, 'w') as f:
        json.dump(sigma_report, f, indent=2)
        
    print(f"✅ σ={density:.4f} | Nodes: {nodes} | Links: {links}")
    return sigma_report

if __name__ == "__main__":
    calculate_sigma()
