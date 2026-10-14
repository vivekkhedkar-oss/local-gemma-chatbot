#!/usr/bin/env python3
"""Local terminal chatbot backed by Ollama, using AGENTS.md as the system prompt."""

import argparse
import json
import sys
import urllib.request
from pathlib import Path

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "gemma4:e2b"
AGENTS_PATH = Path(__file__).parent / "AGENTS.md"


def load_system_prompt(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()


def stream_chat(messages):
    payload = json.dumps({"model": MODEL, "messages": messages, "stream": True}).encode("utf-8")
    req = urllib.request.Request(
        OLLAMA_URL, data=payload, headers={"Content-Type": "application/json"}
    )
    full_reply = []
    with urllib.request.urlopen(req) as resp:
        for line in resp:
            line = line.strip()
            if not line:
                continue
            chunk = json.loads(line)
            content = chunk.get("message", {}).get("content", "")
            if content:
                print(content, end="", flush=True)
                full_reply.append(content)
            if chunk.get("done"):
                break
    print()
    return "".join(full_reply)


def main():
    parser = argparse.ArgumentParser(description="Chat with a local Ollama model.")
    parser.add_argument(
        "--persona",
        type=Path,
        default=AGENTS_PATH,
        help="Markdown file used as the system prompt (default: AGENTS.md)",
    )
    args = parser.parse_args()

    if not args.persona.exists():
        sys.exit(f"Missing {args.persona}")

    history = []
    print(f"Chatting with {MODEL} as {args.persona.name}. Type /exit to quit.\n")

    while True:
        try:
            user_input = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not user_input:
            continue
        if user_input == "/exit":
            break

        history.append({"role": "user", "content": user_input})
        messages = [{"role": "system", "content": load_system_prompt(args.persona)}] + history

        print("bot> ", end="", flush=True)
        try:
            reply = stream_chat(messages)
        except urllib.error.URLError:
            print("\n[error] Could not reach Ollama. Is it running? (`ollama serve`)")
            history.pop()
            continue

        history.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    main()
