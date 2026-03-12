# 2048-AI

A terminal-based 2048 game in Python, with an AI player (Expectimax) coming soon.

## Play

```bash
python3 -m game.main
```

**Controls:** `W A S D` to move · `Q` to quit

## How it works

- **`game/board.py`** — pure game logic: sliding, merging, tile spawning, win/loss detection
- **`game/display.py`** — terminal renderer using ANSI escape codes
- **`game/main.py`** — game loop with raw TTY input (no Enter key needed)

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
│   ├── board.py       # Game logic
│   ├── display.py     # Terminal rendering
│   └── main.py        # Entry point & game loop
└── tests/
    ├── test_board.py
    ├── test_display.py
    └── test_main.py
```

## Roadmap

- [x] Core game logic
- [x] Playable terminal game
- [ ] Expectimax AI player
