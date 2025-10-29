import google.generativeai as genai
from dotenv import dotenv_values

class GeminiConnector:
    def __init__(self):
        env = dotenv_values("archivo.env")
        self.api_key = env.get("GEMINI_API_KEY")

        if not self.api_key:
            raise ValueError("API KEY no encontrada en archivo.env")

        # Configura Gemini
        genai.configure(api_key=self.api_key)

        # Modelo recomendado
        self.model = genai.GenerativeModel("models/gemini-pro")

    def consultar_gemini_con_pasos(self, hechos):

        prompt = f"""
Eres un asistente experto en redes domésticas.

Contexto:
{hechos.model_dump()}

Devuelve SOLO pasos numerados para resolver el problema, en español, con oraciones cortas.
"""

        try:
            res = self.model.generate_content(
                prompt,
                generation_config={"temperature": 0.5}
            )

            # ✅ NUEVA forma recomendada de obtener texto
            return res.text

        except Exception as e:
            return f"⚠️ Error consultando Gemini: {e}"
