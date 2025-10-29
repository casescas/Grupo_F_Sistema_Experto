import DiagnosticoForm from "./components/DiagnosticoForm";
import SpeedTestCard from "./components/SpeedTestCard";
import theme from "./theme/uiTheme";

function App() {
  return (
    <div
      style={{
        textAlign: "center",
        fontFamily: theme.font.family,
        padding: 20,
        backgroundColor: theme.colors.background,
        minHeight: "100vh",
      }}
    >
      <h1 style={{ color: theme.colors.primary }}>
        Sistema Experto - Diagnóstico de Red
      </h1>
      <DiagnosticoForm />
      <SpeedTestCard />
    </div>
  );
}

export default App;
