import requests
import json, os

HEADERS = {"User-Agent": "testai-qa-bot/1.0"}
SEEN_FILE = os.path.join(os.path.dirname(__file__), "seen_posts.json")

SUBREDDITS = ["QualityAssurance", "softwaretesting", "webdev", "reactjs", "node"]
KEYWORDS = [
    "playwright test",
    "cypress e2e",
    "how to write unit tests",
    "test automation help",
    "e2e testing setup",
    "jest testing",
    "frontend testing",
    "no tests codebase",
]

def load_seen() -> set:
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE) as f:
            return set(json.load(f))
    return set()

def save_seen(seen: set):
    with open(SEEN_FILE, "w") as f:
        json.dump(list(seen), f)

def search_reddit(query: str, subreddit: str = None, limit: int = 10) -> list[dict]:
    if subreddit:
        url = f"https://www.reddit.com/r/{subreddit}/search.json"
    else:
        url = "https://www.reddit.com/search.json"
    params = {"q": query, "sort": "new", "limit": limit, "t": "week"}
    try:
        r = requests.get(url, headers=HEADERS, params=params, timeout=10)
        if not r.ok:
            return []
        posts = r.json().get("data", {}).get("children", [])
        return [p["data"] for p in posts]
    except Exception:
        return []

def find_opportunities() -> list[dict]:
    seen = load_seen()
    found = []

    for sub in SUBREDDITS:
        for kw in KEYWORDS[:4]:  # limit to 4 keywords per subreddit to avoid rate limits
            posts = search_reddit(kw, subreddit=sub, limit=5)
            for post in posts:
                pid = post.get("id", "")
                if pid in seen:
                    continue
                score = post.get("score", 0)
                num_comments = post.get("num_comments", 0)
                # Only surface posts with some engagement or very recent
                if score >= 1 or num_comments >= 1:
                    found.append({
                        "id": pid,
                        "title": post.get("title", ""),
                        "selftext": post.get("selftext", "")[:500],
                        "url": f"https://reddit.com{post.get('permalink', '')}",
                        "subreddit": post.get("subreddit", ""),
                        "score": score,
                        "comments": num_comments,
                        "keyword": kw,
                    })
                    seen.add(pid)

    save_seen(seen)
    return found
