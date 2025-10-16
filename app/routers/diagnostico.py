# --------------------------------------------------------
# RUTAS DE LA API – Diagnóstico
# --------------------------------------------------------
from fastapi import APIRouter, HTTPException
from app.models.schemas import Caso, Resultado
from app.services.motor_inferencia import MotorDiagnosticoDesdeArchivo

router = APIRouter(prefix="/diagnostico", tags=["diagnostico"])


@router.get("/health")
def health():
    """Ping simple para verificar que el servicio esté vivo."""
    return {"status": "ok", "message": "Servicio de diagnóstico activo"}


@router.post("/run")
def run(caso: Caso) -> dict:
    """
    Ejecuta el motor de diagnóstico con los síntomas y contexto recibidos.
    Devuelve causa probable, sugerencias y métricas de velocidad (si están).
    """
    try:
        motor = MotorDiagnosticoDesdeArchivo(hechos=caso.dict())
        resultado = motor.diagnosticar()

        # Normalizamos la salida por si en el futuro cambiamos el motor
        return {
            "ok": True,
            "diagnostico": {
                "causa_probable": resultado.get("causa_probable"),
                "sugerencias": resultado.get("sugerencias", []),
                "velocidad": {
                    "ping": resultado.get("velocidad_ping"),
                    "bajada": resultado.get("velocidad_bajada"),
                    "subida": resultado.get("velocidad_subida"),
                },
            },
        }
    except Exception as e:
        # Evitamos romper el contrato de la API
        raise HTTPException(status_code=500, detail=f"Error en diagnóstico: {e}")
