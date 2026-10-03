# CLAUDE.md

## Workflow: spec-driven

`SPEC.md` is the source of truth. Follow this order:

1. **Spec first.** If a requested change isn't covered by `SPEC.md`, update
   the spec (requirements + acceptance checklist) and get it approved before
   touching code. Requirement IDs (R1…) and check IDs (A1…) are stable; don't
   renumber them.
2. **Plan.** Use plan mode for any implementation work; cite the requirement
   IDs the plan covers.
3. **Implement** only what the spec says. Non-goals in the spec are hard limits,
   so don't add features or config the spec doesn't list.
4. **Verify** against the acceptance checklist in `SPEC.md` section 5. Run the
   checks that don't need an API key yourself; list the 🔑 checks for the user
   to run by hand. Never claim a 🔑 check passed unless it was actually run.
5. **Commit** with a message that references the requirement IDs.

## Commands

- Run: `./run.sh` (uses `.env` if present), or `uv run chat.py` (dependencies come from PEP 723 inline metadata in `chat.py`)
- With a `.env` file: `uv run --env-file .env chat.py`
- Requires `ANTHROPIC_API_KEY` in the environment

## Secrets

- Never read, print or commit `.env`. Document new variables in `.env.example` (no values).

## Conventions

- Single file, standard library + `anthropic` only. Keep it minimal and readable.
- No automated tests by design (see SPEC.md); verification is the manual checklist.
