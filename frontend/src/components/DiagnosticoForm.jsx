import { useState } from "react";
import { diagnosticar } from "../api/diagnosticoAPI";
import { ejecutarSpeedTest } from "../api/speedAPI";

const card = {
  maxWidth: 820,
  margin: "0 auto",
  padding: 24,
  borderRadius: 14,
  boxShadow: "0 10px 25px rgba(0,0,0,.08)",
  background: "#fff",
};

const row = {
  display: "grid",
  gridTemplateColumns: "1fr 1fr",
  gap: 14,
  alignItems: "center",
};

const label = { textAlign: "right", fontWeight: 600 };
const select = { padding: 8, borderRadius: 10, border: "1px solid #ddd" };
const chipWrap = { display: "flex", gap: 8, flexWrap: "wrap" };

const chip = (active) => ({
  padding: "8px 12px",
  borderRadius: 999,
  border: `1px solid ${active ? "#2563eb" : "#ddd"}`,
  background: active ? "#e8f0ff" : "#fff",
  color: active ? "#1e3a8a" : "#222",
  cursor: "pointer",
  userSelect: "none",
  fontSize: 14,
});

const Divider = () => (
  <hr style={{ border: 0, borderTop: "1px solid #eee", margin: "18px 0" }} />
);

export default function DiagnosticoForm() {
  const [tipo, setTipo] = useState("");
  const [hechos, setHechos] = useState({});
  const [resultado, setResultado] = useState(null);
  const [loadingDiag, setLoadingDiag] = useState(false);
  const [payloadDebug, setPayloadDebug] = useState(null);

  const setBoolChip = (campo, val) => {
    setHechos((prev) => ({ ...prev, [campo]: val }));
  };

  const enviar = async () => {
    setLoadingDiag(true);
    setResultado(null);

    const hechosConTipo = { ...hechos };

    if (tipo === "sin_internet") hechosConTipo.sin_internet = true;
    if (tipo === "lento") hechosConTipo.conexion_lenta = true;
    if (tipo === "cortes") hechosConTipo.desconexion_intermittente = true;
    if (tipo === "wifi") hechosConTipo.wifi_visible = false;

    setPayloadDebug(hechosConTipo);

    try {
      const data = await diagnosticar(hechosConTipo);
      setResultado(data?.diagnostico ?? null);
    } finally {
      setLoadingDiag(false);
    }
  };

  const limpiar = () => {
    setTipo("");
    setHechos({});
    setResultado(null);
    setPayloadDebug(null);
  };

  return (
    <div style={{ ...card }}>
      <h2 style={{ textAlign: "center", marginTop: 0 }}>
        Diagnóstico de Red Doméstica
      </h2>

      <div style={row}>
        <div style={label}>Síntoma principal</div>
        <select
          style={select}
          value={tipo}
          onChange={(e) => setTipo(e.target.value)}
        >
          <option value="">¿Cuál es el problema?</option>
          <option value="sin_internet">No tengo internet</option>
          <option value="lento">Internet lento</option>
          <option value="cortes">Cortes intermitentes</option>
          <option value="wifi">Problemas con WiFi</option>
        </select>
      </div>

      {/* SIN INTERNET */}
      {tipo === "sin_internet" && (
        <>
          <Divider />
          <div style={row}>
            <div style={label}>Router con luces normales</div>
            <div style={chipWrap}>
              <div
                style={chip(hechos.router_luces_normales === true)}
                onClick={() => setBoolChip("router_luces_normales", true)}
              >Sí</div>
              <div
                style={chip(hechos.router_luces_normales === false)}
                onClick={() => setBoolChip("router_luces_normales", false)}
              >No</div>
            </div>
          </div>

          <div style={row}>
            <div style={label}>WiFi visible</div>
            <div style={chipWrap}>
              <div
                style={chip(hechos.wifi_visible === true)}
                onClick={() => setBoolChip("wifi_visible", true)}
              >Sí</div>
              <div
                style={chip(hechos.wifi_visible === false)}
                onClick={() => setBoolChip("wifi_visible", false)}
              >No</div>
            </div>
          </div>
        </>
      )}

      {/* INTERNET LENTO */}
      {tipo === "lento" && (
        <>
          <Divider />

          <button
            onClick={async () => {
              const data = await ejecutarSpeedTest();
              setHechos((prev) => ({
                ...prev,
                velocidad_bajada_mbps: data.resultado.bajada,
                velocidad_ping_ms: data.resultado.ping,
              }));
            }}
            style={{
              padding: "8px 12px",
              borderRadius: 8,
              background: "#2563eb",
              color: "#fff",
              marginBottom: 12,
            }}
          >
            Medir velocidad ahora
          </button>

          <div style={row}>
            <div style={label}>Velocidad detectada</div>
            <div>{hechos.velocidad_bajada_mbps ?? "—"} Mbps</div>
          </div>

          <div style={row}>
            <div style={label}>Ping detectado</div>
            <div>{hechos.velocidad_ping_ms ?? "—"} ms</div>
          </div>

          <div style={row}>
            <div style={label}>Muchos dispositivos conectados</div>
            <div style={chipWrap}>
              <div
                style={chip(hechos.otros_dispositivos_conectados === true)}
                onClick={() =>
                  setBoolChip("otros_dispositivos_conectados", true)
                }
              >Sí</div>
              <div
                style={chip(hechos.otros_dispositivos_conectados === false)}
                onClick={() =>
                  setBoolChip("otros_dispositivos_conectados", false)
                }
              >No</div>
            </div>
          </div>
        </>
      )}

      {/* CORTES */}
      {tipo === "cortes" && (
        <>
          <Divider />
          <div style={row}>
            <div style={label}>¿Desconexión intermitente?</div>
            <div style={chipWrap}>
              <div
                style={chip(hechos.desconexion_intermittente === true)}
                onClick={() => setBoolChip("desconexion_intermittente", true)}
              >Sí</div>
              <div
                style={chip(hechos.desconexion_intermittente === false)}
                onClick={() => setBoolChip("desconexion_intermittente", false)}
              >No</div>
            </div>
          </div>
        </>
      )}

      {/* WIFI */}
      {tipo === "wifi" && (
        <>
          <Divider />
          <div style={row}>
            <div style={label}>WiFi visible</div>
            <div style={chipWrap}>
              <div
                style={chip(hechos.wifi_visible === true)}
                onClick={() => setBoolChip("wifi_visible", true)}
              >Sí</div>
              <div
                style={chip(hechos.wifi_visible === false)}
                onClick={() => setBoolChip("wifi_visible", false)}
              >No</div>
            </div>
          </div>
        </>
      )}

      <Divider />

      <div style={{ display: "flex", gap: 10, justifyContent: "center" }}>
        <button
          onClick={enviar}
          disabled={loadingDiag || !tipo}
          style={{
            padding: "10px 16px",
            borderRadius: 10,
            border: "1px solid #2563eb",
            background: "#2563eb",
            color: "#fff",
          }}
        >
          {loadingDiag ? "Diagnosticando..." : "Diagnosticar"}
        </button>

        <button
          onClick={limpiar}
          style={{
            padding: "10px 16px",
            borderRadius: 10,
            border: "1px solid #ddd",
            background: "#f8f9fb",
          }}
        >
          Reiniciar
        </button>
      </div>

      {resultado && (
        <div style={{ marginTop: 22 }}>
          <Divider />

          <h4>Causa probable</h4>
          <div style={{ fontWeight: 700 }}>
            {resultado.causa_probable}
          </div>

          <h4>Sugerencias</h4>

          {/* Evita error .map */}
          {Array.isArray(resultado.sugerencias) ? (
            <ul>
              {resultado.sugerencias.map((s, i) => (
                <li key={i}>{s}</li>
              ))}
            </ul>
          ) : typeof resultado.sugerencias === "string" ? (
            <p>{resultado.sugerencias}</p>
          ) : (
            <p>No se proporcionaron sugerencias.</p>
          )}

          {resultado.IMPORTANTE && (
            <>
              <h4>Asistencia IA</h4>
              <p>{resultado.IMPORTANTE[1]}</p>
            </>
          )}
        </div>
      )}

      {payloadDebug && (
        <details style={{ marginTop: 16 }}>
          <summary>Payload enviado (debug)</summary>
          <pre>{JSON.stringify(payloadDebug, null, 2)}</pre>
        </details>
      )}
    </div>
  );
}
