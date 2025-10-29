from MotorInferencia import MotorInferencia
from Controller_Error import Logs_Error  # Para registrar errores
from ChatGemini import GeminiConnector   # Para usar Gemini si no hay coincidencias
from SpeedTest import SpeedTestConexion  # Prueba de velocidad (opcional)

def main():
    print("=== Diagnóstico de fallas en redes domésticas ===")
    print("Ingrese los hechos observables (responda con 'true' o 'false'):")

    try:
        # Entrada de hechos por consola
        hechos_dict = {
            "conexion_lenta": input("¿La conexión es lenta? ").strip().lower() == "true",
            "sin_internet": input("¿No hay acceso a Internet? ").strip().lower() == "true",
            "desconexion_intermittente": input("¿La conexión se cae intermitentemente? ").strip().lower() == "true",
            "solo_un_dispositivo_afectado": input("¿Solo un dispositivo está afectado? ").strip().lower() == "true",
            "router_luces_normales": input("¿Las luces del router son normales? ").strip().lower() == "true",
            "wifi_visible": input("¿El WiFi es visible desde el dispositivo? ").strip().lower() == "true",
            "router_encendido": input("¿El router está encendido? ").strip().lower() == "true",
            "cable_ethernet_usado": input("¿Está conectado por cable Ethernet? ").strip().lower() == "true",
            "firmware_router_actualizado": input("¿El router tiene el firmware actualizado? ").strip().lower() == "true",
            "otros_dispositivos_conectados": input("¿Hay otros dispositivos conectados a la red? ").strip().lower() == "true",
            "distancia_router_lejana": input("¿El dispositivo está lejos del router? ").strip().lower() == "true",
            "reinicio_router_reciente": input("¿El router se reinició recientemente? ").strip().lower() == "true",
            "drivers_red_ok": input("¿Los drivers de red están actualizados? ").strip().lower() == "true",
            "cable_ethernet_ok": input("¿El cable Ethernet está en buen estado? ").strip().lower() == "true",
            "adaptador_red_funcional": input("¿El adaptador de red funciona correctamente? ").strip().lower() == "true",
            "puerto_red_dispositivo_funcional": input("¿El puerto de red del dispositivo funciona? ").strip().lower() == "true",
            "repetidor_cubre_zona_ok": input("¿El repetidor cubre la zona correctamente? ").strip().lower() == "true"
        }

        # Crear motor de diagnóstico con el diccionario directamente
        motor = MotorInferencia(hechos_dict)

        # Ejecutar diagnóstico
        resultado = motor.diagnosticar()

        print("\n=== Resultado del diagnóstico ===")
        print("Causa probable:", resultado["causa_probable"])
        print("Sugerencias:")
        for sug in resultado["sugerencias"]:
            print("-", sug)

    except Exception as e:
        Logs_Error.CapturarEvento("MainTerminal", "main", str(e))
        print(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    main()
