---
name: anki
description: Create, read, and edit Anki flashcard decks (.apkg files). Use when the user wants to generate flashcards from content, parse existing decks, add/remove cards, or export study material to Anki format. Triggers on requests involving Anki, flashcards, spaced repetition decks, or .apkg files.
---

# Anki Deck Skill

## Workflow

**Creating a deck?** → Generate cards as JSON → Run `create-deck`
**Reading a deck?** → Run `parse-deck` → Returns JSON of cards
**Editing a deck?** → Parse first, modify JSON, recreate deck

## Creating Decks

1. Generate card data as JSON:
```json
{
  "deck_name": "My Deck",
  "cards": [
    {"front": "Question", "back": "Answer"},
    {"front": "{{c1::Cloze}} deletion", "back": "", "type": "cloze"}
  ]
}
```

2. Run:
```bash
create-deck input.json output.apkg
```

## Card Types

| Type | Fields | Notes |
|------|--------|-------|
| Basic | front, back | Default type |
| Basic+Reversed | front, back, type:"reversed" | Creates two cards |
| Cloze | front (with {{c1::text}}), back (optional) | Use {{c1::}}, {{c2::}} for deletions |

## Parsing Decks

```bash
parse-deck deck.apkg > cards.json
```

Output format matches input format for round-trip editing.
