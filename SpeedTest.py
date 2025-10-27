import subprocess
import json
import re
import Controller_Error

#prueba cristian
class SpeedTestConexion:

    def __init__(self):
        self.ping = 0.0
        self.bajada = 0.0
        self.subida = 0.0

    # ==================================================
    # MÉTODO PRINCIPAL DE MEDICIÓN
    # ==================================================
    def medir(self):
        try:
            # Intento 1: Ejecutar en JSON (más estable)
            resultado = subprocess.run(
                ["speedtest", "--format=json"],
                capture_output=True,
                text=True
            )

            salida = resultado.stdout.strip()

            if salida.startswith("{"):
                data = json.loads(salida)

                # Conversiones: bandwidth viene en bytes/s
                self.ping = round(data["ping"]["latency"], 2)
                self.bajada = round(data["download"]["bandwidth"] / 125000, 2)
                self.subida = round(data["upload"]["bandwidth"] / 125000, 2)
                return

            # ------------------------------------------------
            # Fallback: regex si JSON falla
            # ------------------------------------------------
            resultado = subprocess.run(
                ["speedtest"],
                capture_output=True,
                text=True
            )
            salida = resultado.stdout

            ping = re.findall(r"Ping:\s+([\d\.]+)", salida)
            bajada = re.findall(r"Download:\s+([\d\.]+)", salida)
            subida = re.findall(r"Upload:\s+([\d\.]+)", salida)

            self.ping = float(ping[0]) if ping else 0.0
            self.bajada = float(bajada[0]) if bajada else 0.0
            self.subida = float(subida[0]) if subida else 0.0

        except Exception as error:
            Controller_Error.Logs_Error.CapturarEvento(
                clase="SpeedTestConexion",
                metodo="medir",
                mensaje=str(error)
            )
            # Valores seguros
            self.ping = 0.0
            self.bajada = 0.0
            self.subida = 0.0

    # ==================================================
    # RETORNO DE RESULTADOS
    # ==================================================
    def obtener_resultados(self):
        return {
            "ping": self.ping,
            "bajada": self.bajada,
            "subida": self.subida
        }


# ======================================================
# FUNCIÓN EXPORTADA PARA FASTAPI
# ======================================================
def run_speedtest():
    test = SpeedTestConexion()
    test.medir()
    return test.obtener_resultados()
