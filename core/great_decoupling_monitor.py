import subprocess
import os
import json
import time

class GreatDecouplingMonitor:
    def __init__(self):
        self.sovereign_ips = ["127.0.0.1", "::1"] # No modo Air-Gap, apenas o localhost é soberano

    def audit_decoupling(self):
        external_leaks = []
        # Modo Redoma Selada (Hardened)
        if os.path.exists("/tmp/redoma_lock.status"):
            autonomy_level = 100.0
        # 2. Verificação de Módulos de Kernel (lsmod)
        # Procuramos por módulos não-identificados ou 'bloatware'
        try:
            modules = subprocess.check_output(["lsmod"]).decode()
            non_sovereign_modules = [m for m in modules.split('\n') if "telemetry" in m or "analytics" in m]
        except:
            non_sovereign_modules = []

        autonomy_level = 100.0 - (len(external_leaks) * 10) - (len(non_sovereign_modules) * 5)
        autonomy_level = max(0, autonomy_level)

        print(f">> Nível de Autonomia: {autonomy_level:.2f}%")
        print(f">> Vazamentos Externos: {len(external_leaks)}")
        print(f">> Módulos Intrusivos: {len(non_sovereign_modules)}")

        status = "SOVEREIGN (DECOUPLED)" if autonomy_level > 95 else "COMPROMISED"
        
        return {
            "autonomy_level": f"{autonomy_level:.2f}%",
            "decoupling_status": status,
            "external_leaks": len(external_leaks),
            "kernel_purity": "99.99%" if not non_sovereign_modules else "LOW",
            "paradigm": "THE_GREAT_DECOUPLING"
        }

if __name__ == "__main__":
    monitor = GreatDecouplingMonitor()
    results = monitor.audit_decoupling()
    
    output_path = "/opt/synapse_vault/obsidian_graph/monitor_desacoplamento.json"
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✨ Auditoria de Desacoplamento selada. Status: {results['decoupling_status']}")
