import axios from "axios";

export async function diagnosticar(hechos) {
  const { data } = await axios.post("http://127.0.0.1:8000/diagnostico", hechos);
  return data;
}
