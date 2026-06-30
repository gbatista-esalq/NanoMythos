import os

def inject_metadata(directory, tags):
    for filename in os.listdir(directory):
        if filename.endswith(".md"):
            path = os.path.join(directory, filename)
            with open(path, 'r') as f:
                content = f.read()
            
            if not content.startswith("---"):
                yaml = "---\n"
                yaml += f"node: SYNAPSE-HUB\n"
                yaml += f"status: DIAMANTE\n"
                yaml += f"tags: {tags}\n"
                yaml += "---\n\n"
                
                with open(path, 'w') as f:
                    f.write(yaml + content)
                print(f"✅ Metadados injetados em: {filename}")

if __name__ == "__main__":
    inject_metadata("/home/synapseagtech/Área de Trabalho/SYNAPSE AGTECH/docs", "['soberania', 'biotech', 'triarquia']")
    inject_metadata("/opt/synapse_vault/obsidian_graph", "['telemetria', 'auditoria', 'vault']")
