import os
import datetime

class Logs_Error:
    """
    Clase para registrar errores del sistema experto en un archivo de log.
    """

    @staticmethod
    def CapturarEvento(clase, metodo, mensaje):
        """
        Registra un evento o error en el archivo logs/errores.log
        """
        try:
            # Crear carpeta de logs si no existe
            log_dir = "logs"
            os.makedirs(log_dir, exist_ok=True)

            # Ruta completa del archivo de log
            ruta = os.path.join(log_dir, "errores.log")

            # Escribir el error con marca de tiempo
            with open(ruta, "a", encoding="utf-8") as f:
                f.write(f"[{datetime.datetime.now()}] {clase}.{metodo}: {mensaje}\n")

        except Exception as e:
            print(f"Error al registrar evento: {e}")
