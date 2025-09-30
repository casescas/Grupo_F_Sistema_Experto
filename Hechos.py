from pydantic import BaseModel
from typing import Optional
from SpeedTest import SpeedTest_Conexion
import Controller_Error

class HechosObservables(BaseModel):
    
    #Variables que vienen del usuario vía FastAPI
    conexion_lenta: bool
    sin_internet: bool
    desconexion_intermittente: bool
    otros_dispositivos_conectados: bool
    router_luces_normales: bool
    wifi_visible: bool

    #Variables internas no las recibimos del archivo JSON
    velocidad_ping: Optional[float] = None
    velocidad_bajada: Optional[float] = None
    velocidad_subida: Optional[float] = None

    #Metodo para medir velocidad
    def medir_velocidad(self):
        try:
            resultado = SpeedTest_Conexion.medir_velocidad()
            self.velocidad_ping = resultado["ping"]
            self.velocidad_bajada = resultado["bajada"]
            self.velocidad_subida = resultado["subida"]
        except Exception as error:
            Controller_Error.Logs_Error.CapturarEvento("HechosObservables", "medir_velocidad", str(error))
            self.velocidad_ping = 0.0
            self.velocidad_bajada = 0.0
            self.velocidad_subida = 0.0