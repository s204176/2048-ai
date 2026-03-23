# 2048-AI

A terminal-based 2048 game in Python, with an AI player (Expectimax) coming soon.

## Play

```bash
python3 -m game.main
```

**Controls:** `W A S D` to move · `Q` to quit

## AI plays

```bash
python3 -m game.main --auto
```

## How it works

- **`game/board.py`** — pure game logic: sliding, merging, tile spawning, win/loss detection
- **`game/display.py`** — terminal renderer using ANSI escape codes
- **`game/main.py`** — game loop with raw TTY input (no Enter key needed)
- **`game/ai.py`** — ai logic with heuristics and expectimax

No external dependencies — standard library only.

## Run tests

```bash
python3 -m pytest tests/
```

23 tests covering board logic, display output, and input handling.

## Project structure

```
2048-ai/
├── game/
│   ├── ai.py          # AI logic
│   ├── board.py       # Game logic
│   ├── display.py     # Terminal rendering
│   └── main.py        # Entry point & game loop

└── tests/
    ├── test_ai.py
    ├── test_board.py
    ├── test_display.py
    └── test_main.py
```

## Heuristic design notes

**Why log2 for monotonicity:** Tile values are exponential (2, 4, 8, 16...), so raw differences between large tiles dwarf those between small ones even when they represent the same structural disorder. Log2 normalises this so every one-step break in ordering costs the same penalty regardless of tile magnitude.

## Roadmap

- [x] Core game logic
- [x] Playable terminal game
- [x] Expectimax AI player
