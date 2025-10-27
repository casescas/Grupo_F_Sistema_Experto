from fastapi import FastAPI, Request
from hechos import HechosObservables
from MotorInferencia import MotorInferencia
from Controller_Error import Logs_Error
from SpeedTest import run_speedtest
from fastapi.middleware.cors import CORSMiddleware
import datetime


# ======================================================
# CONFIGURACIÓN FASTAPI
# ======================================================
app = FastAPI(
    title="Diagnóstico de fallas en redes domésticas - Sistema Experto",
    version="0.3.0",
    description="Alumnos: Cristian Couto, Valeria Villega, Diego Estrada"
)

# ======================================================
# CORS (Permite conexión desde React)
# ======================================================
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================================================
# ENDPOINT: DIAGNÓSTICO PRINCIPAL
# ======================================================
@app.post("/diagnostico")
async def diagnostico(request: Request):
    try:
        hechos_dict = await request.json()
        motor = MotorInferencia(hechos_dict)
        resultado = motor.diagnosticar()

        return {
            "status": "OK",
            "diagnostico": resultado
        }

    except Exception as e:
        ...

# ======================================================
# ENDPOINT: SPEEDTEST
# ======================================================
@app.get("/speedtest")
def api_speedtest():
    """
    Ejecuta un test de velocidad local usando SpeedTest.py
    """
    try:
        resultado = run_speedtest()

        return {
            "status": "OK",
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "resultado": resultado
        }

    except Exception as e:
        Logs_Error.CapturarEvento("MainFlash", "speedtest", str(e))
        return {
            "status": "ERROR",
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "detalle": "Error al ejecutar SpeedTest.",
            "debug": str(e)
        }

# ======================================================
# HEALTH CHECK
# ======================================================
@app.get("/")
def estado():
    """
    Verifica que el servidor esté activo
    """
    return {
        "status": "Servidor activo",
        "version": "0.3.0",
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    }
