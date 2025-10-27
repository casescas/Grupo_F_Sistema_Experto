# ChatLocalLLM.py
import requests

class LocalLLMConnector:
    def __init__(self, base_url="http://localhost:1235/v1/chat/completions", model="meta-llama-3-8b-instruct"):
        self.base_url = base_url
        self.model = model

    def consultar(self, mensaje: str) -> str:
        try:
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": "Actúa como técnico certificado en redes domésticas."},
                    {"role": "user", "content": mensaje}
                ],
                "temperature": 0.35
            }

            response = requests.post(self.base_url, json=payload, timeout=40)
            response.raise_for_status()
            data = response.json()

            return data["choices"][0]["message"]["content"]

        except Exception as e:
            return f"[ERROR LLM]: {e}"
