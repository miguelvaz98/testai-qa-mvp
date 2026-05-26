"""
Generates tests for a given input via the backend API, saves them, and runs them with Playwright.
Usage: python run_tests.py "your input" [playwright|cypress|jest]
"""
import sys, os, subprocess, requests

API = "http://127.0.0.1:8000/api"
OUT_DIR = os.path.join(os.path.dirname(__file__), "test_runs")

def generate_and_run(input_text: str, framework: str = "playwright"):
    print(f"[1/3] Generando tests ({framework})...")
    r = requests.post(f"{API}/generate", json={"input": input_text, "framework": framework}, timeout=30)
    r.raise_for_status()
    data = r.json()
    test_code = data["tests"]
    tokens = data["tokens_used"]
    print(f"      Tokens usados: {tokens}")

    out_file = os.path.join(OUT_DIR, "generated.spec.ts")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(test_code)
    print(f"[2/3] Tests guardados en {out_file}")

    if framework == "playwright":
        print("[3/3] Ejecutando con Playwright...")
        npx = "npx.cmd" if sys.platform == "win32" else "npx"
        result = subprocess.run(
            [npx, "playwright", "test", "test_runs/generated.spec.ts", "--reporter=list"],
            cwd=os.path.dirname(__file__), capture_output=False
        )
        return result.returncode == 0
    else:
        print(f"[3/3] Tests guardados. Ejecuta manualmente para {framework}.")
        return True

if __name__ == "__main__":
    text = sys.argv[1] if len(sys.argv) > 1 else "Login form with email and password. Submit calls POST /api/login."
    fw = sys.argv[2] if len(sys.argv) > 2 else "playwright"
    ok = generate_and_run(text, fw)
    sys.exit(0 if ok else 1)
