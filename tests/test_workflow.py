import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from validate import load_deck, validate_deck  # noqa: E402
from quiz import run_quiz, select_cards, summarize  # noqa: E402

SAMPLE = ROOT / "data" / "flashcards.json"


def card(i, difficulty="easy"):
    return {"id": i, "question": f"Q{i}", "answer": f"A{i}", "difficulty": difficulty}


class TestHandoffGate(unittest.TestCase):
    def test_sample_deck_is_valid(self):
        self.assertEqual(validate_deck(load_deck(SAMPLE)), [])

    def test_missing_answer_is_caught(self):
        deck = {"topic": "T", "cards": [{"id": 1, "question": "Q", "difficulty": "easy"}]}
        self.assertTrue(any("answer" in e for e in validate_deck(deck)))

    def test_duplicate_id_is_caught(self):
        deck = {"topic": "T", "cards": [card(1), card(1)]}
        self.assertTrue(any("duplicate" in e for e in validate_deck(deck)))

    def test_bad_difficulty_is_caught(self):
        deck = {"topic": "T", "cards": [card(1, "super-hard")]}
        self.assertTrue(any("difficulty" in e for e in validate_deck(deck)))

    def test_empty_cards_is_caught(self):
        self.assertTrue(validate_deck({"topic": "T", "cards": []}))

    def test_code_fences_from_chat_are_tolerated(self):
        deck = {"topic": "T", "cards": [card(1)]}
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            f.write("```json\n" + json.dumps(deck) + "\n```")
        self.assertEqual(load_deck(f.name), deck)


class TestQuiz(unittest.TestCase):
    def setUp(self):
        self.cards = [card(1, "easy"), card(2, "hard"), card(3, "easy")]

    def test_filter_by_difficulty(self):
        self.assertEqual([c["id"] for c in select_cards(self.cards, "easy")], [1, 3])

    def test_limit(self):
        self.assertEqual(len(select_cards(self.cards, limit=2)), 2)

    def test_shuffle_with_seed_is_repeatable(self):
        a = select_cards(self.cards, shuffle=True, seed=7)
        b = select_cards(self.cards, shuffle=True, seed=7)
        self.assertEqual(a, b)

    def test_run_quiz_and_score(self):
        answers = iter(["", "y", "", "n", "", "y"])
        results = run_quiz(self.cards, input_fn=lambda _: next(answers), print_fn=lambda *_: None)
        s = summarize(results)
        self.assertEqual((s["correct"], s["total"], s["percent"]), (2, 3, 67))
        self.assertEqual([c["id"] for c in s["missed"]], [2])

    def test_quit_early(self):
        answers = iter(["", "y", "q"])
        results = run_quiz(self.cards, input_fn=lambda _: next(answers), print_fn=lambda *_: None)
        self.assertEqual(len(results), 1)

    def test_invalid_reply_is_asked_again(self):
        answers = iter(["", "maybe", "y"])
        results = run_quiz(self.cards[:1], input_fn=lambda _: next(answers), print_fn=lambda *_: None)
        self.assertTrue(results[0][1])


if __name__ == "__main__":
    unittest.main()
