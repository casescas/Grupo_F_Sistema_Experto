import os
import google.generativeai as genai
import Controller_Error
from dotenv import load_dotenv

load_dotenv()

class GeminiConnector:
    #metodo constructor para inicializar la conexión con Gemini
    def __init__(self):
        try:
            self.api_key = os.getenv("GEMINI_API_KEY")
            if not self.api_key:
                raise ValueError("No se encontró la clave de API de Gemini en el entorno.")
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel("gemini-pro")
        except Exception as error:
            Controller_Error.Logs_Error.CapturarEvento("GeminiConnector", "__init__", str(error))
            self.model = None

    #metodo para construir el prompt
    def construir_prompt(self, hechos):
        try:
            prompt = (
                "Estoy desarrollando un sistema experto para diagnosticar fallas en redes domésticas. "
                "No se encontró coincidencia en las reglas definidas. A continuación se presentan los hechos observables:\n"
            )
            for atributo, valor in hechos.dict().items():
                prompt += f"- {atributo.replace('_', ' ')}: {'Sí' if valor else 'No'}\n"
            prompt += "\n¿Podrías sugerir una posible causa del problema y pasos para resolverlo?"
            return prompt
        except Exception as error:
            Controller_Error.Logs_Error.CapturarEvento("GeminiConnector", "construir_prompt", str(error))
            return None

    #metodo para consultar a Gemini
    def consultar_gemini(self, hechos):
        try:
            if not self.model:
                return {"respuesta": "El modelo Gemini no está disponible."}

            prompt = self.construir_prompt(hechos)
            if not prompt:
                return {"respuesta": "No se pudo construir el prompt correctamente."}

            response = self.model.generate_content(prompt)
            return {"respuesta": response.text}
        except Exception as error:
            Controller_Error.Logs_Error.CapturarEvento("GeminiConnector", "consultar_gemini", str(error))
            return {"respuesta": "Ocurrió un error al consultar a Gemini."}
