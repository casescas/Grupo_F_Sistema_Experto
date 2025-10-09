import json
import Controller_Error
from ChatGemini import GeminiConnector
from SpeedTest import SpeedTestConexion

#Clase para generar un motor de diagnóstico basado en reglas y hechos observables.
class MotorDiagnosticoDesdeArchivo:
    
    #Inicializa con hechos y carga reglas desde un archivo JSON (reglas_diagnostico_red.json).
    def __init__(self, hechos, ruta_reglas="reglas_diagnostico_red.json"):
        #Hechos observables proporcionados por el usuario.
        self.hechos = hechos
        #Instanciamos para realizar pruebas de velocidad.
        self.speedtest = SpeedTestConexion()
        #Cargamos las reglas desde el archivo JSON (reglas_diagnostico_red.json)
        self.reglas = self.cargar_reglas(ruta_reglas)

    #Cargar reglas desde un archivo JSON y manejar errores.
    def cargar_reglas(self, ruta):
        try:
            #Abrimos y leemos el archivo JSON (reglas_diagnostico_red.json) con las reglas.
            with open(ruta, "r", encoding="utf-8") as f:
                return json.load(f)
        #Capturamos el error, se lo enviamos a la clase Controller_Error.py para que lo registre en Logs.
        except Exception as error:
            #Se lo enviamos a la clase Controller_Error.py para que lo registre en Logs.
            Controller_Error.Logs_Error.CapturarEvento(clase="MotorDiagnosticoDesdeArchivo",metodo="_cargar_reglas", mensaje=str(error))
            #Como dio error, retornamos una lista vacía por defecto.
            return []

    #Metodo principal para diagnosticar basado en hechos y reglas.
    def diagnosticar(self):
        try:

            #Evaluamos por iteracion cada regla para ver si coinciden con los hechos observables.
            #Traemos todas las reglas desde el archivo JSON (reglas_diagnostico_red.json).
            for regla in self.reglas:
                #llamamos al metodo para evaluar si la regla coincide con los hechos y resultados de velocidad.
                if self.evaluar_regla(regla):
                   #Si la regla coincide, sale del ciclo y formamos la respuesta y la retornamos.
                   return self.formar_respuesta(regla)
          
            #Si ninguna reglas coincide, consultamos mediante api a Gemini para obtener sugerencias adicionales.
            #jamas nos debemos  quedar sin respuesta.
            return self.respuesta_gemini()

        #Capturamos el error, se lo enviamos a  la clase Controller_Error.py para que lo registre en Logs.
        except Exception as error:
            Controller_Error.Logs_Error.CapturarEvento(clase="MotorDiagnosticoDesdeArchivo", metodo="diagnosticar", mensaje=str(error))
            #Si ocurre un error, retornamos un mensaje de error por defecto.
            return {
                "causa_probable": "Error en el diagnóstico",
                "sugerencias": ["Ocurrió un error al procesar las reglas. Vuelva a intentar más tarde."],
           }

    #Metodo para evaluar si una regla coincide con los hechos observables.
    def evaluar_regla(self, regla):
        condiciones = regla.get("condiciones", {})
        #recorremos cada condición en la regla.
        for clave, valor in condiciones.items():
            #Obtenemos el valor actual del hecho observable.
            valor_actual = getattr(self.hechos, clave)
            #Si el valor es booleano, lo comparamos directamente.
            if isinstance(valor, bool):
                if valor_actual != valor:
                    return False
            #Si el valor es un string con operador, lo evaluamos.
            elif isinstance(valor, str):
                try:
                    operador, umbral = valor.split()
                    umbral = float(umbral)
                    #Evaluamos según el operador.
                    if operador == "<" and not valor_actual < umbral:
                        return False
                    elif operador == ">" and not valor_actual > umbral:
                        return False
                #Capturamos el error, se lo enviamos a la clase Controller_Error.py para que lo registre en Logs.
                except Exception as e:
                    Controller_Error.Logs_Error.CapturarEvento(
                        clase="MotorDiagnosticoDesdeArchivo",
                        metodo="_evaluar_regla",
                        mensaje=str(e)
                    )
                #Como tuvimos error, debemos devolver False.
                    return False
        return True

    #Metodo para formar la respuesta basada en la regla coincidente.
    def formar_respuesta(self, regla):
        return {
            "causa_probable": regla.get("causa", "Causa desconocida"),
            "sugerencias": regla.get("sugerencias", []),
        }

    #Metodo para obtener una respuesta de Gemini si ninguna regla coincide.
    def respuesta_gemini(self):
        #Instanciamos la clase GeminiConnector para consultar a Gemini.
        gemini = GeminiConnector()
        #Consultamos a Gemini pasando los hechos observables.
        
        #respuesta = gemini.consultar_gemini(self.hechos)
        respuesta = gemini.consultar_gemini_con_pasos(self.hechos)
        
        #Retornamos la respuesta de Gemini junto con los resultados de velocidad.
        return {
            "causa_probable": "No encontramos posible causa en nuestras reglas.",
            "IMPORTANTE": [
                "Vamos a solicita asistencia técnica expecializada a Sistema Ingeligente - Gemini.",
                respuesta.get("respuesta", "No se pudo obtener respuesta de Gemini.")
            ],
        }

#Realizamos la prueba de velocidad de internet se puede requerir desde la vista
#self.speedtest.medir()
#resultados = self.speedtest.obtener_resultados()