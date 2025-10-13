# 💻 Trabajo Práctico 4: Sistema Experto para Diagnóstico de Fallas en Redes Domésticas

### Materia: Desarrollo de Sistemas IA
### Profesor: Prof. Horacio Bogarín
### Grupo F: Cristian Couto, Valeria Villega, Estrada Diego

---

## 💡 Contexto del Proyecto

Este proyecto consiste en el desarrollo de un **Sistema Experto** diseñado para asistir a los usuarios domésticos en la **detección y diagnóstico de problemas de conectividad de red** (Internet lento, desconexiones, fallas de equipos, etc.).

El sistema está enfocado en identificar fallas comunes que involucran:
* **Cableado (Ethernet)**
* **Conexión Inalámbrica (Wi-Fi)**
* **Dispositivos de Red (Router)**
* **Fallas del Proveedor de Servicios de Internet (ISP)**

## 🎯 Objetivos de la Implementación

Los objetivos principales definidos para este trabajo práctico son:

* **Definición de Hechos Observables:** Establecer una base de conocimiento clara sobre los síntomas reportados por el usuario (ej: conexión lenta, ausencia total de Internet, desconexión intermitente) para que sirvan como entradas al sistema.
* **Creación de la Base de Reglas:** Implementar reglas lógicas (motores de inferencia) para que el sistema experto pueda correlacionar los síntomas (hechos) con la causa probable de la falla.
* **Implementación de un Endpoint (FastAPI):** Desarrollar una API utilizando FastAPI para exponer la lógica de diagnóstico, permitiendo pruebas y la integración con diversos dispositivos y clientes.

## 🚀 Desafío Adicional (Valor Agregado)

El desafío principal que abordará este sistema experto es:

> **Generar Sugerencias de Resolución Paso a Paso.**
>
> El sistema no solo debe identificar la causa probable, sino también proporcionar al usuario una **guía práctica y detallada** de acciones que puede tomar para resolver el problema (ej: "Paso 1: Reinicie el router. Paso 2: Verifique las luces indicadoras...").

---

## 🛠️ Tecnologías Utilizadas

| Componente | Tecnología | Descripción |
| :--- | :--- | :--- |
| **Backend/API** | Python | Lenguaje de programación principal. |
| **Framework Web** | FastAPI | Para la construcción del endpoint rápido y robusto. |
| **Sistema Experto** | (A definir, ej: Clips, Python-based Engine, o lógica condicional propia) | Motor de inferencia para el diagnóstico. |

## ⚙️ Uso e Instalación (Ejemplo)

Para correr y probar la API localmente:

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://aws.amazon.com/es/what-is/repo/](https://aws.amazon.com/es/what-is/repo/)
    cd trabajo-practico-4-diagnostico
    ```

2.  **Crear y activar un entorno virtual (Recomendado):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Linux/macOS
    # o .\venv\Scripts\activate.bat  # En Windows
    ```

3.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Iniciar el servidor FastAPI:**
    ```bash
    uvicorn main:app --reload
    ```
    *La API estará disponible en `http://127.0.0.1:8000`*

## 💡 Endpoint Principal de Diagnóstico

* **URL:** `/api/diagnostico/`
* **Método:** `POST`
* **Cuerpo (Ejemplo):**
    ```json
    {
      "sintomas": [
        "conexion_lenta",
        "luces_router_parpadean_rojo"
      ]
    }
    ```
* **Respuesta (Ejemplo):**
    ```json
    {
      "causa_probable": "Problema de saturación en el proveedor (ISP)",
      "sugerencias_resolucion": [
        "Paso 1: Intente reiniciar el modem y el router.",
        "Paso 2: Realice una prueba de velocidad en un sitio oficial.",
        "Paso 3: Contacte al soporte técnico de su proveedor con los resultados."
      ]
    }
    ```
