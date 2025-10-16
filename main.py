# --------------------------------------------------------
# ARCHIVO PRINCIPAL DE INICIO (main.py)
# --------------------------------------------------------
# Aquí se crea la aplicación FastAPI, se configura CORS,
# y se incluyen los routers (rutas) del sistema experto.
# --------------------------------------------------------

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_cors_origins, get_settings
from app.routers import diagnostico

# --------------------------------------------------------
# 1. Inicializar la configuración global
# --------------------------------------------------------
settings = get_settings()  # Cargamos las configuraciones desde config.py

# --------------------------------------------------------
# 2. Crear la instancia principal de la aplicación
# --------------------------------------------------------
app = FastAPI(
    title=settings.APP_NAME,  # Nombre visible en Swagger UI
    version="0.1.0"           # Versión de la API
)

# --------------------------------------------------------
# 3. Configurar CORS (permite que el frontend acceda al backend)
# --------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),  # Lista de orígenes permitidos (por ejemplo, localhost:5173)
    allow_credentials=True,            # Permite envío de cookies y autenticación si se necesita
    allow_methods=["*"],               # Permite todos los métodos HTTP (GET, POST, PUT, DELETE)
    allow_headers=["*"],               # Permite todos los encabezados personalizados
)

# --------------------------------------------------------
# 4. Incluir los routers (rutas de la API)
# --------------------------------------------------------
app.include_router(diagnostico.router)  # Conecta /diagnostico/health (y luego /diagnosticar)

# --------------------------------------------------------
# 5. Endpoint raíz para verificar que la API está viva
# --------------------------------------------------------
@app.get("/")
def root():
    """
    Endpoint raíz del sistema. Devuelve el estado general de la API.
    """
    return {"app": settings.APP_NAME, "status": "running"}
