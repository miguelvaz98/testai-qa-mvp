"""
Marketing Agent — finds testing complaints on Reddit and alerts via Telegram.
Run once manually or schedule with cron/Task Scheduler.
"""
import sys, os, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from shared.telegram import send
from marketing_agent.scraper import find_opportunities
from marketing_agent.responder import draft_reply

PRODUCT_URL = "https://testai-qa-mvp.vercel.app"

def format_alert(post: dict, reply: str) -> str:
    return (
        f"🎯 OPORTUNIDAD DE MARKETING\n\n"
        f"📌 r/{post['subreddit']} — {post['title'][:80]}\n"
        f"👍 {post['score']} puntos | 💬 {post['comments']} comentarios\n"
        f"🔗 {post['url']}\n\n"
        f"📝 RESPUESTA SUGERIDA:\n{reply}\n\n"
        f"¿Quieres que la publique? Responde SI o NO."
    )

def run(dry_run: bool = False):
    send("🤖 Marketing Agent iniciado. Buscando oportunidades en Reddit...")
    posts = find_opportunities()

    if not posts:
        send("✅ Sin nuevas oportunidades esta vez. Vuelve a ejecutar mañana.")
        return

    send(f"🔍 Encontré {len(posts)} post(s) nuevos. Generando respuestas...")

    for post in posts[:5]:  # max 5 alerts per run to avoid spam
        try:
            reply = draft_reply(post["title"], post["selftext"])
            alert = format_alert(post, reply)
            send(alert)
            time.sleep(2)  # avoid Telegram rate limit
        except Exception as e:
            send(f"⚠️ Error procesando post {post['id']}: {e}")

    send(f"✅ Marketing Agent terminado. {min(len(posts), 5)} alertas enviadas.")

if __name__ == "__main__":
    dry = "--dry" in sys.argv
    run(dry_run=dry)
