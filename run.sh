#!/usr/bin/env bash
set -euo pipefail

if [ -z "${TG_BOT_TOKEN-}" ]; then
  echo "Please set TG_BOT_TOKEN environment variable."
  exit 1
fi

python3 bot.py
