#!/usr/bin/env sh
# Start the chat agent. Loads .env if present, otherwise uses the current environment.
set -eu
cd "$(dirname "$0")"

if ! command -v uv >/dev/null 2>&1; then
  echo "Error: uv is not installed. See https://docs.astral.sh/uv/" >&2
  exit 1
fi

if [ -f .env ]; then
  exec uv run --env-file .env chat.py "$@"
else
  exec uv run chat.py "$@"
fi
