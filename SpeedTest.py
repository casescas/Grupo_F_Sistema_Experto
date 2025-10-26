import speedtest
import Controller_Error

# ======================================================
# Clase encargada de medir y almacenar la velocidad de WiFi/Internet
# ======================================================
class SpeedTestConexion:

    def __init__(self):
        self.ping = None
        self.bajada = None
        self.subida = None

    def medir(self):
        try:
            st = speedtest.Speedtest()
            st.get_best_server()

            # Medición de bajada (download) y subida (upload)
            self.bajada = round(st.download() / 1_000_000, 2)
            self.subida = round(st.upload() / 1_000_000, 2)
            self.ping = round(st.results.ping, 2)

        except Exception as error:
            # Registro de error en log
            Controller_Error.Logs_Error.CapturarEvento(
                clase="SpeedTestConexion",
                metodo="medir",
                mensaje=str(error)
            )
            # Valores seguros en caso de error
            self.ping = 0.0
            self.bajada = 0.0
            self.subida = 0.0

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
    try:
        test = SpeedTestConexion()
        test.medir()
        return test.obtener_resultados()

    except Exception as error:
        # Fallback extremo (no debería ocurrir)
        Controller_Error.Logs_Error.CapturarEvento(
            clase="SpeedTestConexion",
            metodo="run_speedtest",
            mensaje=str(error)
        )
        return {
            "ping": 0.0,
            "bajada": 0.0,
            "subida": 0.0
        }
