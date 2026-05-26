"""
Orchestrator — control script for TestAI-QA.
Runs tasks and routes approvals through Telegram.
"""
import subprocess, sys, os, time
sys.path.insert(0, os.path.dirname(__file__))
from shared.telegram import send, wait_for_reply

TASKS = {
    "backend": ["venv\\Scripts\\uvicorn.exe", "backend.main:app", "--host", "127.0.0.1", "--port", "8000"],
}

def start_backend():
    send("🚀 *TestAI-QA*: Arrancando backend en puerto 8000...")
    proc = subprocess.Popen(TASKS["backend"], cwd=os.path.dirname(__file__))
    time.sleep(3)
    import requests
    try:
        r = requests.get("http://127.0.0.1:8000/health", timeout=5)
        if r.ok:
            send("✅ Backend OK — http://127.0.0.1:8000")
            return proc
    except Exception:
        pass
    send("❌ Backend no respondió. Revisa los logs.")
    proc.terminate()
    return None

def ask_approval(question: str, options: list[str] = None) -> str:
    """Pause execution and wait for Telegram approval."""
    return wait_for_reply(f"⚠️ APROBACIÓN REQUERIDA\n\n{question}", options)

MENU = ["backend", "frontend", "ambos", "marketing", "status", "stop"]
MENU_HELP = (
    "backend   — arranca API (puerto 8000)\n"
    "frontend  — arranca UI (puerto 3000)\n"
    "ambos     — arranca los dos\n"
    "marketing — busca oportunidades en Reddit y alerta\n"
    "status    — estado de los procesos\n"
    "stop      — detener todo y salir"
)

processes: dict[str, subprocess.Popen] = {}

def start_frontend():
    send("🎨 Arrancando frontend en puerto 3000...")
    frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")
    proc = subprocess.Popen(
        ["python", "-m", "http.server", "3000"],
        cwd=frontend_dir,
    )
    time.sleep(1)
    send("✅ Frontend OK — http://127.0.0.1:3000")
    return proc

def stop_all():
    for name, proc in list(processes.items()):
        proc.terminate()
        send(f"🛑 {name} detenido.")
    processes.clear()

def handle_command(cmd: str):
    c = cmd.lower().strip()
    if c == "backend":
        if "backend" not in processes:
            proc = start_backend()
            if proc:
                processes["backend"] = proc
        else:
            send("Backend ya está corriendo.")
    elif c == "frontend":
        if "frontend" not in processes:
            processes["frontend"] = start_frontend()
        else:
            send("Frontend ya está corriendo.")
    elif c == "ambos":
        handle_command("backend")
        handle_command("frontend")
    elif c == "status":
        if not processes:
            send("ℹ️ Ningún proceso activo.")
        else:
            send("✅ Activos: " + ", ".join(processes.keys()))
    elif c == "stop":
        stop_all()
        send("👋 Todo detenido. Orquestador saliendo.")
        sys.exit(0)
    elif c == "marketing":
        send("Lanzando Marketing Agent...")
        import subprocess
        subprocess.Popen(
            [os.path.join(os.path.dirname(__file__), "venv", "Scripts", "python.exe"),
             "-m", "marketing_agent.agent"],
            cwd=os.path.dirname(__file__)
        )
    elif c == "ayuda":
        send(MENU_HELP)
    else:
        send(f"❓ Comando desconocido: '{cmd}'\n\n{MENU_HELP}")

def run():
    send(f"🤖 Orquestador TestAI-QA listo.\n\n{MENU_HELP}")
    while True:
        cmd = wait_for_reply("¿Qué hacemos?")
        handle_command(cmd)

if __name__ == "__main__":
    run()
