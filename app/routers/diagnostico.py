# --------------------------------------------------------
# RUTAS DE LA API – Módulo Diagnóstico
# --------------------------------------------------------
# Este archivo agrupa los endpoints relacionados con el diagnóstico
# del sistema experto. Por ahora incluye un "health check" básico.
# --------------------------------------------------------

from fastapi import APIRouter

# Creamos un router (subgrupo de rutas con prefijo y etiqueta)
router = APIRouter(
    prefix="/diagnostico",   # Todas las rutas de este módulo empezarán con /diagnostico
    tags=["diagnostico"]     # Etiqueta que agrupa las rutas en la documentación de Swagger
)

# --------------------------------------------------------
# Endpoint /diagnostico/health
# --------------------------------------------------------
@router.get("/health")
def health():
    """
    Verifica que el servicio de diagnóstico esté activo.
    Sirve para pruebas rápidas desde el navegador o Swagger UI.
    """
    return {"status": "ok", "message": "Servicio de diagnóstico activo"}
