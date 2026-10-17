import argparse
import random
import sys

from validate import load_deck, validate_deck


def select_cards(cards, difficulty=None, limit=None, shuffle=False, seed=None):
    chosen = [c for c in cards if difficulty is None or c["difficulty"] == difficulty]
    if shuffle:
        random.Random(seed).shuffle(chosen)
    if limit is not None:
        chosen = chosen[:limit]
    return chosen


def run_quiz(cards, input_fn=input, print_fn=print):
    """Ask each card. Returns a list of (card, got_it) pairs. 'q' quits early."""
    results = []
    for n, card in enumerate(cards, 1):
        print_fn(f"\n[{n}/{len(cards)}] ({card['difficulty']}) {card['question']}")
        if input_fn("  Press Enter to reveal (q to quit) ").strip().lower() == "q":
            break
        print_fn(f"  Answer: {card['answer']}")
        reply = ""
        while reply not in ("y", "n", "q"):
            reply = input_fn("  Did you get it? [y/n] ").strip().lower()
        if reply == "q":
            break
        results.append((card, reply == "y"))
    return results


def summarize(results):
    total = len(results)
    correct = sum(ok for _, ok in results)
    percent = round(100 * correct / total) if total else 0
    missed = [card for card, ok in results if not ok]
    return {"total": total, "correct": correct, "percent": percent, "missed": missed}


def print_study_sheet(deck, print_fn=print):
    print_fn(f"# {deck['topic']} - study sheet\n")
    for card in deck["cards"]:
        print_fn(f"{card['id']}. [{card['difficulty']}] {card['question']}")
        print_fn(f"   -> {card['answer']}")


def parse_args(argv):
    p = argparse.ArgumentParser(description="Terminal flashcard quiz.")
    p.add_argument("deck", nargs="?", default="data/flashcards.json")
    p.add_argument("--difficulty", choices=["easy", "medium", "hard"])
    p.add_argument("--limit", type=int)
    p.add_argument("--shuffle", action="store_true")
    p.add_argument("--seed", type=int)
    p.add_argument("--list", action="store_true", help="print all cards, no quiz")
    return p.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    try:
        deck = load_deck(args.deck)
    except (OSError, ValueError) as e:
        print(f"Could not read deck: {e}")
        return 1
    if errors := validate_deck(deck):
        print("Deck is invalid:")
        for err in errors:
            print(f"  - {err}")
        return 1

    if args.list:
        print_study_sheet(deck)
        return 0

    cards = select_cards(deck["cards"], args.difficulty, args.limit, args.shuffle, args.seed)
    if not cards:
        print("No cards match those options.")
        return 0

    print(f"Quiz: {deck['topic']} ({len(cards)} cards)")
    try:
        results = run_quiz(cards)
    except (EOFError, KeyboardInterrupt):
        print("\nQuiz stopped.")
        return 0

    s = summarize(results)
    print(f"\nScore: {s['correct']}/{s['total']} ({s['percent']}%)")
    if s["missed"]:
        print("Review these:")
        for card in s["missed"]:
            print(f"  - {card['question']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
