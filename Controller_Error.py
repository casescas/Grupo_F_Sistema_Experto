import datetime
import os
from socket import gethostbyname, gethostname
import sys

class Logs_Error:   

    #metodo para capturar evento de error y crear logs
    @staticmethod
    def CapturarEvento(_aplicativoTraductor, _clase, _evento):
        formatoFechaHorastandar = '%d_%m_%y_%H_%M_%S_%f'
        _fechaactual = datetime.datetime.now().strftime(formatoFechaHorastandar)
        Logs_Error.CrearInfoLogNuevo(_aplicativoTraductor, _fechaactual, _clase, _evento)
        return True

    #metodo para crear directorio para aplicativos - traductores
    @staticmethod
    def CrearDirectorio(_aplictivonombre):
        absolutoPath = os.path.dirname(os.path.abspath(sys.argv[0]))
        _rutanueva = 'ErrorSistemaExperto'
        relativoPath = os.path.join(_rutanueva, _aplictivonombre)
        fullPath = os.path.join(absolutoPath, relativoPath)
        if not os.path.exists(fullPath):
            os.makedirs(fullPath)
        return fullPath

    #metodo para el diseño de log ingresando el contenido dentro y titulo
    @staticmethod
    def CrearInfoLogNuevo(_aplicativoTraductor, _fechaactual, _clase, _evento):
        _rutanueva = Logs_Error.CrearDirectorio(_aplicativoTraductor +"\\"+ gethostname())
        log_file_path = os.path.join(_rutanueva, f"{_fechaactual}_{_clase}.txt")
        with open(log_file_path, "w") as file:
            file.write(f"Log de Evento errores - {_aplicativoTraductor}\n")
            file.write(str(_evento))