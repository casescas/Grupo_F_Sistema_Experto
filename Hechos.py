from pydantic import BaseModel
from typing import Optional

class HechosObservables(BaseModel):
    """
    Define los hechos observables que el usuario proporcionará al sistema experto.
    """

    # Estado de Conexión y Síntomas
    conexion_lenta: bool
    sin_internet: bool
    desconexion_intermittente: bool
    solo_un_dispositivo_afectado: bool

    # Estado del Router/Módem y Redes
    router_luces_normales: bool
    wifi_visible: bool
    router_encendido: bool
    cable_ethernet_usado: bool
    firmware_router_actualizado: bool

    # Rendimiento Medido (Opcional)
    velocidad_bajada_mbps: Optional[float] = None
    velocidad_ping_ms: Optional[int] = None

    # Estado de la Red Local
    otros_dispositivos_conectados: bool
    distancia_router_lejana: bool

    # Hechos adicionales
    reinicio_router_reciente: bool

    # Diagnóstico cliente/cableado
    drivers_red_ok: bool
    cable_ethernet_ok: bool
    adaptador_red_funcional: bool
    puerto_red_dispositivo_funcional: bool
    repetidor_cubre_zona_ok: bool
