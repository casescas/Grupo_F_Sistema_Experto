import axios from "axios";

export async function ejecutarSpeedTest() {
  try {
    const { data } = await axios.get("http://127.0.0.1:8000/speedtest");

    // 👇 Asegura que "resultado" sea un objeto y no texto plano
    if (typeof data.resultado === "string") {
      data.resultado = JSON.parse(data.resultado);
    }

    return data.resultado; // => { ping: 55.57, bajada: 21.63, subida: 2.44 }
  } catch (error) {
    console.error("Error en ejecutarSpeedTest:", error);
    throw error;
  }
}
