from fastapi import FastAPI
from Hechos import HechosObservables
from MotorDiagnostico import MotorDiagnosticoDesdeArchivo

app = FastAPI(title="Diagnóstico de Red - Sistema Experto")

@app.post("/diagnostico")

#metodo para iniciar el diagnóstico
def diagnostico(hechos: HechosObservables):
    motor = MotorDiagnosticoDesdeArchivo(hechos)
    resultado = motor.diagnosticar()
    return resultado