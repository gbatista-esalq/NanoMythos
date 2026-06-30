import json
import os
import hashlib
from functools import wraps

class TimeStone:
    """
    Pedra do Tempo: Mecanismo de Cache (Memoization) de Latência Zero
    Armazena o resultado de gerações longas da rede baseando-se no hash físico do input.
    """
    def __init__(self, cache_file="time_stone_cache.json"):
        self.cache_dir = os.path.join("/opt/synapse_vault", "cache")
        # Fallback se o vault não estiver acessível para escrita, salva localmente na workspace
        if not os.access(os.path.dirname("/opt/synapse_vault"), os.W_OK):
            self.cache_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scratch")
            
        os.makedirs(self.cache_dir, exist_ok=True)
        self.cache_path = os.path.join(self.cache_dir, cache_file)
        self.memory = self._load_cache()

    def _load_cache(self):
        if os.path.exists(self.cache_path):
            with open(self.cache_path, 'r', encoding='utf-8') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {}
        return {}

    def _save_cache(self):
        with open(self.cache_path, 'w', encoding='utf-8') as f:
            json.dump(self.memory, f, ensure_ascii=False, indent=2)

    def generate_hash(self, content: str) -> str:
        """Produz a assinatura gravitacional (hash SHA-256) do conteúdo."""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def get(self, content_hash: str):
        return self.memory.get(content_hash)

    def set(self, content_hash: str, payload: dict):
        self.memory[content_hash] = payload
        self._save_cache()

# Instância Global da Pedra do Tempo
time_stone = TimeStone()

def pedra_do_tempo_decorator(func):
    """
    Decorador Quântico: Se o conteúdo já foi processado, "rebobina o tempo"
    e devolve o resultado imediato (0ms latência).
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Em métodos de classe, args[0] é self. Se houver args[1], é a corda_real.
        # Caso contrário, pode estar nos kwargs
        corda_real = kwargs.get('corda_real')
        if not corda_real and len(args) > 1:
            corda_real = args[1]
        elif not corda_real and len(args) == 1:
            corda_real = args[0] # Se for função pura
            
        content_for_hash = str(corda_real)
        content_hash = time_stone.generate_hash(content_for_hash)
        
        cached_result = time_stone.get(content_hash)
        if cached_result:
            print(f"\n[ ⏳ PEDRA DO TEMPO ] Realidade Rebobinada! Resultado obtido do cache (0ms) -> Hash: {content_hash[:8]}")
            cached_result["_from_time_stone"] = True
            return cached_result
            
        print(f"\n[ ⏳ PEDRA DO TEMPO ] Assinatura Inédita detectada. Gerando cálculo temporal (Hash: {content_hash[:8]})...")
        # Executa o salto real
        result = func(*args, **kwargs)
        
        # Salva o resultado na joia
        time_stone.set(content_hash, result)
        return result
        
    return wrapper
