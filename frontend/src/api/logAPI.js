export async function guardarLogSolicitud(solicitud, ticket, tipo) {
  try {
    const logData = {
      solicitud,
      ticket,
      tipo_problema: tipo || "No especificado",
    };

    // Guardado local (navegador)
    const logs = JSON.parse(localStorage.getItem("logs_tecnicos") || "[]");
    const nuevoLog = {
      ...logData,
      fecha: new Date().toLocaleString("es-AR"),
      origen: "Diagnóstico de Red - DR.REDES D.C.V.",
    };
    logs.push(nuevoLog);
    localStorage.setItem("logs_tecnicos", JSON.stringify(logs));

    // Mostrar detalles del ticket en consola
    console.log(
      `✅ Log guardado localmente → Ticket #${ticket || "sin número"} (${tipo || "No especificado"})`
    );
    console.log("📋 Detalles:", nuevoLog);

    // 🔻 Desactivado: backend no tiene ese endpoint
    /*
    await fetch("http://127.0.0.1:8000/api/guardar_log", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(logData),
    });
    */

    return true;
  } catch (error) {
    console.error("❌ Error al guardar log:", error);
    return false;
  }
}
