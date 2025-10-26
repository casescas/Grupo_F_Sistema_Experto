import os
import google.generativeai as genai
from dotenv import dotenv_values
import Controller_Error


class GeminiConnector:
    """Clase encargada de comunicarse con la API de Gemini."""

    def __init__(self):
        try:
            # Cargar variables desde archivo.env
            self.env_vars = dotenv_values("archivo.env")
            self.api_key = self.env_vars.get("GEMINI_API_KEY")

            if not self.api_key:
                raise ValueError("No se encontró la clave GEMINI_API_KEY en archivo.env")

            # Configurar modelo de Gemini
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel("models/gemini-2.0-pro")

        except Exception as error:
            Controller_Error.Logs_Error.CapturarEvento(
                "GeminiConnector", "__init__", str(error)
            )
            self.model = None

    def consultar_gemini_con_pasos(self, hechos, causa=None):
        """Consulta a Gemini con los hechos observables."""
        try:
            if not self.model:
                return {"respuesta": "El modelo Gemini no está disponible."}

            prompt = (
                "Estoy usando un sistema experto para diagnosticar fallas en redes domésticas.\n"
                "Hechos observables:\n"
            )

            for atributo, valor in hechos.dict().items():
                prompt += f"- {atributo.replace('_', ' ')}: {'Sí' if valor else 'No'}\n"

            if causa:
                prompt += f"\nCausa probable detectada: {causa}\n"

            prompt += "\nExplica cómo resolverlo en 5 pasos, en total 30 palabras."

            response = self.model.generate_content(prompt)
            return {"respuesta": response.text}

        except Exception as error:
            Controller_Error.Logs_Error.CapturarEvento(
                "GeminiConnector", "consultar_gemini_con_pasos", str(error)
            )
            return {"respuesta": "Error al consultar a Gemini."}
