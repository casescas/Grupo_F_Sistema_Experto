import speedtest
import Controller_Error 

class SpeedTest_Conexion:
    
    #metodo para medir velocidad
    @staticmethod
    def medir_velocidad():
        try: 
            st = speedtest.Speedtest()
            st.get_best_server()
            bajada = round(st.download() / 1_000_000, 2)   # Mbps
            subida = round(st.upload() / 1_000_000, 2)     # Mbps
            ping = round(st.results.ping, 2)
            return {"ping": ping, "bajada": bajada, "subida": subida}
        
        except Exception as error:
            Controller_Error.Logs_Error.CapturarEvento("SpeedTest_Conexion", "medir_velocidad", str(error))
            return {"ping": 0.0, "bajada": 0.0, "subida": 0.0}
