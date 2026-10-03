# Minimalist Chat Agent

Chat with Claude, an AI assistant made by Anthropic, from your computer's
terminal. It's the simplest possible chat program written in Python: you type a
message, Claude replies, and you keep talking.

```
Minimalist Chat Agent. Ask Claude anything.
Model: claude-sonnet-5-5 · Type /help for more information, /quit to exit.

You: What's a good name for a grey cat?
Claude: A few ideas: Ash, Smokey, Pebble, Earl Grey, or Misty...
```

---

## Contents

1. [What is this?](#1-what-is-this)
2. [What it can and cannot do](#2-what-it-can-and-cannot-do)
3. [What you need before you start](#3-what-you-need-before-you-start)
4. [Setup, step by step](#4-setup-step-by-step)
5. [How to use it](#5-how-to-use-it)
6. [Tips for good conversations](#6-tips-for-good-conversations)
7. [Costs, privacy and safety](#7-costs-privacy-and-safety)
8. [Troubleshooting](#8-troubleshooting)
9. [Glossary](#9-glossary)
10. [For developers](#10-for-developers)

---

## 1. What is this?

### A few words about AI and Claude

**Claude** is an *AI model*: a computer program trained on large amounts of
text so that it can understand questions written in everyday language and
answer them in everyday language. You don't need special commands; you just
write to it as you would write to a knowledgeable person.

**Anthropic** is the company that makes Claude. You may know Claude from the
website [claude.ai](https://claude.ai). This project talks to the same AI, but
through Anthropic's **API**: a way for programs (instead of people in a web
browser) to send messages to Claude and get replies back.

A **chat** is a back-and-forth conversation. You send a message, Claude
replies, and you can answer the reply. Claude sees the whole conversation so
far, so you can say things like "make it shorter" or "explain the second point"
and it knows what you mean.

### What this program is for

This project is deliberately small. It is useful if you want to:

- **Try Claude from your own computer** with your own API key.
- **Learn how a chat program works.** The whole program is one file,
  [`chat.py`](chat.py), of about 90 lines, small enough to read in a few minutes.
- **Have a starting point** for building something of your own.

---

## 2. What it can and cannot do

### ✅ It can

- Hold a conversation with Claude in your terminal.
- Remember everything said **during the current session**, so follow-up
  questions work.
- Answer questions, explain things, write and edit text, translate, brainstorm,
  summarise text you paste in, help with code, and much more: anything Claude can
  do with words alone.
- Let you choose which Claude model to use (see
  [Choosing a different model](#choosing-a-different-model)).

### ❌ It cannot

- **Remember past sessions.** When you close the program, the conversation is
  gone. Nothing is saved to disk.
- **Browse the internet or look up current information.** Claude only knows
  what it learned during training, up to a certain date.
- **Open, read or change files on your computer**, or run programs. It only
  sees the text you type into the chat.
- **Show images or read attachments.** It's text only.
- **Handle endless conversations.** Very long conversations eventually exceed
  how much text Claude can consider at once (its *context window*). You'll see
  an error; restart the program to begin a fresh conversation.

> **Claude can be wrong.** It sometimes states incorrect things confidently.
> Double-check anything important, especially facts, figures, medical, legal
> or financial information.

---

## 3. What you need before you start

| You need | Why | Cost |
|---|---|---|
| A computer running **macOS, Linux or Windows** | To run the program | — |
| An **internet connection** | Claude runs on Anthropic's servers, not on your computer | — |
| A **terminal** (also called command line) | This is where the chat happens | Built in |
| **uv** | A tool that installs Python and everything this program needs, automatically | Free |
| An **Anthropic API key** | Proves to Anthropic that the requests come from your account | Free to create; you pay for use (see [Costs](#costs)) |

**You do not need to install Python yourself.** uv downloads the right version
(Python 3.14 or newer) the first time you run the program.

> **A claude.ai subscription is not the same as API access.** A Claude Pro or
> Max subscription does not include API credits. You need a separate account on
> the [Claude Console](https://console.anthropic.com/) with its own billing.

---

## 4. Setup, step by step

You only need to do this once.

### Step 1: Open a terminal

- **macOS:** press `Cmd + Space`, type **Terminal**, and press Enter.
- **Windows:** press the Windows key, type **PowerShell**, and press Enter.
- **Linux:** press `Ctrl + Alt + T` or find **Terminal** in your applications.

In the instructions below, a grey box like this one holds a command. Type it (or
copy and paste it) into the terminal and press **Enter**:

```sh
echo hello
```

### Step 2: Install uv

**macOS or Linux:**

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Then **close the terminal and open a new one**, so it notices the new tool.
Check that it works:

```sh
uv --version
```

You should see something like `uv 0.12.22`. If you see "command not found",
see [Troubleshooting](#8-troubleshooting).

### Step 3: Download this project

**Option A, no Git needed:** open the
[project page on GitHub](https://github.com/belaboros/MinimalistChatAgent_in_python),
click the green **Code** button, choose **Download ZIP**, and unzip it, for
example into your Documents folder.

**Option B, with Git:**

```sh
git clone https://github.com/belaboros/MinimalistChatAgent_in_python.git
```

Now move the terminal into the project folder. `cd` means "change directory":

```sh
cd MinimalistChatAgent_in_python
```

If you downloaded the ZIP, use the folder's actual location, for example
`cd ~/Documents/MinimalistChatAgent_in_python-main`. A handy trick is to type
`cd ` (with a space) and then drag the folder from Finder or File Explorer onto
the terminal window.

### Step 4: Get an Anthropic API key

1. Go to the [Claude Console](https://console.anthropic.com/) and sign up or log in.
2. Open **Billing** and add credits. The API doesn't work without credit.
3. Open **API Keys** and click **Create Key**. Give it a name such as
   `minimalist-chat`.
4. **Copy the key right away.** It starts with `sk-ant-` and is shown only
   once. If you lose it, just create a new one.

> **Treat your API key like a password.** Anyone who has it can use your credit.
> Never post it online, put it in a screenshot, or send it by email or chat.

### Step 5: Put your key in a `.env` file

The program reads your key from a small settings file called `.env` in the
project folder. A template called `.env.example` is included.

1. Copy the template:

   **macOS / Linux:**
   ```sh
   cp .env.example .env
   ```
   **Windows (PowerShell):**
   ```powershell
   Copy-Item .env.example .env
   ```

2. Open `.env` in any text editor (TextEdit, Notepad, VS Code...) and paste
   your key after the `=` sign, with no spaces or quotes:

   ```
   ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxx
   ```

3. Save the file.

Files whose names start with a dot are hidden by default. In Finder, press
`Cmd + Shift + .` to show them. The `.env` file is listed in `.gitignore`, so
Git will never upload it to GitHub by accident.

### Step 6: Start the chat

**macOS / Linux:**

```sh
./run.sh
```

**Windows (PowerShell):**

```powershell
uv run --env-file .env chat.py
```

The first start takes a little longer while uv downloads what it needs. Then
you'll see the welcome message and the `You:` prompt. You're ready! 🎉

---

## 5. How to use it

### Chatting

Type your message after `You:` and press **Enter**. Wait a moment; Claude's
answer appears after `Claude:`. Then type your next message.

```
You: Explain what a black hole is, in two sentences.
Claude: A black hole is a region of space where gravity is so strong that
nothing, not even light, can escape it. It forms when a massive star collapses
in on itself at the end of its life.

You: Now explain it to a five-year-old.
Claude: Imagine a super-strong space vacuum cleaner...
```

Notice the second question: "it" refers to the black hole. Claude understood
because it sees the whole conversation.

Some things to know:

- **One line per message.** Pressing Enter sends the message. To send a long
  text, paste it as one line, or write it in a text editor first and paste it.
- **The whole reply appears at once**, not word by word. Longer answers take a
  few seconds longer.
- **Empty messages are ignored.** Pressing Enter on an empty line just shows a
  new prompt.

### Commands

| Type this | What happens |
|---|---|
| `/help` | Shows a short help text. This is not sent to Claude. |
| `/quit` | Ends the program. |
| `Ctrl + D` | Also ends the program (macOS/Linux; on Windows use `Ctrl + C`). |
| `Ctrl + C` | Ends the program immediately, even while waiting for a reply. |

Commands must be typed exactly as shown, in lowercase, and on their own.
Anything else, including a mistyped command such as `/hepl`, is sent to Claude
as a normal message.

### Starting a new conversation

Type `/quit`, then start the program again. Starting over is useful when you
change topics, because a fresh conversation keeps old context from getting in
the way.

### Choosing a different model

Anthropic offers several Claude models. Larger ones are more capable; smaller
ones are faster and cheaper. This program uses `claude-sonnet-5-5` by default.
To change it, add a line to your `.env` file:

```
CHAT_MODEL=claude-haiku-4-5-20251001
```

The welcome message shows which model is in use. The list of current model
names is in [Anthropic's documentation](https://docs.claude.com/en/docs/about-claude/models/overview).

### If something goes wrong during a chat

If there's a network hiccup or Anthropic's service is busy, you'll see a
one-line message starting with `Error:`. **Your conversation is not lost.** Just
type your message again. If your API key is wrong, the program tells you and
stops.

---

## 6. Tips for good conversations

- **Be specific.** "Write a 3-sentence birthday message for my sister who loves
  hiking" works better than "write a birthday message".
- **Give context.** Say who it's for, why you need it, and what you already know.
- **Ask for a format.** "Give me a bulleted list", "answer in one paragraph",
  "make a table".
- **Refine as you go.** "Shorter", "more formal", "give me three alternatives",
  "explain step 2 in more detail".
- **Ask it to explain itself.** "Why do you think that?" or "How sure are you?"
- **Paste text in** to have it summarised, translated, proofread or explained.
- **Verify important answers** with a trustworthy source.

---

## 7. Costs, privacy and safety

### Costs

Using the API costs money. You pay per use, measured in **tokens** (small
pieces of words; roughly, 100 tokens ≈ 75 English words). Both your messages
and Claude's replies count.

Because Claude re-reads the **whole conversation** for every new reply, long
conversations cost more per message than short ones. Starting a fresh
conversation for a new topic saves money.

For a person chatting casually, costs are usually small, but check the current
[pricing](https://www.anthropic.com/pricing#api). In the
[Claude Console](https://console.anthropic.com/) you can see your usage and set
spending limits.

### Privacy

- Your messages are sent over the internet to Anthropic to be processed. See
  Anthropic's [privacy policy](https://www.anthropic.com/legal/privacy) for how
  API data is handled.
- **Don't share secrets** such as passwords, bank details or other people's
  private information.
- This program saves nothing to disk. After you quit, the text stays visible in
  the terminal window until you close or clear it.

### Keeping your key safe

- Keep the key only in `.env`. Never commit it to Git, paste it into a chat, or
  share screenshots of `.env`.
- If you think your key has leaked, **delete it** in the Claude Console under
  **API Keys** and create a new one.

---

## 8. Troubleshooting

| You see | What it means | What to do |
|---|---|---|
| `uv: command not found` (or "not recognized") | uv isn't installed, or the terminal was opened before installing it | Close and reopen the terminal. If it still fails, repeat [Step 2](#step-2-install-uv). |
| `Error: ANTHROPIC_API_KEY is not set.` | The program can't find your key | Check that `.env` exists in the project folder and has your key after `ANTHROPIC_API_KEY=`. On Windows, start with `uv run --env-file .env chat.py`. |
| `Error: authentication failed — check ANTHROPIC_API_KEY.` | The key is wrong, incomplete or deleted | Copy the key again carefully, with no spaces or quotes, or create a new key. |
| An error mentioning **credit balance** or **billing** | Your account has no credit left | Add credits in the Claude Console under **Billing**. |
| An error mentioning **model** | The model name in `CHAT_MODEL` is wrong or no longer offered | Fix the name, or remove the `CHAT_MODEL` line to use the default. |
| `Error: Connection error.` | No internet, or a firewall is blocking the connection | Check your connection and send the message again. |
| An error mentioning **overloaded** or **rate limit** | Anthropic is busy, or you're sending too much too fast | Wait a minute and try again. |
| `... (conversation may be too long — restart to begin a new one)` | The conversation no longer fits in Claude's context window | Type `/quit` and start again. |
| `./run.sh: Permission denied` | The script isn't marked as runnable | Run `chmod +x run.sh` once, or use `uv run --env-file .env chat.py`. |
| `No such file or directory` | The terminal isn't in the project folder | `cd` into the project folder (see [Step 3](#step-3-download-this-project)). |
| `[reply truncated]` under a reply | Claude's answer hit the length limit | Ask "please continue", or ask for a shorter answer. |

> **Another key in your shell?** If you also set `ANTHROPIC_API_KEY` elsewhere
> (for example in `~/.zshrc`), that one wins over `.env`. On macOS/Linux, run
> `unset ANTHROPIC_API_KEY` to use the key from `.env`.

---

## 9. Glossary

| Term | Meaning |
|---|---|
| **AI model** | A program trained on lots of text that can understand and write natural language. |
| **Claude** | Anthropic's family of AI models. |
| **API** | A way for one program to talk to another over the internet. Here, this program talks to Claude. |
| **API key** | A secret code that identifies your account to the API. Like a password. |
| **Terminal** | A text window where you type commands for your computer. |
| **Prompt** | Two meanings: the `You:` marker waiting for your input, and also the message you send to an AI. |
| **Token** | A small piece of text (part of a word) that AI models read and write. Usage is billed in tokens. |
| **Context window** | The maximum amount of text (the conversation so far) Claude can consider at once. |
| **Session** | One run of the program, from start until you quit. |
| **`.env` file** | A small text file holding settings such as your API key, kept out of Git. |
| **uv** | A tool that installs Python and the packages a Python program needs. |

---

## 10. For developers

The project uses **spec-driven development**:

- [`SPEC.md`](SPEC.md) is the source of truth for behavior: requirements (R1…),
  non-goals, and the manual acceptance checklist (A1…). Change the spec first,
  then the code.
- [`CLAUDE.md`](CLAUDE.md) holds the workflow and conventions for working on
  the project with Claude Code.
- [`chat.py`](chat.py) is the entire program. Its dependencies are declared
  inline ([PEP 723](https://peps.python.org/pep-0723/)), so `uv run chat.py`
  needs no `pyproject.toml`.
- [`run.sh`](run.sh) starts it, loading `.env` if present.

Without a `.env` file you can also set variables directly:

```sh
ANTHROPIC_API_KEY=sk-ant-... uv run chat.py
```

## License

[Apache License 2.0](LICENSE)
