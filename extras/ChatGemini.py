import os
import google.generativeai as genai
import Controller_Error
from dotenv import dotenv_values

class GeminiConnector:
    #Metodo constructor para inicializar la conexiÃ³n con Gemini
    def __init__(self):
        try:
            #Cargar manualmente el archivo.env
            self.env_vars = dotenv_values("archivo.env")
            self.api_key = self.env_vars.get("GEMINI_API_KEY")
            #Verificar si la clave de API estÃ¡ presente
            if not self.api_key:
                raise ValueError("No se encontrÃ³ la clave de API de Gemini en el entorno.")
            #Configurar la clave de API para google.generativeai
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(model_name="models/gemini-2.5-pro")
        #Capturar y registrar cualquier error durante la inicializaciÃ³n
        except Exception as error:
            #Capturamos el error, se lo enviamos a  la clase Controller_Error.py para que lo registre en Logs.
            Controller_Error.Logs_Error.CapturarEvento("GeminiConnector", "__init__", str(error))
            self.model = None

    #Metodo para construir el prompt
    def construir_prompt(self, hechos):
        try:
            prompt = (
                "Estoy con un sistema experto para diagnosticar fallas en redes domÃ©sticas. "
                "En nuestras reglas definidas no encontramos problema. A continuaciÃ³n se presentan los hechos observables:\n"
            )
            for atributo, valor in hechos\.model_dump().items():
                prompt += f"- {atributo.replace('_', ' ')}: {'SÃ­' if valor else 'No'}\n"
            prompt += "\nÂ¿PodrÃ­as sugerir una posible causa del problema? Resumimelo"
            return prompt
        #Capturamos el error, se lo enviamos a  la clase Controller_Error.py para que lo registre en Logs.
        except Exception as error:
            Controller_Error.Logs_Error.CapturarEvento("GeminiConnector", "construir_prompt", str(error))
            return None

    #Metodo para consultar a Gemini
    def consultar_gemini(self, hechos):
        try:
            if not self.model:
                return {"respuesta": "El modelo Gemini no estÃ¡ disponible."}
            
            prompt = self.construir_prompt(hechos)
            if not prompt:
                return {"respuesta": "No se pudo construir el prompt correctamente."}

            response = self.model.generate_content(prompt)
            return {"respuesta": response.text}
        #Capturamos el error, se lo enviamos a  la clase Controller_Error.py para que lo registre en Logs.
        except Exception as error:
            Controller_Error.Logs_Error.CapturarEvento("GeminiConnector", "consultar_gemini", str(error))
            return {"respuesta": "OcurriÃ³ un error al consultar a Gemini."}

    def consultar_gemini_con_pasos(self, hechos, causa=None):
        try:
            if not self.model:
                return {"respuesta": "El modelo Gemini no estÃ¡ disponible."}
            
            prompt = (
                "Estoy con un sistema experto para diagnosticar fallas en redes domÃ©sticas.\n"
                "Hechos observables:\n"
            )
            for atributo, valor in hechos\.model_dump().items():
                prompt += f"- {atributo.replace('_', ' ')}: {'SÃ­' if valor else 'No'}\n"
    
            if causa:
                prompt += f"\nLa causa probable detectada es: {causa}.\n"
    
            prompt += (
                "\nÂ¿PodrÃ­as detallarme en 5 pasos como resolverlo, resumidos, total 30 palabras?"
            )
    
            response = self.model.generate_content(prompt)
            return {"respuesta": response.text}
        
        except Exception as error:
            Controller_Error.Logs_Error.CapturarEvento("GeminiConnector", "consultar_gemini_con_pasos", str(error))
            return {"respuesta": "OcurriÃ³ un error al consultar a Gemini."}

