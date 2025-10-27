import json
from hechos import HechosObservables
from ChatGemini import GeminiConnector

class MotorDiagnosticoDesdeArchivo:
    def __init__(self, hechos_data, ruta_reglas="reglas_diagnostico_red.json"):
        self.hechos = HechosObservables(**hechos_data)
        self.reglas = self.cargar_reglas(ruta_reglas)

    def cargar_reglas(self, ruta):
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)

    def diagnosticar(self):
        hechos_dict = self.hechos.model_dump(exclude_none=True)

        # Primero intenta reglas
        for regla in self.reglas:
            if self.evaluar_regla(hechos_dict, regla):
                sugerencias_ia = self.consulta_ia(self.hechos)
                return {
                    "causa_probable": regla["causa"],
                    "sugerencias": regla["sugerencias"] + sugerencias_ia
                }

        # Si no hay regla -> solo IA
        sugerencias_ia = self.consulta_ia(self.hechos)
        return {
            "causa_probable": "Diagnóstico asistido por IA",
            "sugerencias": sugerencias_ia
        }

    def evaluar_regla(self, hechos_dict, regla):
        for clave, valor in regla["condiciones"].items():
            if clave not in hechos_dict:
                return False

            recibido = hechos_dict[clave]
            if isinstance(valor, str) and valor[0] in "<>=":
                operador = valor[0]
                umbral = float(valor[1:])
                if operador == "<" and not recibido < umbral:
                    return False
                if operador == ">" and not recibido > umbral:
                    return False
                if operador == "=" and not recibido == umbral:
                    return False
            else:
                if recibido != valor:
                    return False

        return True

    def consulta_ia(self, hechos):
        gemini = GeminiConnector()
        respuesta = gemini.consultar_gemini_con_pasos(hechos)

        # Extraer texto de IA
        texto = respuesta.get("respuesta", "")

        # Convertir texto multilinea en array
        sugerencias = [
            line.strip("-•1234567890. ")
            for line in texto.split("\n")
            if line.strip()
        ]

        # Garantiza siempre al menos 1 sugerencia
        if not sugerencias:
            sugerencias = [
                "No pude interpretar el problema. Verifique cables, router y proveedor."
            ]

        return sugerencias
