import openai
import Controller_Error  # Asegurate de tener este módulo en tu entorno

class ChatGPTConnector:
    
    #Metodo constructor que recibe la clave de API
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = self.api_key

    #Metodo para construir el prompt basado en los hechos
    def construir_prompt(self, hechos):
        try:            
            prompt = "Estoy desarrollando un sistema experto para diagnosticar fallas en redes domésticas. No se encontró coincidencia en las reglas definidas. A continuación se presentan los hechos observables:\n"
            for atributo, valor in hechos.dict().items():
                prompt += f"- {atributo.replace('_', ' ')}: {'Sí' if valor else 'No'}\n"
            prompt += "\n¿Podrías sugerir una posible causa del problema y pasos para resolverlo?"
            return prompt
        except Exception as error:
            Controller_Error.Logs_Error.CapturarEvento("ChatGPTConnector", "construir_prompt", str(error))
            return "No se pudo construir el prompt correctamente."
        
    #metodo para consultar a ChatGPT con el prompt construido
    def consultar_chatgpt(self, hechos):
        try:
            prompt = self.construir_prompt(hechos)
            if prompt.startswith("No se pudo"):
                return {"respuesta": prompt}
             
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Sos un asistente experto en redes domésticas."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            return {"respuesta": response.choices[0].message.content}
        except Exception as error:
            Controller_Error.Logs_Error.CapturarEvento("ChatGPTConnector", "consultar_chatgpt", str(error))
            return {"respuesta": "Ocurrió un error al consultar a ChatGPT."}
