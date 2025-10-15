# ------------------------------------------------------------
# Motor de Diagnóstico basado en reglas + hechos observables
# ------------------------------------------------------------
# - Carga reglas desde un JSON
# - Evalúa condiciones (booleanas y numéricas con operadores)
# - Integra medición de velocidad (SpeedTestConexion)
# - Opción de enriquecer sugerencias con Gemini (si está disponible)
# ------------------------------------------------------------

from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Tuple

# ------------------------------------------------------------
# Importes tolerantes a estructura de paquete (app/...) y plano
# ------------------------------------------------------------
try:
    # Estructura nueva (recomendada)
    from app.core import errors as Controller_Error
except Exception:  # pragma: no cover
    try:
        # Compatibilidad con nombre antiguo
        import Controller_Error  # type: ignore
    except Exception:
        Controller_Error = None  # Fallback: no hay logger propio

try:
    # Estructura nueva
    from app.services.speedtest import SpeedTestConexion  # type: ignore
except Exception:  # pragma: no cover
    try:
        # Compatibilidad con nombre antiguo
        from SpeedTest import SpeedTestConexion  # type: ignore
    except Exception:
        SpeedTestConexion = None  # Fallback: sin speedtest

try:
    # Tu conector de IA (opcional)
    from ChatGemini import GeminiConnector  # type: ignore
except Exception:  # pragma: no cover
    GeminiConnector = None  # Fallback: sin Gemini


# ------------------------------------------------------------
# Utilidades de logging seguro
# ------------------------------------------------------------
def _log_evento(clase: str, metodo: str, mensaje: str) -> None:
    """
    Loggea el evento usando tu controlador si existe; de lo contrario, imprime.
    """
    if Controller_Error and hasattr(Controller_Error, "Logs_Error"):
        try:
            Controller_Error.Logs_Error.CapturarEvento(
                clase=clase, metodo=metodo, mensaje=mensaje
            )
            return
        except Exception:
            pass
    # Fallback mínimo
    print(f"[{clase}.{metodo}] {mensaje}")


# ------------------------------------------------------------
# Resolución robusta de ruta al archivo de reglas
# ------------------------------------------------------------
def _ruta_reglas_por_defecto() -> str:
    """
    Devuelve la ruta absoluta a app/data/reglas_diagnostico_red.json,
    calculada de forma relativa a este archivo (funciona en Windows/Linux).
    """
    base = os.path.dirname(os.path.abspath(__file__))                # .../app/services
    data_dir = os.path.normpath(os.path.join(base, "..", "data"))    # .../app/data
    return os.path.join(data_dir, "reglas_diagnostico_red.json")


# ------------------------------------------------------------
# Parseo y evaluación de condiciones con operadores
# ------------------------------------------------------------
def _parse_operador(cond: str) -> Tuple[str, float]:
    """
    Parsea condiciones del tipo '< 5', '<= 10', '> 100', '>= 3.5', '= 42'
    Retorna (operador, umbral) o levanta ValueError si es inválido.
    """
    cond = cond.strip()
    # Soportamos operadores dobles primero
    for op in ("<=", ">=", "=="):
        if cond.startswith(op):
            valor = float(cond[len(op):].strip())
            return op, valor
    # Operadores simples
    if cond[0] in "<>=":
        op = cond[0]
        valor = float(cond[1:].strip())
        # Normalizamos '=' a '==' para comparación numérica
        if op == "=":
            op = "=="
        return op, valor
    raise ValueError(f"Condición numérica inválida: {cond}")


def _cumple_condicion(valor_actual: Any, condicion: Any) -> bool:
    """
    Evalúa si un valor 'valor_actual' cumple una 'condicion'.
    - Booleanos: igualdad directa
    - Strings: comparación numérica con operadores (<, <=, >, >=, ==)
    - None: no cumple
    """
    # Caso booleano
    if isinstance(condicion, bool):
        return valor_actual is not None and bool(valor_actual) == condicion

    # Caso numérico expresado como string con operador
    if isinstance(condicion, str):
        if valor_actual is None:
            return False
        try:
            op, umbral = _parse_operador(condicion)
            try:
                actual = float(valor_actual)
            except (TypeError, ValueError):
                return False

            if op == "<":
                return actual < umbral
            if op == "<=":
                return actual <= umbral
            if op == ">":
                return actual > umbral
            if op == ">=":
                return actual >= umbral
            if op == "==":
                return actual == umbral
            return False
        except Exception as e:
            _log_evento("MotorDiagnosticoDesdeArchivo", "_cumple_condicion", str(e))
            return False

    # Por defecto no cumple
    return False


# ------------------------------------------------------------
# Clase principal del motor
# ------------------------------------------------------------
class MotorDiagnosticoDesdeArchivo:
    """
    Motor de diagnóstico que:
    - Recibe 'hechos' (objeto con atributos o dict con claves)
    - Carga reglas desde un archivo JSON
    - Ejecuta pruebas de velocidad (si están disponibles)
    - Evalúa reglas y genera diagnóstico
    - Si no matchea, consulta Gemini (si está disponible)
    """

    def __init__(self, hechos: Any, ruta_reglas: str | None = None) -> None:
        # Hechos observables proporcionados por el usuario (objeto o dict)
        self.hechos = hechos

        # Instancia para medir velocidad (opcional si no está implementada)
        self.speedtest = SpeedTestConexion() if SpeedTestConexion else None

        # Ruta segura al archivo de reglas (usa la de app/data si no pasaste una)
        self.ruta_reglas = ruta_reglas or _ruta_reglas_por_defecto()

        # Carga de reglas
        self.reglas: List[Dict[str, Any]] = self.cargar_reglas(self.ruta_reglas)

    # --------------------------------------------------------
    # Carga de reglas desde JSON
    # --------------------------------------------------------
    def cargar_reglas(self, ruta: str) -> List[Dict[str, Any]]:
        """
        Carga las reglas desde un archivo JSON.
        Estructura esperada por regla:
        {
          "id": "R01",
          "causa": "Descripción",
          "condiciones": { "sin_internet": true, "velocidad_bajada_mbps": "< 5" },
          "sugerencias": ["Paso 1", "Paso 2", ...]
        }
        """
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
                _log_evento("MotorDiagnosticoDesdeArchivo", "cargar_reglas", "El JSON no es una lista de reglas.")
                return []
        except Exception as error:
            _log_evento("MotorDiagnosticoDesdeArchivo", "cargar_reglas", f"Error leyendo {ruta}: {error}")
            return []

    # --------------------------------------------------------
    # Diagnóstico principal
    # --------------------------------------------------------
    def diagnosticar(self) -> Dict[str, Any]:
        """
        Ejecuta medición de velocidad (si está disponible), evalúa reglas y
        retorna un dict con causa/sugerencias/velocidades.
        """
        try:
            # 1) Medición de velocidad (si tenemos clase disponible)
            resultados = {"ping": None, "bajada": None, "subida": None}
            if self.speedtest:
                try:
                    self.speedtest.medir()
                    resultados = self.speedtest.obtener_resultados()
                except Exception as e:
                    _log_evento("MotorDiagnosticoDesdeArchivo", "diagnosticar(medir)", str(e))

            # 2) Evaluar reglas en orden
            for regla in self.reglas:
                if self.evaluar_regla(regla, resultados):
                    return self.formar_respuesta(regla, resultados)

            # 3) Si no matchea ninguna, pedir ayuda a Gemini (si existe)
            return self.respuesta_gemini(resultados)

        except Exception as error:
            _log_evento("MotorDiagnosticoDesdeArchivo", "diagnosticar", str(error))
            return {
                "causa_probable": "Error en el diagnóstico",
                "sugerencias": ["Ocurrió un error al procesar las reglas."],
                "velocidad_ping": resultados.get("ping") if isinstance(resultados, dict) else None,
                "velocidad_bajada": resultados.get("bajada") if isinstance(resultados, dict) else None,
                "velocidad_subida": resultados.get("subida") if isinstance(resultados, dict) else None,
            }

    # --------------------------------------------------------
    # Evaluación de una regla contra hechos + resultados
    # --------------------------------------------------------
    def evaluar_regla(self, regla: Dict[str, Any], resultados: Dict[str, Any]) -> bool:
        """
        Devuelve True si TODOS los pares clave:valor en 'condiciones' se cumplen.
        - Busca la clave primero en 'hechos' (atributo o dict), luego en 'resultados'.
        """
        condiciones: Dict[str, Any] = regla.get("condiciones", {})

        for clave, valor_esperado in condiciones.items():
            # 1) Obtener valor actual desde hechos (atributo o dict)
            valor_actual = None
            if isinstance(self.hechos, dict):
                valor_actual = self.hechos.get(clave)
            else:
                valor_actual = getattr(self.hechos, clave, None)

            # 2) Si no está en hechos, intentar en resultados de speedtest
            if valor_actual is None:
                valor_actual = resultados.get(clave)

            # 3) Evaluar
            if not _cumple_condicion(valor_actual, valor_esperado):
                return False

        return True  # Se cumplieron todas las condiciones

    # --------------------------------------------------------
    # Construcción de respuesta cuando una regla coincide
    # --------------------------------------------------------
    def formar_respuesta(self, regla: Dict[str, Any], resultados: Dict[str, Any]) -> Dict[str, Any]:
        """
        Devuelve la salida estándar del motor cuando hay match de regla.
        Si Gemini está disponible, agrega un tip extra de IA al final.
        """
        sugerencias = list(regla.get("sugerencias", []))

        # Tip extra de IA (opcional)
        try:
            if GeminiConnector is not None:
                gemini = GeminiConnector()
                extra = gemini.consultar_gemini_con_pasos(self.hechos, causa=regla.get("causa"))
                if isinstance(extra, dict):
                    tip = extra.get("respuesta", "")
                    if tip:
                        sugerencias.append(tip)
        except Exception as e:
            _log_evento("MotorDiagnosticoDesdeArchivo", "formar_respuesta(Gemini)", str(e))

        return {
            "causa_probable": regla.get("causa", "Causa desconocida"),
            "sugerencias": sugerencias,
            "velocidad_ping": resultados.get("ping"),
            "velocidad_bajada": resultados.get("bajada"),
            "velocidad_subida": resultados.get("subida"),
        }

    # --------------------------------------------------------
    # Respuesta por defecto: sin match de regla (fallback)
    # --------------------------------------------------------
    def respuesta_gemini(self, resultados: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fallback cuando ninguna regla coincide.
        Si Gemini está disponible, pide una guía general de pasos.
        """
        sugerencias = [
            "Verifica todos los componentes de tu red (router, cables, repetidores, dispositivos).",
            "Si el problema persiste, solicitar asistencia técnica especializada.",
        ]

        try:
            if GeminiConnector is not None:
                gemini = GeminiConnector()
                extra = gemini.consultar_gemini_con_pasos(self.hechos)
                if isinstance(extra, dict):
                    tip = extra.get("respuesta", "")
                    if tip:
                        sugerencias.append(tip)
        except Exception as e:
            _log_evento("MotorDiagnosticoDesdeArchivo", "respuesta_gemini", str(e))

        return {
            "causa_probable": "No pudimos darte un diagnóstico preciso.",
            "sugerencias": sugerencias,
            "velocidad_ping": resultados.get("ping"),
            "velocidad_bajada": resultados.get("bajada"),
            "velocidad_subida": resultados.get("subida"),
        }

