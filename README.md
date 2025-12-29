# AnkiSkill

A Python tool for creating, parsing, and editing Anki flashcard decks (.apkg files). Designed as a "skill" for AI assistants to work with Anki decks programmatically using JSON as an intermediate format.

## Installation

Requires Python 3.13+ and [uv](https://docs.astral.sh/uv/).

```bash
# Install globally as a uv tool (recommended for Claude Code skill)
uv tool install -e .

# Or for local development only
uv sync
```

## Claude Code Skill Setup

To use this as a Claude Code skill across all your projects:

1. **Install the commands globally:**
   ```bash
   uv tool install -e /path/to/AnkiSkill
   ```

2. **Copy the skill definition:**
   ```bash
   mkdir -p ~/.claude/skills/anki
   cp SKILL.md ~/.claude/skills/anki/
   ```

3. **Use it:** In any project, ask Claude to create flashcards or work with Anki decks. Claude will automatically detect and use the skill.

## Usage

### Creating a Deck

1. Create a JSON file with your cards:

```json
{
  "deck_name": "My Flashcards",
  "cards": [
    {"front": "What is the capital of France?", "back": "Paris"},
    {"front": "H2O", "back": "Water", "type": "reversed"},
    {"front": "The {{c1::mitochondria}} is the powerhouse of the {{c2::cell}}", "back": "", "type": "cloze"}
  ]
}
```

2. Generate the .apkg file:

```bash
uv run create-deck input.json output.apkg
```

### Parsing a Deck

Extract cards from an existing .apkg file to JSON:

```bash
uv run parse-deck deck.apkg > cards.json
```

### Editing a Deck

1. Parse the existing deck to JSON
2. Modify the JSON
3. Recreate the deck

```bash
uv run parse-deck original.apkg > cards.json
# Edit cards.json
uv run create-deck cards.json modified.apkg
```

## Card Types

| Type | Description | Example |
|------|-------------|---------|
| `basic` | Standard front/back card (default) | `{"front": "Q", "back": "A"}` |
| `reversed` | Creates two cards (front→back and back→front) | `{"front": "Term", "back": "Definition", "type": "reversed"}` |
| `cloze` | Cloze deletion cards | `{"front": "{{c1::Answer}} in context", "back": "Extra info", "type": "cloze"}` |

## Development

```bash
# Install dev dependencies
uv sync

# Run type checker
uv run pyright

# Run linter
uv run ruff check
```

## License

MIT
