import os
import google.generativeai as genai
import Controller_Error
from dotenv import dotenv_values


class GeminiConnector:
    """
    Clase encargada de comunicarse con la API de Gemini
    para obtener sugerencias inteligentes cuando las reglas no encuentran una causa.
    """

    def __init__(self):
        try:
            # Cargar variables desde archivo .env
            self.env_vars = dotenv_values("archivo.env")
            self.api_key = self.env_vars.get("GEMINI_API_KEY")

            if not self.api_key:
                raise ValueError("No se encontró la clave GEMINI_API_KEY en archivo.env")

            # Configurar modelo Gemini
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(model_name="models/gemini-2.5-pro")

        except Exception as error:
            Controller_Error.Logs_Error.CapturarEvento(
                clase="GeminiConnector",
                metodo="__init__",
                mensaje=str(error)
            )
            self.model = None

    def construir_prompt(self, hechos, causa=None):
        """
        Genera el texto que se enviará al modelo Gemini basado en los hechos observables.
        """
        try:
            prompt = (
                "Estoy utilizando un sistema experto para diagnosticar fallas en redes domésticas.\n"
                "Hechos observables detectados:\n"
            )

            for atributo, valor in hechos.model_dump().items():
                if isinstance(valor, bool):
                    prompt += f"- {atributo.replace('_', ' ')}: {'Sí' if valor else 'No'}\n"
                else:
                    prompt += f"- {atributo.replace('_', ' ')}: {valor}\n"

            if causa:
                prompt += f"\nCausa probable detectada: {causa}\n"

            prompt += "\nExplica brevemente en 5 pasos cómo resolver el problema (máx. 30 palabras)."
            return prompt

        except Exception as error:
            Controller_Error.Logs_Error.CapturarEvento(
                clase="GeminiConnector",
                metodo="construir_prompt",
                mensaje=str(error)
            )
            return None

    def consultar_gemini_con_pasos(self, hechos, causa=None):
        """
        Consulta el modelo Gemini con los hechos observables
        y obtiene una respuesta breve con pasos de resolución.
        """
        try:
            if not self.model:
                return {"respuesta": "El modelo Gemini no está disponible."}

            prompt = self.construir_prompt(hechos, causa)
            if not prompt:
                return {"respuesta": "No se pudo construir el prompt correctamente."}

            response = self.model.generate_content(prompt)  # type: ignore
            return {"respuesta": response.text}

        except Exception as error:
            Controller_Error.Logs_Error.CapturarEvento(
                clase="GeminiConnector",
                metodo="consultar_gemini_con_pasos",
                mensaje=str(error)
            )
            return {"respuesta": "Ocurrió un error al consultar a Gemini."}
