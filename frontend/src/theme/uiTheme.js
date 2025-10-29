// src/theme/uiTheme.js

const theme = {
  colors: {
    // 🎨 Paleta base violeta/lila
    primary: "#8B5CF6",        // Violeta principal
    secondary: "#A78BFA",      // Lila claro
    accent: "#C084FC",         // Lila intenso para hover
    background: "#1E1B2E",     // Fondo general oscuro
    surface: "#2D2541",        // Tarjeta principal
    textPrimary: "#F8F9FB",    // Texto principal (claro)
    textSecondary: "#C7C8D0",  // Texto gris claro
    border: "#4C3A7B",         // Bordes suaves violetas
  },

  font: {
    family: "'Inter', sans-serif",
    sizeBase: "16px",
    sizeTitle: "20px",
    weightBold: 600,
  },

  card: {
    borderRadius: "16px",
    boxShadow: "0 8px 20px rgba(0, 0, 0, 0.25)",
    padding: "1.8rem",
  },

  divider: {
    margin: "1.5rem 0",
    border: "none",
    borderTop: "2px solid #3F3A52",
  },
};

export default theme;
