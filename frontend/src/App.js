import DiagnosticoForm from "./components/DiagnosticoForm";
import SpeedTestCard from "./components/SpeedTestCard";

function App() {
  return (
    <div style={{ textAlign: "center", fontFamily: "Arial", padding: 20 }}>
      <h1>Sistema Experto - Diagnóstico de Red</h1>
      <DiagnosticoForm />
      <SpeedTestCard />
    </div>
  );
}

export default App;
