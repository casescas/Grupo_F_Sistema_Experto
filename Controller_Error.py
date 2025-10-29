import os
import datetime

class Logs_Error:
    """
    Clase para registrar errores y eventos del sistema experto en un archivo de log.
    """

    @staticmethod
    def CapturarEvento(clase, metodo, mensaje, tipo="ERROR"):
        """
        Registra un evento o error en el archivo logs/errores.log.
        tipo puede ser: INFO, WARNING o ERROR.
        """
        try:
            # Crear carpeta de logs si no existe
            log_dir = "logs"
            os.makedirs(log_dir, exist_ok=True)

            # Ruta completa del archivo de log
            ruta = os.path.join(log_dir, "errores.log")

            # Fecha y hora formateadas
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Escribir el evento en el archivo
            with open(ruta, "a", encoding="utf-8") as f:
                f.write(f"[{timestamp}] [{tipo}] {clase}.{metodo}: {mensaje}\n")

        except Exception as e:
            print(f"⚠️ Error al registrar evento: {e}")
