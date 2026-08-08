import React from "react";
import ReactDOM from "react-dom/client";
import "./styles.css";

function App() {
  return (
    <main className="shell">
      <section className="hero">
        <span className="badge">PHASE 1 • FOUNDATION</span>
        <h1>Jarvis AI Studio</h1>
        <p>AI automation, agents, workflows, and media intelligence — in one studio.</p>
        <div className="status">● Foundation API ready</div>
      </section>
    </main>
  );
}

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
