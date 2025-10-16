# --------------------------------------------------------
# CONFIGURACIÓN CENTRAL DEL SISTEMA EXPERTO
# --------------------------------------------------------
# Este módulo maneja:
# - Variables de configuración (nombre de la app, rutas base, orígenes permitidos)
# - Lectura del archivo .env
# - Cacheo de la configuración para evitar recargarla varias veces
# --------------------------------------------------------

from functools import lru_cache        # Decorador para guardar en caché funciones (evita recalcular)
from pydantic_settings import BaseSettings  # Nuevo import - Clase que permite leer variables de entorno automáticamente
from typing import List                # Para declarar listas tipadas
import os                              # Para operaciones básicas con el sistema

# --------------------------------------------------------
# Clase principal de configuración
# --------------------------------------------------------
class Settings(BaseSettings):
    # Nombre de la aplicación, visible en los títulos y documentación
    APP_NAME: str = "Expertito Wi-Fi"

    # Prefijo general para los endpoints de la API
    API_V1_STR: str = "/api"

    # Lista de orígenes permitidos para CORS (Cross-Origin Resource Sharing)
    # Es necesaria para que el frontend (por ejemplo, Vite o React) pueda acceder al backend FastAPI
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",   # Frontend local (Vite)
        "http://127.0.0.1:5173",   # Alternativa del localhost
    ]

    # Configuración interna de Pydantic
    class Config:
        env_file = ".env"           # Archivo donde guardamos variables de entorno (por ejemplo claves o URLs)
        env_file_encoding = "utf-8" # Codificación estándar para evitar errores con caracteres especiales


# --------------------------------------------------------
# Función cacheada para obtener una única instancia de Settings
# --------------------------------------------------------
@lru_cache()
def get_settings() -> Settings:
    """
    Devuelve una instancia única (cacheada) de la clase Settings.
    Esto evita volver a cargar las configuraciones cada vez que se llama.
    """
    return Settings()


# --------------------------------------------------------
# Función de ayuda para obtener las URLs permitidas por CORS
# --------------------------------------------------------
def get_cors_origins() -> List[str]:
    """
    Devuelve la lista de orígenes permitidos para solicitudes desde el frontend.
    """
    s = get_settings()       # Obtiene la configuración actual
    return s.CORS_ORIGINS    # Retorna la lista de URLs permitidas
