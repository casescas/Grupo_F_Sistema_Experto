import json

class MotorInferencia:
    def __init__(self, hechos_data, ruta_reglas="reglas_diagnostico_red.json"):
        """
        hechos_data:
            Diccionario JSON recibido desde React
        """
        # guardamos hechos como diccionario simple
        self.hechos = hechos_data

        # cargamos reglas desde JSON
        self.reglas = self._cargar_reglas(ruta_reglas)

    # ----------------------------------------------------------
    def _cargar_reglas(self, ruta):
        """
        Cargar reglas desde archivo JSON
        """
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)

    # ----------------------------------------------------------
    def diagnosticar(self):
        """
        Evalúa reglas 1 vez hasta encontrar coincidencia
        """
        for regla in self.reglas:
            if self._evaluar_regla(self.hechos, regla):
                return {
                    "causa_probable": regla["causa"],
                    "sugerencias": regla["sugerencias"]
                }

        # Si ninguna regla coincide
        return {
            "causa_probable": "No se pudo determinar una causa probable.",
            "sugerencias": [
                "Verificar cables y alimentación del router.",
                "Reiniciar el router.",
                "Contactar al proveedor de servicio."
            ]
        }

    # ----------------------------------------------------------
    def _evaluar_regla(self, hechos_dict, regla):
        """
        Evalúa las condiciones de cada regla contra los hechos recibidos
        """
        for clave, valor_esperado in regla["condiciones"].items():

            # Si falta un dato, descartar regla
            if clave not in hechos_dict:
                return False

            valor_hecho = hechos_dict[clave]

            # === Operadores condicionales ===
            if isinstance(valor_esperado, str) and valor_esperado[0] in "<>=":
                operador = valor_esperado[0]
                umbral = float(valor_esperado[1:])

                if operador == "<" and not valor_hecho < umbral: return False
                if operador == ">" and not valor_hecho > umbral: return False
                if operador == "=" and not valor_hecho == umbral: return False

            # === Comparación directa ===
            else:
                if valor_hecho != valor_esperado:
                    return False

        return True
