import requests
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from shared.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

BASE = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

def send(text: str) -> bool:
    r = requests.post(f"{BASE}/sendMessage", json={"chat_id": TELEGRAM_CHAT_ID, "text": text}, timeout=10)
    return r.ok

def get_updates(offset: int = 0) -> list[dict]:
    r = requests.get(f"{BASE}/getUpdates", params={"offset": offset, "timeout": 30}, timeout=35)
    if r.ok:
        return r.json().get("result", [])
    return []

def wait_for_reply(prompt: str, options: list[str] = None) -> str:
    """Send prompt to Telegram, block until user replies. Returns reply text."""
    msg = prompt
    if options:
        msg += "\n\nOpciones: " + " | ".join(f"[{o}]" for o in options)
    send(msg)

    last_update_id = 0
    updates = get_updates()
    if updates:
        last_update_id = updates[-1]["update_id"] + 1

    print(f"[Telegram] Esperando respuesta... (prompt enviado)")
    while True:
        updates = get_updates(offset=last_update_id)
        for upd in updates:
            last_update_id = upd["update_id"] + 1
            msg = upd.get("message", {})
            if str(msg.get("chat", {}).get("id")) == str(TELEGRAM_CHAT_ID):
                return msg.get("text", "").strip()
