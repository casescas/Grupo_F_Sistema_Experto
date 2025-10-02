import speedtest
import Controller_Error

#Clase encargada de medir y almacenar la velocidad de conexión a Internet
class SpeedTestConexion:
    
    #Inicializamos los atributos de velocidad y ping.
    def __init__(self):
        self.ping = None
        self.bajada = None
        self.subida = None

    #se realiza la medición de velocidad y ping.
    def medir(self):
        try:
            #Usamos la librería speedtest para medir la velocidad y ping.
            st = speedtest.Speedtest()
            #Seleccionamos el mejor servidor basado en ping.
            st.get_best_server()
            #Realizamos las pruebas de descarga y subida.
            self.bajada = round(st.download() / 1_000_000, 2)
            self.subida = round(st.upload() / 1_000_000, 2)
            self.ping = round(st.results.ping, 2)
        #capturamos cualquier error y lo registramos en un archivo Logs localmente.
        except Exception as error:
            #Enviamos el error a la clase Controller_Error.py para que lo registre en Logs.
            Controller_Error.Logs_Error.CapturarEvento(
                clase="SpeedTestConexion",
                metodo="medir",
                mensaje=str(error)
            )
            #Como fue un error, debemos enviar valores por defecto.
            self.ping = 0.0
            self.bajada = 0.0
            self.subida = 0.0

    #Devuelve los resultados como diccionario.
    def obtener_resultados(self):
        return {
            "ping": self.ping,
            "bajada": self.bajada,
            "subida": self.subida
        }