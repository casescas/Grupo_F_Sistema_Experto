// ============================================================
// log_server.js — Servidor simple para guardar logs en JSON
// ============================================================

import express from "express";
import fs from "fs";
import path from "path";
import cors from "cors";

const app = express();
app.use(cors());
app.use(express.json());

const LOG_PATH = path.join(process.cwd(), "logs", "solicitudes.json");

// Asegura que exista la carpeta /logs
fs.mkdirSync(path.dirname(LOG_PATH), { recursive: true });

// ============================================================
// Ruta principal para guardar logs
// ============================================================
app.post("/api/logs", (req, res) => {
  const logData = req.body;

  if (!logData.ticket || !logData.descripcion) {
    return res.status(400).json({ error: "Datos incompletos" });
  }

  let logs = [];
  if (fs.existsSync(LOG_PATH)) {
    logs = JSON.parse(fs.readFileSync(LOG_PATH, "utf-8"));
  }

  logs.push({
    ...logData,
    fecha: new Date().toLocaleString("es-AR"),
  });

  fs.writeFileSync(LOG_PATH, JSON.stringify(logs, null, 2));
  console.log("🟣 Nuevo log guardado:", logData);

  res.json({ message: "Log guardado correctamente" });
});

// ============================================================
// Servidor activo
// ============================================================
const PORT = 5000;
app.listen(PORT, () =>
  console.log(`🟢 Servidor de logs activo en http://localhost:${PORT}`)
);
