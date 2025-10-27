import { useState } from "react";
import { ejecutarSpeedTest } from "../api/speedAPI";

export default function SpeedTestCard() {
  const [resultado, setResultado] = useState(null);

  async function ejecutar() {
    const data = await ejecutarSpeedTest();
    setResultado(data.resultado);
  }

  return (
    <div style={{ padding: 20 }}>
      <h3>SpeedTest</h3>

      <button onClick={ejecutar}>Ejecutar prueba</button>

      {resultado && (
        <div>
          <p>Ping: {resultado.ping} ms</p>
          <p>Bajada: {resultado.bajada} Mbps</p>
          <p>Subida: {resultado.subida} Mbps</p>
        </div>
      )}
    </div>
  );
}
