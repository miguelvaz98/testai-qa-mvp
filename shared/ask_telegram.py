"""
Run this script to send a question to Telegram and wait for the reply.
Usage: python shared/ask_telegram.py "Your question here" [opt1] [opt2] ...
Output: prints the user's reply to stdout (captured by Claude Code)
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from shared.telegram import wait_for_reply

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print("Usage: ask_telegram.py <question> [option1] [option2] ...")
        sys.exit(1)
    question = args[0]
    options = args[1:] if len(args) > 1 else None
    reply = wait_for_reply(question, options)
    print(reply)
