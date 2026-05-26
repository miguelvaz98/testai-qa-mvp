import anthropic
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from shared.config import ANTHROPIC_API_KEY

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

SYSTEM_PROMPT = (
    "You are a QA expert. Given frontend code or a user story, "
    "output ONLY a ready-to-run test file in the requested framework. "
    "No explanations. No markdown fences. No backtick code blocks. Raw code only. "
    "Start directly with the import statement or first line of code."
)

FRAMEWORK_HINTS = {
    "playwright": "Use Playwright with TypeScript. Use test() and expect().",
    "cypress":    "Use Cypress with JavaScript. Use describe/it/cy commands.",
    "jest":       "Use Jest + React Testing Library. Use describe/it/expect.",
}

def generate_tests(input_text: str, framework: str) -> tuple[str, int]:
    hint = FRAMEWORK_HINTS.get(framework, "")
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": f"{hint}\n\n{input_text}"}],
    )
    tests = message.content[0].text.strip()
    # Strip markdown fences if model ignores instructions
    if tests.startswith("```"):
        tests = "\n".join(tests.split("\n")[1:])
    if tests.endswith("```"):
        tests = "\n".join(tests.split("\n")[:-1])
    tokens = message.usage.input_tokens + message.usage.output_tokens
    return tests, tokens
