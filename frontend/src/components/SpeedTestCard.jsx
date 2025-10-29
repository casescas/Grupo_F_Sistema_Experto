import { ejecutarSpeedTest } from "../api/speedAPI";
import { useState } from "react";

export default function SpeedTestCard() {
  const [resultado, setResultado] = useState(null);
  const [cargando, setCargando] = useState(false);

  const ejecutar = async () => {
    try {
      setCargando(true);
      const data = await ejecutarSpeedTest();
      setResultado(data);
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setCargando(false);
    }
  };

  return (
    <div className="p-4 bg-gray-100 rounded-xl shadow-md">
      <h2 className="text-xl font-bold text-gray-700 mb-3">SpeedTest</h2>
      <button
        onClick={ejecutar}
        disabled={cargando}
        className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
      >
        {cargando ? "Midiendo..." : "Ejecutar SpeedTest"}
      </button>

      {resultado && (
        <div className="mt-4 text-gray-800">
          <p>Ping: {resultado.ping} ms</p>
          <p>Bajada: {resultado.bajada} Mbps</p>
          <p>Subida: {resultado.subida} Mbps</p>
        </div>
      )}
    </div>
  );
}
