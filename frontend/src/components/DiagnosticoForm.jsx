import { useState } from "react";
import { diagnosticar } from "../api/diagnosticoAPI";
import { ejecutarSpeedTest } from "../api/speedAPI"; // puede quedar importado
import { guardarLogSolicitud } from "../api/logAPI";

const card = {
  maxWidth: 1100,
  margin: "0 auto",
  padding: 24,
  borderRadius: 14,
  boxShadow: "0 10px 25px rgba(0,0,0,.08)",
  background: "#2d2541",
  color: "#fff",
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
  // ====== ESTADO EXISTENTE ======
  const [tipo, setTipo] = useState("");
  const [hechos, setHechos] = useState({});
  const [resultado, setResultado] = useState(null);
  const [loadingDiag, setLoadingDiag] = useState(false);
  const [payloadDebug, setPayloadDebug] = useState(null);

  // ====== SOLICITUD TÉCNICA (aislado) ======
  const [mostrarSolicitud, setMostrarSolicitud] = useState(false);
  const [solicitud, setSolicitud] = useState("");
  const [ticket, setTicket] = useState(null);

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
    if (tipo === "wifi") hechosConTipo.problemas_wifi = true;

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
    setSolicitud("");
    setTicket(null);
    setMostrarSolicitud(false);
  };

  const enviarSolicitud = () => {
    if (!solicitud.trim()) {
      alert("Por favor describí el problema antes de enviar.");
      return;
    }
    const numero = Math.floor(Math.random() * 9000 + 1000);
    const tkt = `TKT-${numero}`;
    setTicket(tkt);
    guardarLogSolicitud(solicitud, tkt, tipo);

  };

  return (
    <div style={{ ...card }}>
      {/* === LOGO DR. REDES D.C.V (solo visual) === */}
      <div style={{ textAlign: "center", marginBottom: 20 }}>
        <img
          src="/logo_drredes.png"
          alt="Logo DR. REDES D.C.V"
          style={{
            width: 150,
            marginBottom: 8,
            filter: "drop-shadow(0 0 10px rgba(155, 89, 182, 0.55))",
          }}
        />
        <h2 style={{ color: "#c4b5fd", margin: 0, fontSize: 20 }}>
          DR. REDES - D.C.V
        </h2>
        <p
          style={{
            fontSize: 12,
            letterSpacing: 1.5,
            color: "#a78bfa",
            margin: 0,
          }}
        >
          SISTEMA EXPERTO DE DIAGNÓSTICO DE FALLAS
        </p>
        <Divider />
      </div>

      <h3 style={{ textAlign: "center", marginTop: 0 }}>
        Diagnóstico de Red Doméstica
      </h3>

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
          <option value="wifi">Problemas de WiFi</option>
        </select>
      </div>

      {/* === NO TENGO INTERNET === */}
      {tipo === "sin_internet" && (
        <>
          <Divider />
          <div style={row}>
            <div style={label}>¿Todas las luces del router encendidas?</div>
            <div style={chipWrap}>
              <div
                style={chip(hechos.router_luces_todas === true)}
                onClick={() => setBoolChip("router_luces_todas", true)}
              >
                Sí
              </div>
              <div
                style={chip(hechos.router_luces_todas === false)}
                onClick={() => setBoolChip("router_luces_todas", false)}
              >
                No
              </div>
            </div>
          </div>

          <div style={row}>
            <div style={label}>¿Otros dispositivos sin internet?</div>
            <div style={chipWrap}>
              <div
                style={chip(hechos.otros_sin_internet === true)}
                onClick={() => setBoolChip("otros_sin_internet", true)}
              >
                Sí
              </div>
              <div
                style={chip(hechos.otros_sin_internet === false)}
                onClick={() => setBoolChip("otros_sin_internet", false)}
              >
                No
              </div>
            </div>
          </div>

          <div style={row}>
            <div style={label}>¿Reiniciaste el router recientemente?</div>
            <div style={chipWrap}>
              <div
                style={chip(hechos.reinicio_router_reciente === true)}
                onClick={() => setBoolChip("reinicio_router_reciente", true)}
              >
                Sí
              </div>
              <div
                style={chip(hechos.reinicio_router_reciente === false)}
                onClick={() => setBoolChip("reinicio_router_reciente", false)}
              >
                No
              </div>
            </div>
          </div>
        </>
      )}

      {/* === INTERNET LENTO (sin SpeedTest) === */}
      {tipo === "lento" && (
        <>
          <Divider />
          <div style={row}>
            <div style={label}>¿Muchos dispositivos conectados?</div>
            <div style={chipWrap}>
              <div
                style={chip(hechos.otros_dispositivos_conectados === true)}
                onClick={() =>
                  setBoolChip("otros_dispositivos_conectados", true)
                }
              >
                Sí
              </div>
              <div
                style={chip(hechos.otros_dispositivos_conectados === false)}
                onClick={() =>
                  setBoolChip("otros_dispositivos_conectados", false)
                }
              >
                No
              </div>
            </div>
          </div>

          <div style={row}>
            <div style={label}>¿Lentitud al ver videos o streaming?</div>
            <div style={chipWrap}>
              <div
                style={chip(hechos.streaming_lento === true)}
                onClick={() => setBoolChip("streaming_lento", true)}
              >
                Sí
              </div>
              <div
                style={chip(hechos.streaming_lento === false)}
                onClick={() => setBoolChip("streaming_lento", false)}
              >
                No
              </div>
            </div>
          </div>
        </>
      )}

      {/* === CORTES INTERMITENTES === */}
      {tipo === "cortes" && (
        <>
          <Divider />
          <div style={row}>
            <div style={label}>¿Los cortes ocurren solo por WiFi?</div>
            <div style={chipWrap}>
              <div
                style={chip(hechos.cortes_wifi_solo === true)}
                onClick={() => setBoolChip("cortes_wifi_solo", true)}
              >
                Sí
              </div>
              <div
                style={chip(hechos.cortes_wifi_solo === false)}
                onClick={() => setBoolChip("cortes_wifi_solo", false)}
              >
                No
              </div>
            </div>
          </div>

          <div style={row}>
            <div style={label}>¿Sucede principalmente en horarios pico?</div>
            <div style={chipWrap}>
              <div
                style={chip(hechos.horario_pico === true)}
                onClick={() => setBoolChip("horario_pico", true)}
              >
                Sí
              </div>
              <div
                style={chip(hechos.horario_pico === false)}
                onClick={() => setBoolChip("horario_pico", false)}
              >
                No
              </div>
            </div>
          </div>
        </>
      )}

      {/* === PROBLEMAS DE WIFI === */}
      {tipo === "wifi" && (
        <>
          <Divider />
          <div style={row}>
            <div style={label}>¿El WiFi se desconecta frecuentemente?</div>
            <div style={chipWrap}>
              <div
                style={chip(hechos.wifi_se_cae === true)}
                onClick={() => setBoolChip("wifi_se_cae", true)}
              >
                Sí
              </div>
              <div
                style={chip(hechos.wifi_se_cae === false)}
                onClick={() => setBoolChip("wifi_se_cae", false)}
              >
                No
              </div>
            </div>
          </div>

          <div style={row}>
            <div style={label}>¿No aparece tu red WiFi en la lista?</div>
            <div style={chipWrap}>
              <div
                style={chip(hechos.wifi_no_visible === true)}
                onClick={() => setBoolChip("wifi_no_visible", true)}
              >
                Sí
              </div>
              <div
                style={chip(hechos.wifi_no_visible === false)}
                onClick={() => setBoolChip("wifi_no_visible", false)}
              >
                No
              </div>
            </div>
          </div>

          <div style={row}>
            <div style={label}>¿Funciona bien cerca del router?</div>
            <div style={chipWrap}>
              <div
                style={chip(hechos.funciona_cerca === true)}
                onClick={() => setBoolChip("funciona_cerca", true)}
              >
                Sí
              </div>
              <div
                style={chip(hechos.funciona_cerca === false)}
                onClick={() => setBoolChip("funciona_cerca", false)}
              >
                No
              </div>
            </div>
          </div>

          <div style={row}>
            <div style={label}>¿Otros dispositivos también presentan cortes?</div>
            <div style={chipWrap}>
              <div
                style={chip(hechos.otros_cortes_wifi === true)}
                onClick={() => setBoolChip("otros_cortes_wifi", true)}
              >
                Sí
              </div>
              <div
                style={chip(hechos.otros_cortes_wifi === false)}
                onClick={() => setBoolChip("otros_cortes_wifi", false)}
              >
                No
              </div>
            </div>
          </div>
        </>
      )}

      <Divider />

      {/* === BOTONES PRINCIPALES === */}
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
            color: "#000",
            fontWeight: 500,
            background: "#f8f9fb",
          }}
        >
          Reiniciar
        </button>
      </div>

      {/* === RESULTADOS === */}
      {resultado && (
        <div style={{ marginTop: 22 }}>
          <Divider />
          <h4>Causa probable</h4>
          <div style={{ fontWeight: 700 }}>{resultado.causa_probable}</div>

          <h4>Sugerencias</h4>
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
        </div>
      )}

      {/* === SOLICITUD TÉCNICA (plegable) === */}
      <Divider />
      <div style={{ textAlign: "center", marginBottom: 10 }}>
        <button
          onClick={() => setMostrarSolicitud((v) => !v)}
          style={{
            padding: "10px 20px",
            borderRadius: 10,
            border: "1px solid #8b5cf6",
            background: mostrarSolicitud ? "#7c3aed" : "#8b5cf6",
            color: "#fff",
            fontWeight: 600,
            cursor: "pointer",
          }}
        >
          {mostrarSolicitud ? "Ocultar solicitud" : "Solicitud técnica"}
        </button>
      </div>

      {mostrarSolicitud && (
        <>
          <h4 style={{ textAlign: "center" }}>Solicitar Asistencia Técnica</h4>
          <textarea
            placeholder="Describí brevemente el problema para enviar al técnico..."
            value={solicitud}
            onChange={(e) => setSolicitud(e.target.value)}
            style={{
              width: "100%",
              height: 90,
              borderRadius: 10,
              border: "1px solid #ccc",
              padding: 10,
              resize: "none",
              marginBottom: 10,
              color: "#fff",
              background: "#3b2e5a",
            }}
          />
          <div style={{ textAlign: "center" }}>
            <button
              onClick={enviarSolicitud}
              style={{
                padding: "10px 20px",
                borderRadius: 10,
                border: "none",
                background: "#8b5cf6",
                color: "#fff",
                fontWeight: 600,
                cursor: "pointer",
              }}
            >
              Enviar solicitud
            </button>
          </div>

          {ticket && (
            <div style={{ marginTop: 20, textAlign: "center" }}>
              <h4>✅ Solicitud enviada</h4>
              <p>
                Tu número de ticket es: <strong>{ticket}</strong>
              </p>
              <p>
                Un técnico se comunicará con vos al siguiente contacto:
                <br />
                <a
                  href="https://wa.me/5492964654321"
                  target="_blank"
                  rel="noreferrer"
                  style={{ color: "#4ade80", fontWeight: "bold" }}
                >
                  WhatsApp Técnico - 2964 654321
                </a>
              </p>
            </div>
          )}
        </>
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
