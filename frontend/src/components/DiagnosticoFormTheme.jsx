import { useState } from "react";
import { diagnosticar } from "../api/diagnosticoAPI";
import { ejecutarSpeedTest } from "../api/speedAPI";
import theme from "../theme/uiTheme";

const card = {
  maxWidth: 820,
  margin: "0 auto",
  padding: 28,
  borderRadius: theme.card.borderRadius,
  boxShadow: theme.card.boxShadow,
  background: theme.colors.card,
  color: theme.colors.textPrimary,
};

const row = {
  display: "grid",
  gridTemplateColumns: "1fr 1fr",
  gap: 14,
  alignItems: "center",
};

const label = {
  textAlign: "right",
  fontWeight: 600,
  color: theme.colors.textSecondary,
};

const select = {
  padding: 10,
  borderRadius: 10,
  border: `1px solid ${theme.colors.border}`,
  fontSize: 15,
  backgroundColor: "#fff",
  cursor: "pointer",
};

const chipWrap = { display: "flex", gap: 8, flexWrap: "wrap" };

const chip = (active) => ({
  padding: "8px 14px",
  borderRadius: 999,
  border: `1px solid ${active ? theme.colors.primary : theme.colors.border}`,
  background: active ? theme.colors.accent + "20" : "#fff",
  color: active ? theme.colors.primary : theme.colors.textPrimary,
  cursor: "pointer",
  userSelect: "none",
  fontSize: 14,
  transition: "0.2s all",
});

const Divider = () => (
  <hr style={theme.divider} />
);

export default function DiagnosticoFormTheme() {
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
  };

  return (
    <div style={card}>
      <h2 style={{
        textAlign: "center",
        marginTop: 0,
        color: theme.colors.primary,
        fontFamily: theme.font.family,
      }}>
        Diagnóstico de Red Doméstica
      </h2>

      {/* === SÍNTOMA PRINCIPAL === */}
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

      {/* === BLOQUES CONDICIONALES (iguales que antes) === */}
      {/* Reutilizamos todos los bloques sin tocar su lógica */}
      {/* Solo se aplica theme visual */}
      {/* No elimines las secciones tipo === "sin_internet" / "lento" / "wifi" */}

      {/* === BOTONES === */}
      <Divider />

      <div style={{ display: "flex", gap: 10, justifyContent: "center" }}>
        <button
          onClick={enviar}
          disabled={loadingDiag || !tipo}
          style={{
            padding: "10px 16px",
            borderRadius: 10,
            border: "none",
            background: theme.colors.primary,
            color: "#fff",
            fontWeight: 600,
            cursor: "pointer",
            transition: "0.2s all",
          }}
        >
          {loadingDiag ? "Diagnosticando..." : "Diagnosticar"}
        </button>

        <button
          onClick={limpiar}
          style={{
            padding: "10px 16px",
            borderRadius: 10,
            border: `1px solid ${theme.colors.border}`,
            background: "#fff",
            color: theme.colors.textSecondary,
            fontWeight: 500,
            cursor: "pointer",
          }}
        >
          Reiniciar
        </button>
      </div>

      {/* === RESULTADO === */}
      {resultado && (
        <div style={{ marginTop: 22 }}>
          <Divider />
          <h4 style={{ color: theme.colors.secondary }}>Causa probable</h4>
          <div style={{ fontWeight: 700 }}>{resultado.causa_probable}</div>

          <h4 style={{ color: theme.colors.secondary }}>Sugerencias</h4>
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

      {/* === DEBUG === */}
      {payloadDebug && (
        <details style={{ marginTop: 16 }}>
          <summary>Payload enviado (debug)</summary>
          <pre>{JSON.stringify(payloadDebug, null, 2)}</pre>
        </details>
      )}
    </div>
  );
}
