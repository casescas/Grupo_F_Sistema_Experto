import axios from "axios";

export async function ejecutarSpeedTest() {
  const { data } = await axios.get("http://127.0.0.1:8000/speedtest");
  return data;
}
