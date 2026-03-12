"""Failing test stubs for the game loop (main module).

These tests define behavioral contracts for DIRECTION_MAP, process_key(), and
check_game_over() exported by main.py.
All tests will raise ImportError (RED state) until Plan 03 creates main.py.
"""
from game.board import Board
from game.main import DIRECTION_MAP, process_key, check_game_over


# ---------------------------------------------------------------------------
# INPUT-01 — DIRECTION_MAP maps WASD to canonical direction strings
# ---------------------------------------------------------------------------

def test_direction_map():
    """DIRECTION_MAP must map w/a/s/d exactly to up/left/down/right."""
    expected = {"w": "up", "s": "down", "a": "left", "d": "right"}
    assert DIRECTION_MAP == expected, (
        f"DIRECTION_MAP mismatch: got {DIRECTION_MAP!r}, expected {expected!r}"
    )


# ---------------------------------------------------------------------------
# INPUT-03 — unrecognised keys are silently ignored (board unchanged)
# ---------------------------------------------------------------------------

def test_invalid_key_ignored():
    """process_key with an unknown key must return the same board instance."""
    board = Board(grid=[[2, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
    returned_board, score, best, won = process_key(
        board, "x", score=0, best=0, won=False
    )
    assert returned_board is board, (
        "process_key with invalid key must return the original board instance"
    )
    assert won is False, "won flag must remain False for an invalid key"


# ---------------------------------------------------------------------------
# INPUT-04 — valid key advances game state (board, score updated)
# ---------------------------------------------------------------------------

def test_loop_state_advance():
    """process_key with 'w' on a mergeable board must increase score and return a Board."""
    # Two 2-tiles in the same column: pressing 'w' (up) merges them into a 4 → score 4
    board = Board(grid=[
        [2, 0, 0, 0],
        [2, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ])
    returned_board, score, best, won = process_key(
        board, "w", score=0, best=0, won=False
    )
    assert isinstance(returned_board, Board), (
        "process_key must return a Board instance as the first element"
    )
    assert score == 4, f"Merging two 2-tiles must yield score 4, got {score}"


# ---------------------------------------------------------------------------
# INPUT-05 — reaching 2048 sets won flag without raising SystemExit
# ---------------------------------------------------------------------------

def test_win_continues():
    """Merging two 1024 tiles must set won=True and must not exit the process."""
    board = Board(grid=[
        [1024, 1024, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ])
    # 'a' (left) merges the two 1024s into 2048
    try:
        returned_board, score, best, won = process_key(
            board, "a", score=0, best=0, won=False
        )
    except SystemExit:
        assert False, "process_key must not call sys.exit() on win — game continues"
    assert won is True, "won flag must be True after reaching 2048"


# ---------------------------------------------------------------------------
# INPUT-06 — check_game_over returns True when no moves remain
# ---------------------------------------------------------------------------

def test_game_over_exits():
    """check_game_over must return True for a full board with no valid moves."""
    # Build a board where no merges are possible (game over)
    board = Board(grid=[
        [2,  4,  2,  4],
        [4,  2,  4,  2],
        [2,  4,  2,  4],
        [4,  2,  4,  2],
    ])
    result = check_game_over(board, score=0)
    assert result is True, (
        "check_game_over must return True when the board has no valid moves"
    )
