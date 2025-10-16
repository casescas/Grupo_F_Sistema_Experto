# --------------------------------------------------------
# MODELOS (SCHEMAS) DE DATOS
# --------------------------------------------------------
# En este módulo definimos las clases que representan la
# estructura de los datos de entrada y salida del sistema experto.
# Usamos Pydantic para validación automática.
# --------------------------------------------------------

from pydantic import BaseModel
from typing import List, Dict, Optional

# --------------------------------------------------------
# Clase 'Caso': lo que envía el usuario al sistema
# --------------------------------------------------------
class Caso(BaseModel):
    """
    Representa la información que recibe el sistema experto.
    Contiene los síntomas observados y el contexto del usuario.
    """
    sintomas: List[str]           # Lista de síntomas (ejemplo: ["velocidad_baja", "sin_internet"])
    contexto: Dict[str, str] = {} # Información adicional (ejemplo: {"topologia": "router", "firmware": "actualizado"})


# --------------------------------------------------------
# Clase 'Resultado': lo que devuelve el sistema como diagnóstico
# --------------------------------------------------------
class Resultado(BaseModel):
    """
    Representa un diagnóstico generado por el sistema.
    Incluye el nombre del diagnóstico, nivel de confianza,
    pasos sugeridos y métricas de verificación.
    """
    diag: str                             # Nombre del diagnóstico (ejemplo: "saturacion_canal")
    conf: float                           # Nivel de confianza (entre 0 y 1)
    steps: Optional[List[str]] = None     # Lista de pasos para resolver el problema
    metricas: Optional[List[str]] = None  # Métricas esperadas después de aplicar la solución
