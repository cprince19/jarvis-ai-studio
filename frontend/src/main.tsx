import React, { useState } from "react";
import ReactDOM from "react-dom/client";
import { Dashboard } from "./components/Dashboard";
import { Login } from "./components/Login";
import { getToken } from "./auth";
import "./styles.css";

function App() {
  const [authenticated, setAuthenticated] = useState(Boolean(getToken()));
  return authenticated ? <Dashboard onLogout={() => setAuthenticated(false)} /> : <main className="auth-shell"><Login onAuthenticated={() => setAuthenticated(true)} /></main>;
}

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode><App /></React.StrictMode>,
);
