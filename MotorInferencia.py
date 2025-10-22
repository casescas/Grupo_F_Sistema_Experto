import json
import Controller_Error
from hechos import HechosObservables
from ChatGemini import GeminiConnector
from SpeedTest import SpeedTestConexion
from pydantic import ValidationError


class MotorDiagnosticoDesdeArchivo:
    """
    Motor principal del sistema experto.
    Evalúa los hechos observables contra las reglas y consulta Gemini si no hay coincidencias.
    """

    def __init__(self, hechos_data, ruta_reglas="reglas_diagnostico_red.json"):
        self.speedtest = SpeedTestConexion()
        self.reglas = self.cargar_reglas(ruta_reglas)

        try:
            self.hechos = HechosObservables(**hechos_data)
        except ValidationError as e:
            Controller_Error.Logs_Error.CapturarEvento(
                clase="MotorDiagnosticoDesdeArchivo",
                metodo="__init__",
                mensaje=str(e)
            )
            self.hechos = None

    def cargar_reglas(self, ruta):
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as error:
            Controller_Error.Logs_Error.CapturarEvento(
                clase="MotorDiagnosticoDesdeArchivo",
                metodo="cargar_reglas",
                mensaje=str(error)
            )
            return []

    def diagnosticar(self):
        """
        Recorre las reglas y aplica el diagnóstico basado en coincidencias.
        """
        try:
            if not self.hechos:
                return {"causa_probable": "Error en los hechos de entrada"}

            hechos_dict = self.hechos.model_dump(exclude_none=True)

            # 🔹 Este bloque estaba mal indentado antes
            for regla in self.reglas:
                if self.evaluar_regla(hechos_dict, regla):
                    return self.formar_respuesta(regla)

            return self.respuesta_gemini()

        except Exception as error:
            Controller_Error.Logs_Error.CapturarEvento(
                clase="MotorDiagnosticoDesdeArchivo",
                metodo="diagnosticar",
                mensaje=str(error)
            )
            return {
                "causa_probable": "Error en el diagnóstico",
                "sugerencias": ["Ocurrió un error al procesar las reglas."]
            }

    def evaluar_regla(self, hechos_dict, regla):
        """
        Evalúa si los hechos cumplen las condiciones de una regla.
        """
        condiciones = regla.get("condiciones", {})

        for clave, valor in condiciones.items():
            fact_value = hechos_dict.get(clave)

            if fact_value is None:
                return False

            if isinstance(valor, bool) and fact_value != valor:
                return False

            if isinstance(valor, str):
                try:
                    operador = valor[0]
                    umbral = float(valor[1:].strip())

                    if operador == "<" and not fact_value < umbral:
                        return False
                    elif operador == ">" and not fact_value > umbral:
                        return False
                    elif operador == "=" and not fact_value == umbral:
                        return False
                except Exception as e:
                    Controller_Error.Logs_Error.CapturarEvento(
                        clase="MotorDiagnosticoDesdeArchivo",
                        metodo="evaluar_regla",
                        mensaje=str(e)
                    )
                    return False

        return True

    def formar_respuesta(self, regla):
        """
        Construye la respuesta final cuando una regla coincide.
        """
        return {
            "causa_probable": regla.get("causa", "Causa desconocida"),
            "sugerencias": regla.get("sugerencias", [])
        }

    def respuesta_gemini(self):
        """
        Consulta a Gemini cuando no hay coincidencias en las reglas.
        """
        gemini = GeminiConnector()
        try:
            respuesta = gemini.consultar_gemini_con_pasos(self.hechos)
            return {
                "causa_probable": "No se encontró una coincidencia en las reglas.",
                "IMPORTANTE": [
                    "Se solicitó asistencia a Gemini.",
                    respuesta.get("respuesta", "Sin respuesta de Gemini.")
                ]
            }
        except Exception as error:
            Controller_Error.Logs_Error.CapturarEvento(
                clase="MotorDiagnosticoDesdeArchivo",
                metodo="respuesta_gemini",
                mensaje=str(error)
            )
            return {
                "causa_probable": "Asistencia Gemini no disponible",
                "sugerencias": ["Verifique la conexión o API Key."]
            }
