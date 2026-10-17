#!/usr/bin/env bash
# One command to check the handoff and start the quiz.
set -euo pipefail
cd "$(dirname "$0")"
DECK="${1:-data/flashcards.json}"

echo "== 1. Gate: validating Stage 1 output =="
python3 validate.py "$DECK"

echo "== 2. Checking Stage 2 code: running tests =="
python3 -m unittest discover -s tests

echo "== 3. Launching quiz =="
python3 quiz.py "$DECK" --shuffle
