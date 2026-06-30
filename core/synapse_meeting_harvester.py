import os
import time
import json
import datetime
import wave
import struct
import math
from pathlib import Path
from google import genai
from google.genai import types

# Configurações
AUDIO_DIR = "/tmp/synapse_audio_harvest"
VAULT_MEETING_DIR = "/opt/synapse_vault/meeting_logs"
REASONING_GRAPH_PATH = "/opt/synapse_vault/obsidian_graph/reasoning_graph.json"
MODEL_NAME = "gemini-2.5-flash"
RMS_THRESHOLD = int(os.getenv("RMS_THRESHOLD", 500))

# Tenta carregar a API KEY do ambiente
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    # Tenta ler de múltiplos locais
    env_locations = [
        os.path.join(os.getcwd(), ".env"),
        "/home/synapseagtech/.synapse_vault.env",
        "/opt/synapse_vault/.env"
    ]
    for loc in env_locations:
        if os.path.exists(loc):
            with open(loc, 'r') as f:
                for line in f:
                    clean_line = line.strip()
                    if clean_line.startswith("#"):
                        continue
                    if "GEMINI_API_KEY" in clean_line and "=" in clean_line:
                        parts = clean_line.split('=', 1)
                        key_candidate = parts[1].strip().replace("'", "").replace('"', '')
                        if key_candidate and key_candidate not in ["your_key_here", "sua_chave"]:
                            api_key = key_candidate
                            break
        if api_key and api_key != "your_key_here":
            break
        else:
            api_key = None

if not api_key:
    print("❌ Erro: GEMINI_API_KEY não encontrada.")
    exit(1)

# Inicializa o cliente do novo SDK google-genai
client = genai.Client(api_key=api_key)

def get_audio_rms(file_path):
    """Calcula a amplitude RMS do arquivo WAV para detectar silêncio/ruído."""
    try:
        if not os.path.exists(file_path):
            return 0
        with wave.open(str(file_path), 'rb') as w:
            width = w.getsampwidth()
            nframes = w.getnframes()
            if nframes == 0:
                return 0
            frames = w.readframes(nframes)
            
            # Tenta usar audioop se disponível
            try:
                import audioop
                return audioop.rms(frames, width)
            except ImportError:
                # Fallback para cálculo manual robusto
                if width == 2:
                    fmt = f"{nframes}h"
                    samples = struct.unpack(fmt, frames)
                elif width == 1:
                    fmt = f"{nframes}B"
                    samples = [s - 128 for s in struct.unpack(fmt, frames)]
                else:
                    return 1000  # Fallback genérico para larguras incomuns
                
                sum_squares = sum(s * s for s in samples)
                return math.sqrt(sum_squares / len(samples))
    except Exception as e:
        print(f"⚠️ Erro ao calcular RMS de {file_path}: {e}")
        return 0

def process_audio_chunk(file_path):
    print(f"🧠 Processando chunk: {file_path.name}")
    
    try:
        # Upload do arquivo usando o novo SDK
        audio_file = client.files.upload(file=str(file_path))
        
        # Aguarda o processamento do arquivo
        while audio_file.state.name == "PROCESSING":
            time.sleep(1)
            audio_file = client.files.get(name=audio_file.name)
            
        if audio_file.state.name == "FAILED":
            print(f"❌ Falha no processamento do arquivo {file_path.name}")
            return None

        prompt = """
        Atue como o Synapse Meeting Harvester. Analise este trecho de áudio de uma reunião em tempo real.
        Extraia:
        1. Participantes (se identificáveis).
        2. Tópicos principais discutidos.
        3. Ideias Sinápticas: Conceitos-chave que devem ser registrados como 'nós'.
        4. Action Items: Tarefas ou decisões tomadas.
        
        Formate a saída em JSON estrito com a seguinte estrutura:
        {
            "metadata": {"participants": [], "tone": "", "duration": "30s"},
            "topics": [],
            "synaptic_nodes": [{"id": "", "label": "", "connection": ""}],
            "actions": []
        }
        """
        
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[prompt, audio_file]
        )
        
        # Remove o arquivo do servidor do Gemini após o uso
        client.files.delete(name=audio_file.name)
        
        return response.text
    except Exception as e:
        print(f"⚠️ Erro ao processar chunk: {e}")
        return None

def update_vault(insight_json):
    try:
        data = json.loads(insight_json.strip('```json').strip('```'))
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(VAULT_MEETING_DIR, f"live_insights_{timestamp}.md")
        
        if not os.path.exists(VAULT_MEETING_DIR):
            os.makedirs(VAULT_MEETING_DIR)
            
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write(f"---\ntype: meeting_insight\ntimestamp: {timestamp}\n---\n\n")
            f.write(f"# 🎙️ INSIGHT DE REUNIÃO (REAL-TIME)\n\n")
            f.write(f"## 👥 PARTICIPANTES\n{', '.join(data['metadata']['participants']) if data['metadata']['participants'] else 'Não identificados'}\n\n")
            f.write(f"## 📌 TÓPICOS\n")
            for topic in data['topics']:
                f.write(f"- {topic}\n")
            f.write(f"\n## 🧬 NÓS SINÁPTICOS\n")
            for node in data['synaptic_nodes']:
                f.write(f"- **{node['label']}**: {node['connection']}\n")
            f.write(f"\n## ✅ AÇÕES\n")
            for action in data['actions']:
                f.write(f"- [ ] {action}\n")
                
        print(f"✅ Insight persistido no Vault: {log_file}")
        return data
    except Exception as e:
        print(f"⚠️ Erro ao persistir insight: {e}")
        return None

def update_graph(data):
    if not os.path.exists(REASONING_GRAPH_PATH):
        return
        
    try:
        with open(REASONING_GRAPH_PATH, 'r') as f:
            graph = json.load(f)
            
        for node in data.get('synaptic_nodes', []):
            graph['nodes'].append({
                "id": f"meeting_{node['id']}_{int(time.time())}",
                "label": node['label'],
                "type": "meeting_idea",
                "timestamp": datetime.datetime.now().isoformat()
            })
            
        with open(REASONING_GRAPH_PATH, 'w') as f:
            json.dump(graph, f, indent=2)
        print("✅ Grafo de raciocínio atualizado com novas ideias.")
    except Exception as e:
        print(f"⚠️ Erro ao atualizar grafo: {e}")

def main():
    print("🚀 Synapse Meeting Harvester Iniciado...")
    print(f"📡 Monitorando diretório: {AUDIO_DIR}")
    print(f"🎚️ Filtro RMS ativo (Limiar: {RMS_THRESHOLD})")
    processed_files = set()
    
    # Garante que o diretório de áudio exista
    os.makedirs(AUDIO_DIR, exist_ok=True)
    
    while True:
        files = sorted(Path(AUDIO_DIR).glob("*.wav"))
        for file in files:
            try:
                if file not in processed_files:
                    if not file.exists():
                        continue
                    size1 = file.stat().st_size
                    time.sleep(2)
                    if not file.exists():
                        continue
                    size2 = file.stat().st_size
                    
                    if size1 == size2 and size1 > 0:
                        # Calcula a amplitude RMS antes de prosseguir
                        rms = get_audio_rms(file)
                        if rms < RMS_THRESHOLD:
                            print(f"🔇 Silêncio ou ruído detectado em {file.name} (RMS: {rms:.1f} < {RMS_THRESHOLD}). Ignorando chunk.")
                        else:
                            print(f"🔊 Áudio ativo detectado em {file.name} (RMS: {rms:.1f} >= {RMS_THRESHOLD}). Enviando para a API...")
                            insight = process_audio_chunk(file)
                            if insight:
                                data = update_vault(insight)
                                if data:
                                    update_graph(data)
                        processed_files.add(file)
            except Exception as e:
                print(f"⚠️ Erro ao processar arquivo {file.name}: {e}")
        
        time.sleep(5)

if __name__ == "__main__":
    main()
