import os
import re
import json

class TesseractLinkValidator:
    def __init__(self):
        self.vault_path = "/opt/synapse_vault/obsidian_graph"
        self.links_map = {}

    def scan_spatial_entanglement(self):
        print("🌌 ATIVANDO TESSERACT: Mapeando Emaranhamento do Grafo Obsidian...")
        
        md_files = [f for f in os.listdir(self.vault_path) if f.endswith('.md')]
        total_links = 0
        
        for filename in md_files:
            path = os.path.join(self.vault_path, filename)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Busca por links estilo [[Link]]
                links = re.findall(r'\[\[(.*?)\]\]', content)
                self.links_map[filename] = links
                total_links += len(links)

        # Métrica de Densidade Espacial (Média de links por nota)
        density = total_links / len(md_files) if md_files else 0
        
        print(f">> Notas Mapeadas: {len(md_files)}")
        print(f">> Conexões (Emaranhamento): {total_links}")
        print(f">> Densidade Espacial: {density:.2f} links/nota")
        
        status = "STABLE (TESSERACT_SYNC)" if density > 1.0 else "FRAGMENTED"
        
        return {
            "total_nodes": len(md_files),
            "total_edges": total_links,
            "spatial_density": f"{density:.2f}",
            "graph_status": status,
            "quantum_sync_level": "MAXIMUM" if status == "STABLE (TESSERACT_SYNC)" else "LOW"
        }

if __name__ == "__main__":
    validator = TesseractLinkValidator()
    results = validator.scan_spatial_entanglement()
    
    output_path = "/opt/synapse_vault/obsidian_graph/tesseract_spatial_map.json"
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✨ Mapa Espacial Tesseract selado. Status do Grafo: {results['graph_status']}")
