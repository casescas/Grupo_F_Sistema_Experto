from pydantic import BaseModel
from typing import Optional

class HechosObservables(BaseModel):
    conexion_lenta: Optional[bool] = None
    sin_internet: Optional[bool] = None
    desconexion_intermittente: Optional[bool] = None
    solo_un_dispositivo_afectado: Optional[bool] = None

    router_luces_normales: Optional[bool] = None
    wifi_visible: Optional[bool] = None
    router_encendido: Optional[bool] = None
    cable_ethernet_usado: Optional[bool] = None
    
    velocidad_bajada_mbps: Optional[float] = None
    velocidad_ping_ms: Optional[float] = None

    otros_dispositivos_conectados: Optional[bool] = None
    distancia_router_lejana: Optional[bool] = None
    reinicio_router_reciente: Optional[bool] = None

    drivers_red_ok: Optional[bool] = None
    cable_ethernet_ok: Optional[bool] = None
    adaptador_red_funcional: Optional[bool] = None
    puerto_red_dispositivo_funcional: Optional[bool] = None
    repetidor_cubre_zona_ok: Optional[bool] = None
