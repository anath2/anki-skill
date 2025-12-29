# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AnkiSkill is a Python tool for creating, parsing, and editing Anki flashcard decks (.apkg files). It's designed as a "skill" for AI assistants to work with Anki decks programmatically using JSON as an intermediate format.

## Development Commands

### Setup
```bash
# Install dependencies using uv
uv sync

# Or install directly with pip
pip install genanki
```

### Running Scripts
```bash
# Create a deck from JSON
uv run create-deck input.json output.apkg
# Or: python3 scripts/create_deck.py input.json output.apkg

# Parse a deck to JSON
uv run parse-deck deck.apkg
# Or: python3 scripts/parse_deck.py deck.apkg
```

### Linting and Type Checking
```bash
# Run type checker
uv run pyright

# Run linter
uv run ruff check
```

## Architecture

### Core Components

**scripts/create_deck.py** - Converts JSON to .apkg format
- Defines three card models: BASIC_MODEL, REVERSED_MODEL, CLOZE_MODEL
- Uses `stable_id()` to generate consistent IDs from names via SHA-256 hashing
- Creates genanki Note and Deck objects, packages them into .apkg

**scripts/parse_deck.py** - Extracts cards from .apkg to JSON
- Unzips .apkg file (which is a ZIP containing SQLite database)
- Reads collection.anki2/anki21 database
- Infers card type from model name ("cloze", "reverse", or "basic")
- Outputs JSON matching create_deck input format

### JSON Card Format

The workflow uses this JSON structure for round-trip editing:

```json
{
  "deck_name": "Deck Name",
  "cards": [
    {"front": "Question", "back": "Answer"},
    {"front": "Front", "back": "Back", "type": "reversed"},
    {"front": "{{c1::Cloze}} text", "back": "Extra info", "type": "cloze"}
  ]
}
```

Card types:
- `basic` (default): Single front→back card
- `reversed`: Creates two cards (front→back and back→front)
- `cloze`: Cloze deletion cards using {{c1::text}}, {{c2::text}} syntax

### ID Generation

The `stable_id()` function in scripts/create_deck.py:11 generates deterministic IDs from names to prevent conflicts and ensure reproducible deck creation. This is crucial because genanki requires unique numeric IDs for models and decks.

## Important Notes

- .apkg files are ZIP archives containing an SQLite database (collection.anki2 or collection.anki21)
- The scripts use genanki for creation but raw SQLite for parsing (since genanki doesn't provide parsing)
- Card type inference during parsing is done by matching model names (case-insensitive check for "cloze" or "reverse")
- When editing decks, always parse first, modify the JSON, then recreate the .apkg
