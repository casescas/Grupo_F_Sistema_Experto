from fastapi import FastAPI, Request
from Hechos import HechosObservables
from MotorInferencia import MotorInferencia
from Controller_Error import Logs_Error
from SpeedTest import run_speedtest
from fastapi.middleware.cors import CORSMiddleware
from ChatLocalLLM import LocalLLMConnector
import datetime
import requests

# ======================================================
# CONFIGURACIÓN FASTAPI
# ======================================================
app = FastAPI(
    title="Diagnóstico de fallas en redes domésticas - Sistema Experto",
    version="0.5.1",
    description="Alumnos: Cristian Couto, Valeria Villega, Diego Estrada"
)

# ======================================================
# CORS (Permite conexión desde React)
# ======================================================
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================================================
# FUNCIONES AUXILIARES
# ======================================================
def consultar_LMStudio(prompt: str):
    """
    Envía el prompt a LM Studio (puerto 1235)
    y devuelve una respuesta corta, clara y técnica (máx. 250 caracteres).
    """
    try:
        url = "http://127.0.0.1:1235/v1/chat/completions"
        payload = {
            "model": "meta-llama-3-8b-instruct",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "Sos un técnico especializado en diagnóstico de redes domésticas. "
                        "Tu respuesta debe ser breve, técnica y directa, sin enumeraciones ni explicaciones largas. "
                        "Usá un máximo de dos oraciones cortas, simples y fáciles de entender."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.4,
            "max_tokens": 120
        }

        response = requests.post(url, json=payload, timeout=20)
        if response.status_code == 200:
            data = response.json()
            texto = data["choices"][0]["message"]["content"].strip()

            # Limpieza y truncado
            texto = texto.replace("**", "").replace("\n", " ").strip()
            if len(texto) > 250:
                texto = texto[:247].rsplit(" ", 1)[0] + "..."
            return texto

        else:
            return f"⚠️ LM Studio devolvió error HTTP {response.status_code}"

    except Exception as e:
        Logs_Error.CapturarEvento("MainFlash", "consultar_LMStudio", str(e))
        return "⚠️ No se pudo conectar con LM Studio (puerto 1235)."

# ======================================================
# ENDPOINT: DIAGNÓSTICO PRINCIPAL
# ======================================================
@app.post("/diagnostico")
async def diagnostico(request: Request):
    try:
        hechos_dict = await request.json()

        motor = MotorInferencia(hechos_dict)
        resultado = motor.diagnosticar()

        # ✅ Si no se encontró regla, usar LM Studio
        if resultado["causa_probable"].startswith("No se pudo determinar"):
            prompt = f"""
Síntomas detectados en la red doméstica:
{hechos_dict}

Indicá en no más de dos oraciones:
1. La causa probable del problema.
2. Una acción concreta para solucionarlo.
"""
            respuesta_llm = consultar_LMStudio(prompt)
            resultado["causa_probable"] = "Diagnóstico asistido por IA"
            resultado["sugerencias"] = [respuesta_llm]

        return {
            "status": "OK",
            "diagnostico": resultado
        }

    except Exception as e:
        Logs_Error.CapturarEvento("MainFlash", "diagnostico", str(e))
        return {
            "status": "ERROR",
            "detalle": "Error al evaluar diagnóstico.",
            "debug": str(e)
        }

# ======================================================
# ENDPOINT: SPEEDTEST
# ======================================================
@app.get("/speedtest")
def api_speedtest():
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
    return {
        "status": "Servidor activo",
        "version": "0.5.1",
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

# ======================================================
# EJECUCIÓN DIRECTA (arranque del servidor)
# ======================================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("MainFlash:app", host="127.0.0.1", port=5000, reload=True)
