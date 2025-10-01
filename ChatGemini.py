import os
import google.generativeai as genai
import Controller_Error
from dotenv import dotenv_values

class GeminiConnector:
    #Metodo constructor para inicializar la conexión con Gemini
    def __init__(self):
        try:
            #Cargar manualmente el archivo.env
            self.env_vars = dotenv_values("archivo.env")          
            self.api_key = self.env_vars.get("GEMINI_API_KEY")
            
            if not self.api_key:
                raise ValueError("No se encontró la clave de API de Gemini en el entorno.")
            
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(model_name="models/gemini-2.5-pro")
        except Exception as error:
            Controller_Error.Logs_Error.CapturarEvento("GeminiConnector", "__init__", str(error))
            self.model = None

    #Metodo para construir el prompt
    def construir_prompt(self, hechos):
        try:
            prompt = (
                "Estoy con un sistema experto para diagnosticar fallas en redes domésticas. "
                "En nuestras reglas definidas no encontramos problema. A continuación se presentan los hechos observables:\n"
            )
            for atributo, valor in hechos.dict().items():
                prompt += f"- {atributo.replace('_', ' ')}: {'Sí' if valor else 'No'}\n"
            prompt += "\n¿Podrías sugerir una posible causa del problema? Resumimelo"
            return prompt
        except Exception as error:
            Controller_Error.Logs_Error.CapturarEvento("GeminiConnector", "construir_prompt", str(error))
            return None

    #Metodo para consultar a Gemini
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


#Simulación de hechos
#class HechosSimulados:
#    def dict(self):
#        return {
#            "internet_funciona": False,
#            "router_encendido": True,
#            "wifi_visible": True,
#            "dispositivo_conectado": False,
#            "ip_asignada": False
#        }

# Prueba
#conector = GeminiConnector()
#respuesta = conector.consultar_gemini(HechosSimulados())
#print("Respuesta de Gemini:")
#print(respuesta["respuesta"])