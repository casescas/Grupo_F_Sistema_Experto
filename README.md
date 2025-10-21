## Trabajo Práctico 4 — Diagnóstico de fallas en redes domésticas
### Materia: Desarrollo de Sistema IA - Prof. Horacio Bogarin
### Grupo F: Cristian Couto, Valeria Villegas, Estrada Diego

# 🧠 Sistema Experto de Diagnóstico Wi-Fi — Rama `valeria-dev2`

## 📋 Contexto general
El proyecto forma parte del desarrollo del **Sistema Experto de Diagnóstico de Redes Wi-Fi Domésticas**, cuyo propósito es ofrecer un diagnóstico automático de fallas de conectividad y sugerir soluciones personalizadas al usuario final.

La rama **`valeria-dev2`** se centró en la **reorganización del entorno backend**, la **limpieza del repositorio** y la **preparación de la estructura base para el futuro desarrollo del frontend (UI)**.

---

## ⚠️ Problema detectado
Durante la revisión inicial del repositorio se identificaron varios inconvenientes:

- Existencia de carpetas y archivos innecesarios (`venv/`, `__pycache__/`, `.vscode/`) que aumentaban el peso y el desorden del proyecto.  
- Estructura de directorios poco clara para continuar con el desarrollo del frontend.  
- Dificultades al levantar el servidor local en `localhost:8000` por conflictos de entorno.  

Estos problemas complicaban la colaboración entre los integrantes del grupo y la integración futura de módulos nuevos.

---

## 🎯 Objetivo principal
Organizar el entorno del proyecto para dejar una **base estable, limpia y funcional** que permita avanzar con el desarrollo de la interfaz de usuario y la conexión con la API del sistema experto.

---

## 🧩 Proceso realizado

1. **Revisión de la estructura existente**: se analizaron las carpetas y dependencias del entorno.  
2. **Eliminación de archivos innecesarios**: se quitaron directorios locales que no deben incluirse en el control de versiones (`venv/`, `.vscode/`, `__pycache__/`).  
3. **Reorganización del proyecto**: se agruparon los módulos de lógica, reglas y utilidades dentro del backend.  
4. **Verificación del servidor local**: se comprobó la ejecución correcta del entorno FastAPI y se registraron ajustes en `requirements.txt`.  
5. **Preparación para UI**: se definió la estructura inicial para integrar React y vincularlo con la API.

---

## 🗂️ Nueva estructura del proyecto

Grupo_F_Sistema_Experto/
│
├── backend/
│ ├── main.py
│ ├── api/
│ ├── rules/
│ ├── utils/
│ └── requirements.txt
│
├── frontend/
│ └── (en desarrollo)
│
├── docs/
│ └── README_valeria-dev2.md
│
└── tests/


---

## 🚀 Próximos pasos

- Iniciar el desarrollo de la **interfaz de usuario (UI)** en React.  
- Conectar los módulos del backend con la UI mediante API REST.  
- Documentar los endpoints y flujos de diagnóstico para la interfaz.  
- Realizar pruebas integradas de conexión y respuesta del sistema experto.  

---

## 👩‍💻 Autora y contribuciones

**Valeria Villegas**  
Rama: `valeria-dev2`  
Proyecto colaborativo — *Grupo F, Tecnicatura Superior en Ciencia de Datos e Inteligencia Artificial*  
**Instituto Politécnico Malvinas Argentinas — Tierra del Fuego, Argentina**

---

📅 *Documento actualizado: Octubre 2025*


