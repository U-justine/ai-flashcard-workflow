import json
import sys
from pathlib import Path

ALLOWED_DIFFICULTY = {"easy", "medium", "hard"}


def load_deck(path):
    """Read the deck. Tolerates ```json fences that chat tools often add."""
    text = Path(path).read_text(encoding="utf-8").strip()
    if text.startswith("```"):
        lines = text.splitlines()[1:]
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines)
    return json.loads(text)


def validate_deck(data):
    """Return a list of error messages. An empty list means the deck is valid."""
    if not isinstance(data, dict):
        return ["Top level must be a JSON object."]

    errors = []
    topic = data.get("topic")
    if not isinstance(topic, str) or not topic.strip():
        errors.append("'topic' must be a non-empty string.")

    cards = data.get("cards")
    if not isinstance(cards, list) or not cards:
        errors.append("'cards' must be a non-empty list.")
        return errors

    seen_ids = set()
    for i, card in enumerate(cards, 1):
        where = f"card #{i}"
        if not isinstance(card, dict):
            errors.append(f"{where}: must be an object.")
            continue
        card_id = card.get("id")
        if not isinstance(card_id, int) or isinstance(card_id, bool):
            errors.append(f"{where}: 'id' must be a whole number.")
        elif card_id in seen_ids:
            errors.append(f"{where}: duplicate id {card_id}.")
        else:
            seen_ids.add(card_id)
        for field in ("question", "answer"):
            value = card.get(field)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{where}: '{field}' must be a non-empty string.")
        if card.get("difficulty") not in ALLOWED_DIFFICULTY:
            errors.append(f"{where}: 'difficulty' must be one of {sorted(ALLOWED_DIFFICULTY)}.")
    return errors


def main(argv):
    path = argv[1] if len(argv) > 1 else "data/flashcards.json"
    try:
        data = load_deck(path)
    except FileNotFoundError:
        print(f"FAIL: file not found: {path}")
        return 2
    except json.JSONDecodeError as e:
        print(f"FAIL: invalid JSON at line {e.lineno}, column {e.colno}: {e.msg}")
        print("Tip: ask the chat AI to 'return only valid JSON' and try again.")
        return 1

    if errors := validate_deck(data):
        print(f"FAIL: {path} has {len(errors)} problem(s):")
        for err in errors:
            print(f"  - {err}")
        print("Tip: paste these errors back into the chat AI and ask it to fix the JSON.")
        return 1

    print(f"PASS: {path} - '{data['topic']}' with {len(data['cards'])} cards.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
