const API = window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1"
  ? "http://127.0.0.1:8000/api"
  : "https://testai-qa-mvp.onrender.com/api";
const MAX_TRIALS = 5;

function getSessionId() {
  let id = localStorage.getItem("tqa_session_id");
  if (!id) {
    id = crypto.randomUUID();
    localStorage.setItem("tqa_session_id", id);
  }
  return id;
}

function getTrials() {
  return parseInt(localStorage.getItem("tqa_trials") || "0");
}
function incTrials() {
  localStorage.setItem("tqa_trials", getTrials() + 1);
}
function updateTrialsUI() {
  if (isPaid()) {
    document.getElementById("upgradeBox").classList.add("hidden");
    document.getElementById("trialsMsg").textContent = "Plan activo — generaciones ilimitadas.";
    return;
  }
  const left = MAX_TRIALS - getTrials();
  const el = document.getElementById("trialsMsg");
  if (left > 0) {
    el.textContent = `Pruebas gratuitas restantes: ${left} / ${MAX_TRIALS}`;
    document.getElementById("upgradeBox").classList.add("hidden");
  } else {
    el.textContent = "";
    document.getElementById("upgradeBox").classList.remove("hidden");
  }
}

// Called on page load if user returns from Stripe with ?upgraded=true
function checkUpgradeReturn() {
  const params = new URLSearchParams(window.location.search);
  if (params.get("upgraded") === "true") {
    localStorage.setItem("tqa_paid", "true");
    document.getElementById("upgradeBox").classList.add("hidden");
    document.getElementById("trialsMsg").textContent = "Plan activo — generaciones ilimitadas.";
    window.history.replaceState({}, "", "/");
  }
}

function isPaid() {
  return localStorage.getItem("tqa_paid") === "true";
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
  if (!isPaid() && getTrials() >= MAX_TRIALS) {
    document.getElementById("upgradeBox").classList.remove("hidden");
    return;
  }

  btn.disabled = true;
  btn.textContent = "Generando...";

  try {
    const res = await fetch(`${API}/generate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ input, framework, session_id: getSessionId() }),
    });
    if (!res.ok) {
      const err = await res.json();
      if (res.status === 402) {
        localStorage.setItem("tqa_trials", MAX_TRIALS);
        updateTrialsUI();
        return;
      }
      throw new Error(err.detail || "Error del servidor.");
    }
    const data = await res.json();
    document.getElementById("output").textContent = data.tests;
    document.getElementById("tokenCount").textContent = `Tokens usados: ${data.tokens_used}`;
    outputBox.classList.remove("hidden");
    if (!isPaid()) {
      incTrials();
      updateTrialsUI();
    }
  } catch (e) {
    showError(e.message);
  } finally {
    btn.disabled = false;
    btn.textContent = "Generar Tests";
  }
}

async function startCheckout() {
  const btn = document.querySelector("#upgradeBox button");
  btn.disabled = true;
  btn.textContent = "Redirigiendo...";
  try {
    const res = await fetch(`${API}/checkout`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ session_id: getSessionId() }),
    });
    const data = await res.json();
    if (data.url) {
      window.location.href = data.url;
    } else {
      throw new Error(data.detail || "No se pudo iniciar el pago.");
    }
  } catch (e) {
    showError(e.message);
    btn.disabled = false;
    btn.textContent = "Actualizar ahora — $9/mes";
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

checkUpgradeReturn();
updateTrialsUI();
