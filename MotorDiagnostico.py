import json
import Controller_Error
from ChatGemini import GeminiConnector

class MotorDiagnosticoDesdeArchivo:

    #inicializa el motor de diagnóstico cargando las reglas desde un archivo JSON
    def __init__(self, hechos, ruta_reglas="reglas_diagnostico_red.json"):
        self.hechos = hechos
        try:
            with open(ruta_reglas, "r", encoding="utf-8") as f:
                self.reglas = json.load(f)
        except Exception as error:
            Controller_Error.Logs_Error.CapturarEvento(
                "MotorDiagnosticoDesdeArchivo", "__init__", str(error)
            )
            self.reglas = []
    
    #metodo para evaluar las condiciones de las reglas
    def diagnosticar(self):
        try:
            self.hechos.medir_velocidad()

            for regla in self.reglas:
                condiciones = regla.get("condiciones", {})
                cumple = True

                for clave, valor in condiciones.items():
                    valor_actual = getattr(self.hechos, clave, None)

                    if isinstance(valor, bool):
                        if valor_actual != valor:
                            cumple = False
                            break
                    elif isinstance(valor, str):
                        try:
                            operador, umbral = valor.split()
                            umbral = float(umbral)

                            if operador == "<" and not valor_actual < umbral:
                                cumple = False
                                break
                            elif operador == ">" and not valor_actual > umbral:
                                cumple = False
                                break
                        except Exception as e:
                            Controller_Error.Logs_Error.CapturarEvento(
                                "MotorDiagnosticoDesdeArchivo", "evaluar_condicion", str(e)
                            )
                            cumple = False
                            break

                if cumple:
                    return {
                        "causa_probable": regla.get("causa", "Causa desconocida"),
                        "sugerencias": regla.get("sugerencias", []),
                        "velocidad_ping": self.hechos.velocidad_ping,
                        "velocidad_bajada": self.hechos.velocidad_bajada,
                        "velocidad_subida": self.hechos.velocidad_subida
                    }
            
            #Si ninguna regla coincide, usar Gemini para sugerencias   
            gemini = GeminiConnector()
            respuesta_gemini = gemini.consultar_gemini(self.hechos)
            
            return {
                "causa_probable": "Diagnóstico no concluyente",
                "sugerencias": [
                    "Verifica todos los componentes de tu red.",
                    "Solicita asistencia técnica.",
                    respuesta_gemini.get("respuesta", "No se pudo obtener respuesta de Gemini.")
                ],
                "velocidad_ping": self.hechos.velocidad_ping,
                "velocidad_bajada": self.hechos.velocidad_bajada,
                "velocidad_subida": self.hechos.velocidad_subida
            }

        except Exception as error:
            Controller_Error.Logs_Error.CapturarEvento(
                "MotorDiagnosticoDesdeArchivo", "diagnosticar", str(error)
            )
            return {
                "causa_probable": "Error en el diagnóstico",
                "sugerencias": ["Ocurrió un error al procesar las reglas."],
                "velocidad_ping": None,
                "velocidad_bajada": None,
                "velocidad_subida": None
            }