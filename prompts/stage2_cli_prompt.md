# Stage 2 Prompt — CLI AI or IDE AI

Works in: Claude Code, Gemini CLI, Codex CLI, Aider (CLI),
or Copilot / Cursor / Gemini Code Assist chat (IDE).
Open the project folder first, then paste the prompt.

---
In this folder, `data/flashcards.json` is a flashcard deck made by another AI.
`validate.py` already checks that file. Do not change the JSON format.

Build `quiz.py`, a terminal flashcard quiz, using only the Python standard library:
1. Load and validate the deck using `load_deck` and `validate_deck` from `validate.py`.
   If it is invalid, print the errors and exit with code 1.
2. For each card: show the question, press Enter to reveal the answer,
   then the user types y or n for "did you get it?". Typing q quits.
3. At the end, print the score (correct / total and percent) and list missed questions.
4. Options: --difficulty easy|medium|hard, --limit N, --shuffle, --seed N,
   --list (print all cards as a study sheet, no quiz).
5. Keep the logic in small functions (select_cards, run_quiz, summarize)
   so they can be tested without typing.

Then write unit tests in `tests/` with `unittest`, run
`python3 -m unittest discover -s tests`, and fix anything that fails.
Finish by running `python3 validate.py` and `python3 quiz.py --list`.
---
