from fastapi import FastAPI
from Hechos import HechosObservables
from MotorInferencia import MotorDiagnosticoDesdeArchivo

#titulo del API via FastAPI
app = FastAPI(title="Diagnóstico de fallas en redes domésticas - Sistema Experto", version="0,1,1")

#Endpoint para diagnóstico de fallas de red
@app.post("/diagnostico")

#Metodo principal del API
def diagnostico(hechos: HechosObservables):
    #Creamos la instancia del motor de diagnóstico
    motor = MotorDiagnosticoDesdeArchivo(hechos)
    #Realizamos el diagnóstico
    resultado = motor.diagnosticar()
    return resultado