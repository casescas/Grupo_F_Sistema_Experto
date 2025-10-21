from fastapi import FastAPI
from modelos import HechosObservables
from reglas import MotorDiagnosticoDesdeArchivo

#titulo del API via FastAPI
#app = FastAPI(title="DiagnÃ³stico de fallas en redes domÃ©sticas - Sistema Experto", version="0.1.1")

app = FastAPI(
    title="DiagnÃ³stico de fallas en redes domÃ©sticas - Sistema Experto",
    version="0.1.1",
    description="Alumnos: Cristian Couto, Valeria Villega, Diego Estrada")

#Endpoint para diagnÃ³stico de fallas de red
@app.post("/diagnostico")

#Metodo principal del API
def diagnostico(hechos: HechosObservables):
    #Creamos la instancia del motor de diagnÃ³stico
    motor = MotorDiagnosticoDesdeArchivo(hechos)
    #Realizamos el diagnÃ³stico
    resultado = motor.diagnosticar()
    return resultado

