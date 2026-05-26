const API = window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1"
  ? "http://127.0.0.1:8000/api"
  : "https://testai-qa-mvp.onrender.com/api";
const MAX_TRIALS = 3;

function getTrials() {
  return parseInt(localStorage.getItem("tqa_trials") || "0");
}
function incTrials() {
  localStorage.setItem("tqa_trials", getTrials() + 1);
}
function updateTrialsUI() {
  const left = MAX_TRIALS - getTrials();
  const el = document.getElementById("trialsMsg");
  el.textContent = left > 0
    ? `Pruebas gratuitas restantes: ${left} / ${MAX_TRIALS}`
    : "Has usado todas las pruebas gratuitas.";
}

async function generate() {
  const input = document.getElementById("inputCode").value.trim();
  const framework = document.getElementById("framework").value;
  const btn = document.getElementById("generateBtn");
  const outputBox = document.getElementById("outputBox");
  const errorBox = document.getElementById("errorBox");

  errorBox.classList.add("hidden");
  outputBox.classList.add("hidden");

  if (!input) {
    showError("Por favor, escribe algo antes de generar.");
    return;
  }
  if (getTrials() >= MAX_TRIALS) {
    showError("Has agotado las pruebas gratuitas. Próximamente: planes de pago.");
    return;
  }

  btn.disabled = true;
  btn.textContent = "Generando...";

  try {
    const res = await fetch(`${API}/generate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ input, framework }),
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || "Error del servidor.");
    }
    const data = await res.json();
    document.getElementById("output").textContent = data.tests;
    document.getElementById("tokenCount").textContent = `Tokens usados: ${data.tokens_used}`;
    outputBox.classList.remove("hidden");
    incTrials();
    updateTrialsUI();
  } catch (e) {
    showError(e.message);
  } finally {
    btn.disabled = false;
    btn.textContent = "Generar Tests";
  }
}

function showError(msg) {
  const el = document.getElementById("errorBox");
  el.textContent = msg;
  el.classList.remove("hidden");
}

function copyOutput() {
  const text = document.getElementById("output").textContent;
  navigator.clipboard.writeText(text).then(() => alert("¡Copiado!"));
}

updateTrialsUI();
