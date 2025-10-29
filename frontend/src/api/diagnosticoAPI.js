import axios from "axios";

// Función que envía los datos del formulario al backend FastAPI
export async function diagnosticar(hechos) {
  try {
    const { data } = await axios.post("http://127.0.0.1:8000/diagnostico", hechos);
    return data;
  } catch (error) {
    console.error("Error en la solicitud de diagnóstico:", error);
    throw error;
  }
}
