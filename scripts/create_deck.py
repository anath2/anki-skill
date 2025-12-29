#!/usr/bin/env python3
"""Create Anki .apkg deck from JSON input."""

import json
import sys
import hashlib
import genanki


def stable_id(name: str) -> int:
    """Generate stable ID from name to avoid collisions."""
    return int(hashlib.sha256(name.encode()).hexdigest()[:8], 16)


# Models
BASIC_MODEL = genanki.Model(
    stable_id("basic_model_v1"),
    "Basic",
    fields=[{"name": "Front"}, {"name": "Back"}],
    templates=[{
        "name": "Card 1",
        "qfmt": "{{Front}}",
        "afmt": '{{FrontSide}}<hr id="answer">{{Back}}',
    }],
)

REVERSED_MODEL = genanki.Model(
    stable_id("reversed_model_v1"),
    "Basic (and reversed)",
    fields=[{"name": "Front"}, {"name": "Back"}],
    templates=[
        {
            "name": "Card 1",
            "qfmt": "{{Front}}",
            "afmt": '{{FrontSide}}<hr id="answer">{{Back}}',
        },
        {
            "name": "Card 2",
            "qfmt": "{{Back}}",
            "afmt": '{{FrontSide}}<hr id="answer">{{Front}}',
        },
    ],
)

CLOZE_MODEL = genanki.Model(
    stable_id("cloze_model_v1"),
    "Cloze",
    model_type=genanki.Model.CLOZE,
    fields=[{"name": "Text"}, {"name": "Extra"}],
    templates=[{
        "name": "Cloze",
        "qfmt": "{{cloze:Text}}",
        "afmt": "{{cloze:Text}}<br>{{Extra}}",
    }],
)


def create_deck(data: dict, output_path: str) -> None:
    deck_name = data.get("deck_name", "Untitled Deck")
    deck = genanki.Deck(stable_id(deck_name), deck_name)

    for card in data.get("cards", []):
        card_type = card.get("type", "basic")
        front = card.get("front", "")
        back = card.get("back", "")

        if card_type == "cloze":
            note = genanki.Note(model=CLOZE_MODEL, fields=[front, back])
        elif card_type == "reversed":
            note = genanki.Note(model=REVERSED_MODEL, fields=[front, back])
        else:
            note = genanki.Note(model=BASIC_MODEL, fields=[front, back])

        deck.add_note(note)

    genanki.Package(deck).write_to_file(output_path)


def main():
    if len(sys.argv) != 3:
        print("Usage: create-deck input.json output.apkg", file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1]) as f:
        data = json.load(f)

    create_deck(data, sys.argv[2])
    print(f"Created {sys.argv[2]} with {len(data.get('cards', []))} cards")


if __name__ == "__main__":
    main()
