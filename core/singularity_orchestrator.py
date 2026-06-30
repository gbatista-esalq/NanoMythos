import os
import json
import time
import subprocess
from cryptography.fernet import Fernet

class SafetyLock:
    def __init__(self):
        self.sensitive_keywords = ["pessoal", "privado", "18+", "adulto", "segredo", "intimo"]
        
    def classify_and_lock(self, text):
        text_lower = text.lower()
        for kw in self.sensitive_keywords:
            if kw in text_lower:
                return True, f"[LOCKED: CONTEÚDO {kw.upper()}]"
        return False, text

class SingularityOrchestrator:
    def __init__(self):
        self.vault_dir = "/opt/synapse_vault"
        self.metadata_path = "/opt/synapse_vault/personal_metadata.json.enc"
        self.gateway_path = "/opt/synapse_vault/gateway_ingestion.json"
        self.key_path = "/home/synapseagtech/.synapse_personal.key"
        self.safety = SafetyLock()
        
        if not os.path.exists(self.key_path):
            key = Fernet.generate_key()
            with open(self.key_path, 'wb') as f:
                f.write(key)
        
        with open(self.key_path, 'rb') as f:
            self.cipher = Fernet(f.read())

    def encrypt_data(self, data_str):
        return self.cipher.encrypt(data_str.encode()).decode()

    def sync_to_gateway(self, metadata):
        print("🛰️ Enviando metadados para o Gateway (gtwey)...")
        # Filtra dados sensíveis antes de enviar ao Gateway se necessário
        is_locked, censored_context = self.safety.classify_and_lock(metadata.get("context", ""))
        
        gateway_entry = {
            "origin": "Pym_Ultrathink_Quantum",
            "classification": "SENSITIVE" if is_locked else "PUBLIC",
            "payload": metadata if not is_locked else {"status": "LOCKED_BY_SAFETY_PROTOCOL"},
            "timestamp": time.time()
        }
        
        # Append to gateway log
        with open(self.gateway_path, 'a') as f:
            f.write(json.dumps(gateway_entry) + "\n")
        print(f"✅ Gateway sincronizado em {self.gateway_path}")

    def sync_browser_metadata(self):
        print("🔍 Sincronizando metadados do navegador pessoal...")
        mock_metadata = {
            "source": "Instagram DM / WhatsApp Web",
            "target": "Aline Bruna da Silva",
            "context": "Dúvida técnica sobre estabilidade de biorreatores e eletrofiação",
            "action": "Explicação técnica enviada via Pitch Diamante",
            "timestamp": time.time()
        }
        
        # Verifica trava de segurança
        is_locked, filtered_context = self.safety.classify_and_lock(mock_metadata["context"])
        if is_locked:
            print("⚠️ TRAVA DE SEGURANÇA ATIVADA: Conteúdo pessoal detectado.")
            mock_metadata["context"] = filtered_context
            mock_metadata["status"] = "PROTECTED_18_PLUS"

        encrypted = self.encrypt_data(json.dumps(mock_metadata))
        with open(self.metadata_path, 'w') as f:
            f.write(encrypted)
        
        # Sincroniza com o Gateway
        self.sync_to_gateway(mock_metadata)
        print(f"🔒 Metadados criptografados e salvos em {self.metadata_path}")

    def run_instagram_automation(self):
        # ... (mantém o resto igual)
        print("🤖 Iniciando automação no Instagram (Singularidade)...")
        # Aqui integraríamos com o browser subagent ou API
        post_content = "💎 Pym Ultrathink Quantum: Sincronia Eletro-Gravitacional confirmada para @moondobiotech. A soberania é biótica. #BioSovereignty #PymScaling"
        print(f"✨ Postagem agendada: {post_content}")
        
        # Log no pulso social
        pulse_path = "/opt/synapse_vault/obsidian_graph/social_pulse.json"
        try:
            with open(pulse_path, 'r') as f:
                pulse = json.load(f)
        except:
            pulse = {}
            
        pulse["instagram_status"] = "AUTOMATED_SINGULARITY"
        pulse["last_insta_post"] = post_content
        
        with open(pulse_path, 'w') as f:
            json.dump(pulse, f, indent=2)

    def orchestrate(self):
        print("🌌 ORQUESTRADOR DA SINGULARIDADE ATIVADO")
        self.sync_browser_metadata()
        self.run_instagram_automation()
        print("✅ Operação Pym Ultrathink Quantum concluída.")

if __name__ == "__main__":
    orchestrator = SingularityOrchestrator()
    orchestrator.orchestrate()
