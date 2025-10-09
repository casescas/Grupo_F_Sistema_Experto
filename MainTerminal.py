from Hechos import HechosObservables
from MotorInferencia import MotorDiagnosticoDesdeArchivo

def main():
    print("=== Diagnóstico de fallas en redes domésticas ===")
    print("Ingrese los hechos observables (responda con 'true' o 'false'):")

    # Simulación de entrada de hechos por consola
    hechos_dict = {
        "conexion_lenta": input("¿La conexión es lenta? ").strip().lower() == "true",
        "sin_internet": input("¿No hay acceso a Internet? ").strip().lower() == "v",
        "desconexion_intermittente": input("¿La conexión se cae intermitentemente? ").strip().lower() == "true",
        "otros_dispositivos_conectados": input("¿Hay otros dispositivos conectados? ").strip().lower() == "true",
        "router_luces_normales": input("¿Las luces del router son normales? ").strip().lower() == "true",
        "wifi_visible": input("¿El WiFi es visible desde el dispositivo? ").strip().lower() == "true"
    }

    # Crear instancia de hechos
    hechos = HechosObservables(**hechos_dict)

    # Crear motor de diagnóstico
    motor = MotorDiagnosticoDesdeArchivo(hechos)

    # Ejecutar diagnóstico
    resultado = motor.diagnosticar()

    print("\n=== Resultado del diagnóstico ===")
    print(resultado)

if __name__ == "__main__":
    main()
