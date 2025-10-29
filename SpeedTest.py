import subprocess
import json
import re
import Controller_Error

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
            # ------------------------------------------------
            # PRIMER MÉTODO: usar la librería de Python (speedtest-cli)
            # ------------------------------------------------
            try:
                import speedtest
                st = speedtest.Speedtest()
                st.get_best_server()
                self.ping = round(st.results.ping, 2)
                self.bajada = round(st.download() / 1_000_000, 2)  # Mbps
                self.subida = round(st.upload() / 1_000_000, 2)    # Mbps
                return
            except Exception as inner_error:
                Controller_Error.Logs_Error.CapturarEvento(
                    clase="SpeedTestConexion",
                    metodo="medir (speedtest-cli)",
                    mensaje=f"Fallo en librería speedtest-cli: {inner_error}"
                )

            # ------------------------------------------------
            # SEGUNDO MÉTODO: usar el ejecutable externo si existe
            # ------------------------------------------------
            try:
                resultado = subprocess.run(
                    ["speedtest", "--format=json"],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                salida = resultado.stdout.strip()

                if salida.startswith("{"):
                    data = json.loads(salida)
                    self.ping = round(data["ping"]["latency"], 2)
                    self.bajada = round(data["download"]["bandwidth"] / 125000, 2)
                    self.subida = round(data["upload"]["bandwidth"] / 125000, 2)
                    return
            except FileNotFoundError:
                Controller_Error.Logs_Error.CapturarEvento(
                    clase="SpeedTestConexion",
                    metodo="medir (subprocess-json)",
                    mensaje="Comando externo 'speedtest' no encontrado en el sistema"
                )
            except Exception as inner_error:
                Controller_Error.Logs_Error.CapturarEvento(
                    clase="SpeedTestConexion",
                    metodo="medir (subprocess-json)",
                    mensaje=f"Error ejecutando subprocess: {inner_error}"
                )

            # ------------------------------------------------
            # TERCER MÉTODO: parseo por regex (texto plano)
            # ------------------------------------------------
            try:
                resultado = subprocess.run(
                    ["speedtest"],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                salida = resultado.stdout

                ping = re.findall(r"Ping:\s+([\d\.]+)", salida)
                bajada = re.findall(r"Download:\s+([\d\.]+)", salida)
                subida = re.findall(r"Upload:\s+([\d\.]+)", salida)

                self.ping = float(ping[0]) if ping else 0.0
                self.bajada = float(bajada[0]) if bajada else 0.0
                self.subida = float(subida[0]) if subida else 0.0

            except Exception as inner_error:
                Controller_Error.Logs_Error.CapturarEvento(
                    clase="SpeedTestConexion",
                    metodo="medir (regex fallback)",
                    mensaje=f"Error en regex fallback: {inner_error}"
                )

        except Exception as error:
            Controller_Error.Logs_Error.CapturarEvento(
                clase="SpeedTestConexion",
                metodo="medir",
                mensaje=f"Error general: {error}"
            )
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
