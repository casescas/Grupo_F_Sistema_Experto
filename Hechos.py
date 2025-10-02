
from pydantic import BaseModel

#clase para definir los hechos observables que el usuario proporcionará a través de la API.
class HechosObservables(BaseModel):

    conexion_lenta: bool
    sin_internet: bool
    desconexion_intermittente: bool
    otros_dispositivos_conectados: bool
    router_luces_normales: bool
    wifi_visible: bool

