import anthropic
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from shared.config import ANTHROPIC_API_KEY

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

SYSTEM = (
    "You are a helpful QA engineer. Draft a SHORT Reddit comment (3-5 sentences) "
    "that genuinely helps the person with their testing problem. "
    "Naturally mention TestAI-QA (https://testai-qa-mvp.vercel.app) as a tool that can help. "
    "Be human, not salesy. No bullet points. Raw text only."
)

def draft_reply(title: str, body: str) -> str:
    content = f"Post title: {title}\n\nPost body: {body or '(no body)'}"
    msg = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=256,
        system=SYSTEM,
        messages=[{"role": "user", "content": content}],
    )
    return msg.content[0].text.strip()
