# SPEC: Minimalist Chat Agent

Status: **Approved**
Last updated: 2026-10-03

This file is the source of truth for what the program does. Change the spec
first, then the code.

## 1. Goal

The simplest possible chat agent in Python: a terminal loop where a person
chats with Claude. It does only that.

### Non-goals

- Tools or function calling
- Memory or persistence between runs (history lasts only for one run)
- Streaming output
- System prompt, CLI flags or config files
- Context-window management (trimming, summarizing)
- Multi-line input
- Automated tests

## 2. Technical decisions

| Topic | Decision |
|---|---|
| Language | Python 3.14 (latest stable as of 2026-10). `requires-python = ">=3.14"` |
| Layout | A single file, `chat.py`. No package and no `pyproject.toml` |
| Dependencies | Only `anthropic` (official SDK), declared as [PEP 723](https://peps.python.org/pep-0723/) inline script metadata at the top of `chat.py` |
| Run command | `uv run chat.py` (uv reads the inline metadata and installs dependencies automatically) |
| API | Messages API via `client.messages.create(...)`, non-streaming |
| Default model | `claude-sonnet-5-5` |
| `max_tokens` | `8192` |
| Retries | The SDK's built-in retries (default settings) |

## 3. Configuration

Configuration comes only from environment variables:

| Variable | Required | Default | Purpose |
|---|---|---|---|
| `ANTHROPIC_API_KEY` | yes | — | API key, read by the SDK |
| `CHAT_MODEL` | no | `claude-sonnet-5-5` | Model ID override |

Optionally, these variables can be kept in a `.env` file loaded by uv:
`uv run --env-file .env chat.py`. The program itself does not read `.env`.
`.env` is gitignored; `.env.example` (committed, no values) documents it.

## 4. Behavior

### 4.1 Startup
- R1. If `ANTHROPIC_API_KEY` is unset or empty, print
  `Error: ANTHROPIC_API_KEY is not set.` to stderr and exit with code 1. Make
  no API call.
- R2. Otherwise print this welcome message, followed by a blank line
  (`<model>` is the model in use):

  ```
  Minimalist Chat Agent. Ask Claude anything.
  Model: <model> · Type /help for more information, /quit to exit.
  ```

### 4.2 Chat loop
- R3. Prompt with `You: ` and read one line from stdin.
- R4. Input that is empty or only whitespace is ignored: re-prompt, make no
  API call, and leave history unchanged.
- R5. For any other input, append `{"role": "user", "content": <text>}` to
  history and send the **full history** to the API.
- R6. On success, print `Claude: <reply text>` followed by a blank line, and
  append `{"role": "assistant", "content": <reply text>}` to history. The
  reply text is all text content blocks of the response joined together.
- R7. If the response `stop_reason` is `max_tokens`, print `[reply truncated]`
  on its own line after the reply. The truncated reply stays in history.

### 4.3 Exiting
- R8. `/quit` (after trimming whitespace) exits with code 0.
- R9. EOF (Ctrl+D) exits with code 0. Print a newline first so the shell
  prompt starts on a clean line.
- R10. Ctrl+C, at the prompt or while waiting for a reply, exits with code 0,
  with a newline and no traceback.

### 4.4 Errors
- R11. Authentication error (invalid key): print
  `Error: authentication failed — check ANTHROPIC_API_KEY.` to stderr and exit
  with code 1.
- R12. Any other API or connection error (after the SDK's retries): print
  `Error: <short message from the exception>` to stderr, **remove the failed
  user message from history** (so history keeps alternating user/assistant),
  and return to the prompt.
- R13. Context window exceeded is handled as in R12: the error is shown and
  nothing is trimmed. The error message should suggest restarting, e.g.
  `Error: <message> (conversation may be too long — restart to begin a new one)`
  when the error is a 400 bad request.
- R14. No error path prints a Python traceback.

### 4.5 Commands
- R15. `/help` (after trimming whitespace) prints the help text below to
  stdout, followed by a blank line, and returns to the prompt. It makes no API
  call and leaves history unchanged. `<model>` is the model in use.

  ```
  Type a message and press Enter to chat with Claude (<model>).
  The conversation is remembered until you exit; nothing is saved.

  Commands:
    /help   Show this help
    /quit   Exit (Ctrl+D or Ctrl+C also exit)
  ```
- R16. Commands are case-sensitive and match only the whole trimmed input.
  Anything else, including unknown `/something` input, is sent to Claude as
  a normal message.

## 5. Acceptance checklist (manual)

Run each check before calling the implementation done. Checks marked 🔑 need a
valid API key.

- [ ] A1 (R1): `env -u ANTHROPIC_API_KEY uv run chat.py` prints the key error and `echo $?` gives `1`.
- [ ] A2 (R11): `ANTHROPIC_API_KEY=bogus uv run chat.py`, then send `hi`: prints the auth error and exits with 1.
- [ ] A3 🔑 (R2, R5, R6): start the program, see the welcome message, send `hi`, and get a `Claude:` reply.
- [ ] A4 🔑 (R5): send `My name is Ada.`, then `What is my name?`. The reply mentions Ada, which shows history is kept.
- [ ] A5 🔑 (R4): press Enter on an empty line and on `   `. The prompt reappears and no reply is printed.
- [ ] A6 🔑 (R8): `/quit` exits with code 0.
- [ ] A7 🔑 (R9): Ctrl+D exits cleanly with code 0.
- [ ] A8 🔑 (R10): Ctrl+C at the prompt, and Ctrl+C while waiting for a reply, both exit with no traceback.
- [ ] A9 🔑 (R12): turn off networking, send a message, and see a one-line error. Turn networking back on, send another message, and the conversation continues normally.
- [ ] A10 🔑 (R7): temporarily set `max_tokens` to `5` in code, send `Count to 100`, and see `[reply truncated]`. Restore `8192` afterwards.
- [ ] A11 🔑 (config): `CHAT_MODEL=claude-haiku-4-5-20251001 uv run chat.py`. The welcome message shows that model.
- [ ] A12 (size): `chat.py` stays small and readable, roughly 100 lines or fewer.
- [ ] A13 (R2, R15): `ANTHROPIC_API_KEY=bogus uv run chat.py`. The welcome message mentions `/help`. Typing `/help` and `  /help  ` prints the help text with the model name, with no auth error (no API call is made); then `/quit` exits with 0.
- [ ] A14 🔑 (R15, R16): send `My name is Ada.`, then `/help`, then `What did I just tell you?`. The reply refers to the name, not to `/help`, which shows `/help` stayed out of history.
