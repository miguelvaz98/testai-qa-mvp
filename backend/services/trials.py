import httpx
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from shared.config import SUPABASE_URL, SUPABASE_ANON_KEY

MAX_TRIALS = 5
HEADERS = {
    "apikey": SUPABASE_ANON_KEY,
    "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation",
}
TABLE = f"{SUPABASE_URL}/rest/v1/trials"


def _get_row(session_id: str) -> dict | None:
    r = httpx.get(TABLE, headers=HEADERS, params={"session_id": f"eq.{session_id}"}, timeout=5)
    rows = r.json()
    return rows[0] if rows else None


def get_count(session_id: str) -> int:
    row = _get_row(session_id)
    return row["count"] if row else 0


def increment(session_id: str) -> int:
    row = _get_row(session_id)
    if row is None:
        httpx.post(TABLE, headers=HEADERS, json={"session_id": session_id, "count": 1, "paid": False}, timeout=5)
        return 1
    new_count = row["count"] + 1
    httpx.patch(TABLE, headers=HEADERS, params={"session_id": f"eq.{session_id}"}, json={"count": new_count}, timeout=5)
    return new_count


def mark_paid(session_id: str):
    row = _get_row(session_id)
    if row is None:
        httpx.post(TABLE, headers=HEADERS, json={"session_id": session_id, "count": 0, "paid": True}, timeout=5)
    else:
        httpx.patch(TABLE, headers=HEADERS, params={"session_id": f"eq.{session_id}"}, json={"paid": True}, timeout=5)


def is_allowed(session_id: str) -> bool:
    row = _get_row(session_id)
    if row is None:
        return True
    if row.get("paid", False):
        return True
    return row["count"] < MAX_TRIALS
