"""Quick validation: checks env vars are loaded and APIs are reachable."""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

def check_env():
    from dotenv import load_dotenv
    load_dotenv()
    keys = ["OPENAI_API_KEY", "ANTHROPIC_API_KEY", "TELEGRAM_BOT_TOKEN", "SUPABASE_URL"]
    missing = [k for k in keys if not os.getenv(k)]
    if missing:
        print(f"[WARN] Missing .env keys: {', '.join(missing)}")
    else:
        print("[OK] All env vars loaded.")

def check_fastapi():
    import fastapi, uvicorn, pydantic
    print(f"[OK] FastAPI {fastapi.__version__} | Uvicorn {uvicorn.__version__} | Pydantic {pydantic.__version__}")

def check_playwright():
    import playwright
    print(f"[OK] Playwright installed.")

def check_requests():
    import requests
    r = requests.get("https://httpbin.org/get", timeout=5)
    print(f"[OK] HTTP connectivity — status {r.status_code}")

if __name__ == "__main__":
    print("=== TestAI-QA Setup Check ===")
    check_env()
    check_fastapi()
    check_playwright()
    try:
        check_requests()
    except Exception as e:
        print(f"[FAIL] HTTP check: {e}")
    print("=============================")
