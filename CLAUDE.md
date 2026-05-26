# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project: TestAI-QA MVP

Micro-SaaS that receives frontend code or a user story and returns a ready-to-run test suite (Playwright/Cypress/Jest). Built in sessions of ~1h/day — keep changes surgical and modular.

## Commands

```powershell
# Activate venv (always required first)
.\venv\Scripts\Activate.ps1

# Run backend locally
.\venv\Scripts\uvicorn.exe backend.main:app --host 127.0.0.1 --port 8000

# Run frontend locally (serves frontend/ on port 3000)
cd frontend; python -m http.server 3000

# Run both via orchestrator (controlled from Telegram)
.\venv\Scripts\python orchestrator.py

# Validate setup (env vars, imports, HTTP)
.\venv\Scripts\python check_setup.py

# Generate tests via API + run them with Playwright
.\venv\Scripts\python run_tests.py "your input here" playwright

# Run a specific generated test file
npx.cmd playwright test test_runs/generated.spec.ts --reporter=list

# Install a new dependency
.\venv\Scripts\pip install <package>
# Then add to requirements.txt manually
```

## Architecture

```
testai-qa-mvp/
├── backend/              FastAPI app (deployed on Render)
│   ├── main.py           App factory + CORS + router mount
│   ├── models.py         Pydantic: GenerateRequest, GenerateResponse
│   ├── routers/
│   │   └── generate.py   POST /api/generate — entry point
│   └── services/
│       ├── llm.py        Anthropic claude-haiku-4-5 call + markdown fence stripping
│       └── trials.py     Supabase REST trial counter (httpx, no SDK)
├── frontend/             Static HTML/JS (deployed on Vercel)
│   ├── index.html        Tailwind UI: textarea + framework select + button
│   └── app.js            Fetch logic, session_id (localStorage), trial gate
├── shared/
│   ├── config.py         Single source for all env vars (dotenv)
│   ├── telegram.py       send() / wait_for_reply() — blocking Telegram polling
│   └── ask_telegram.py   CLI wrapper: sends question to Telegram, prints reply to stdout
├── orchestrator.py       Interactive process manager controlled via Telegram
├── run_tests.py          Generates tests via API then runs them with Playwright
└── marketing_agent/      (pending) Reddit/X scraper + Telegram alerts
```

## Key Design Decisions

**No Supabase SDK** — uses httpx directly against the REST API (`/rest/v1/trials`). The Python SDK requires C++ build tools to compile on Windows and fails on Python 3.14.

**Trial counting is dual-layer** — `session_id` is `crypto.randomUUID()` stored in localStorage (frontend) and checked/incremented in Supabase (backend). The frontend has its own localStorage counter for UI responsiveness; the backend is the authority. HTTP 402 = trial exhausted.

**Telegram as control plane** — `wait_for_reply()` is a blocking long-poll loop. `ask_telegram.py` lets Claude Code ask questions via Telegram during development sessions and capture the reply as stdout. The orchestrator uses the same mechanism for runtime commands.

**LLM prompt is intentionally minimal** — `SYSTEM_PROMPT` in `llm.py` is ~50 words. Longer prompts increase per-call cost. The fence-stripping post-process handles model non-compliance instead of adding prompt weight.

**Backend is run as a module** — always start with `uvicorn backend.main:app` from the project root (not from inside `backend/`). All `sys.path.insert` calls assume the project root is in the path.

## Deployments

| Service | URL | Notes |
|---------|-----|-------|
| Frontend | https://testai-qa-mvp.vercel.app | Auto-deploys from `main` branch |
| Backend | https://testai-qa-mvp.onrender.com | Start cmd: `bash start.sh`; free tier sleeps after 15min |

Backend env vars required on Render: `ANTHROPIC_API_KEY`, `SUPABASE_URL`, `SUPABASE_ANON_KEY`.

## Supabase Schema

```sql
CREATE TABLE trials (
  session_id TEXT PRIMARY KEY,
  count      INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT now()
);
-- RLS disabled: ALTER TABLE trials DISABLE ROW LEVEL SECURITY;
```

## Environment Variables (.env)

```
ANTHROPIC_API_KEY=...
TELEGRAM_BOT_TOKEN=...
TELEGRAM_CHAT_ID=...
SUPABASE_URL=https://aaidnpzrezclenvcnfvn.supabase.co
SUPABASE_ANON_KEY=...
```
