import httpx
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from shared.config import SUPABASE_URL, SUPABASE_ANON_KEY

MAX_TRIALS = 3
HEADERS = {
    "apikey": SUPABASE_ANON_KEY,
    "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation",
}
TABLE = f"{SUPABASE_URL}/rest/v1/trials"

def get_count(session_id: str) -> int:
    r = httpx.get(TABLE, headers=HEADERS, params={"session_id": f"eq.{session_id}"}, timeout=5)
    rows = r.json()
    return rows[0]["count"] if rows else 0

def increment(session_id: str) -> int:
    current = get_count(session_id)
    if current == 0:
        httpx.post(TABLE, headers=HEADERS, json={"session_id": session_id, "count": 1}, timeout=5)
        return 1
    else:
        new_count = current + 1
        httpx.patch(TABLE, headers=HEADERS, params={"session_id": f"eq.{session_id}"}, json={"count": new_count}, timeout=5)
        return new_count

def is_allowed(session_id: str) -> bool:
    return get_count(session_id) < MAX_TRIALS
