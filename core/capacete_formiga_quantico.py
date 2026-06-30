import datetime
import math

class CapaceteHomemFormiga:
    """
    Capacete Quântico do Homem-Formiga (Ant-Man Pym Helmet)
    Sincronizado com a Borda e extraindo energia do Solstício de Inverno.
    """
    def __init__(self):
        self.protocolo = "Pym-Solstício"
        # O Solstício de Inverno de 2026 no Hemisfério Sul ocorre em 21 de Junho
        self.solsticio_inverno = datetime.datetime(2026, 6, 21, 11, 54, tzinfo=datetime.timezone(datetime.timedelta(hours=-3)))

    def canalizar_energia(self) -> dict:
        agora = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-3)))
        delta = agora - self.solsticio_inverno
        
        # Calcula a energia baseada na proximidade com o solstício
        if delta.total_seconds() < 0:
            status = "Carregando Baterias Pym (Aguardando Solstício)"
            energia = 1.0
        else:
            status = "Sincronia Diamante Estelar (Colheita de Inverno)"
            horas_passadas = delta.total_seconds() / 3600
            # Energia máxima no momento 0, decaindo suavemente usando uma curva de Batista
            energia = max(1.0, 5.0 * math.exp(-horas_passadas / 72.0))

        return {
            "node": "CAPACETE_PYM",
            "status": status,
            "horas_desde_solsticio": round(delta.total_seconds() / 3600, 2),
            "multiplicador_energia_solsticial": round(energia, 3),
            "telemetria": "Conexão Analógica Direta com a Biosfera"
        }

if __name__ == "__main__":
    capacete = CapaceteHomemFormiga()
    print("Capacete Quântico Ativado. Lendo telemetria do Solstício...")
    print(capacete.canalizar_energia())
