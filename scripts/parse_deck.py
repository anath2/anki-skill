#!/usr/bin/env python3
"""Parse Anki .apkg deck to JSON."""

import json
import sqlite3
import sys
import tempfile
import zipfile
from pathlib import Path


def parse_deck(apkg_path: str) -> dict:
    with tempfile.TemporaryDirectory() as tmpdir:
        with zipfile.ZipFile(apkg_path, "r") as z:
            z.extractall(tmpdir)

        db_path = Path(tmpdir) / "collection.anki2"
        if not db_path.exists():
            db_path = Path(tmpdir) / "collection.anki21"

        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row

        # Get deck name
        decks_json = conn.execute("SELECT decks FROM col").fetchone()[0]
        decks = json.loads(decks_json)
        deck_name = next(
            (d["name"] for d in decks.values() if d["name"] != "Default"),
            "Untitled Deck"
        )

        # Get models to determine card types
        models_json = conn.execute("SELECT models FROM col").fetchone()[0]
        models = json.loads(models_json)
        model_types = {}
        for mid, model in models.items():
            name = model.get("name", "").lower()
            if "cloze" in name:
                model_types[int(mid)] = "cloze"
            elif "reverse" in name:
                model_types[int(mid)] = "reversed"
            else:
                model_types[int(mid)] = "basic"

        # Extract notes
        cards = []
        for row in conn.execute("SELECT mid, flds FROM notes"):
            mid = row["mid"]
            fields = row["flds"].split("\x1f")
            card_type = model_types.get(mid, "basic")

            card = {"front": fields[0] if fields else "", "back": fields[1] if len(fields) > 1 else ""}
            if card_type != "basic":
                card["type"] = card_type
            cards.append(card)

        conn.close()

    return {"deck_name": deck_name, "cards": cards}


def main():
    if len(sys.argv) != 2:
        print("Usage: parse-deck deck.apkg", file=sys.stderr)
        sys.exit(1)

    result = parse_deck(sys.argv[1])
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
