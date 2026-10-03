# /// script
# requires-python = ">=3.14"
# dependencies = ["anthropic"]
# ///
"""Minimalist chat agent: a terminal chat with Claude. See SPEC.md."""

import os
import sys

import anthropic

DEFAULT_MODEL = "claude-sonnet-5-5"
MAX_TOKENS = 8192

HELP = """\
Type a message and press Enter to chat with Claude ({model}).
The conversation is remembered until you exit; nothing is saved.

Commands:
  /help   Show this help
  /quit   Exit (Ctrl+D or Ctrl+C also exit)
"""


def error_message(e: anthropic.APIError) -> str:
    """Prefer the API's own error message over the SDK's long default."""
    body = getattr(e, "body", None)
    if isinstance(body, dict) and isinstance(body.get("error"), dict):
        return body["error"].get("message") or str(e)
    return str(e)


def chat(client: anthropic.Anthropic, model: str) -> int:
    history = []
    while True:
        try:
            text = input("You: ").strip()
        except EOFError:  # R9
            print()
            return 0

        if not text:  # R4
            continue
        if text == "/quit":  # R8
            return 0
        if text == "/help":  # R15
            print(HELP.format(model=model))
            continue

        history.append({"role": "user", "content": text})  # R5
        try:
            response = client.messages.create(model=model, max_tokens=MAX_TOKENS, messages=history)
        except anthropic.AuthenticationError:  # R11
            print("Error: authentication failed — check ANTHROPIC_API_KEY.", file=sys.stderr)
            return 1
        except anthropic.APIError as e:  # R12, R13
            history.pop()
            hint = ""
            if isinstance(e, anthropic.BadRequestError):
                hint = " (conversation may be too long — restart to begin a new one)"
            print(f"Error: {error_message(e)}{hint}", file=sys.stderr)
            continue

        reply = "".join(block.text for block in response.content if block.type == "text")
        history.append({"role": "assistant", "content": reply})  # R6
        print(f"Claude: {reply}")
        if response.stop_reason == "max_tokens":  # R7
            print("[reply truncated]")
        print()


def main() -> int:
    if not os.environ.get("ANTHROPIC_API_KEY"):  # R1
        print("Error: ANTHROPIC_API_KEY is not set.", file=sys.stderr)
        return 1

    model = os.environ.get("CHAT_MODEL") or DEFAULT_MODEL
    print("Minimalist Chat Agent. Ask Claude anything.")  # R2
    print(f"Model: {model} · Type /help for more information, /quit to exit.")
    print()

    try:
        return chat(anthropic.Anthropic(), model)
    except KeyboardInterrupt:  # R10
        print()
        return 0


if __name__ == "__main__":
    sys.exit(main())
