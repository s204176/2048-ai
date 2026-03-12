"""Failing test stubs for the display module.

These tests define the behavioral contracts for display.render().
All tests will raise ImportError (RED state) until Plan 02 creates display.py.
"""
import io
from unittest.mock import patch
from game.board import Board
from game import display  # noqa: F401


def _render_output(board, score=0, best=0):
    """Capture everything render() writes to stdout and return it as a string."""
    buf = io.StringIO()
    with patch("sys.stdout", new=buf):
        display.render(board, score, best)  # type: ignore
    return buf.getvalue()


def _empty_board():
    """Return a 4x4 all-zero Board (no tiles spawned)."""
    return Board(grid=[[0] * 4 for _ in range(4)])


# ---------------------------------------------------------------------------
# DISP-01 / STRUCT-03 — render() is a callable that accepts (board, score, best)
# ---------------------------------------------------------------------------

def test_render_interface():
    """display.render must exist, be callable, and accept (board, score, best)."""
    assert callable(display.render), "display.render must be callable"
    board = _empty_board()
    # Must not raise any exception
    _render_output(board, score=0, best=0)


# ---------------------------------------------------------------------------
# DISP-02 — output starts with ANSI clear-screen escape sequence
# ---------------------------------------------------------------------------

def test_render_clears_screen():
    """render() must write '\\033[2J\\033[H' at the start of every frame."""
    board = _empty_board()
    output = _render_output(board)
    assert output.startswith("\033[2J\033[H"), (
        "render() must begin with ANSI clear-screen escape '\\033[2J\\033[H'"
    )


# ---------------------------------------------------------------------------
# DISP-03 — cell values are padded to exactly 6 characters between '|' separators
# ---------------------------------------------------------------------------

def test_cell_padding():
    """Each cell in the grid display must be exactly 6 characters wide."""
    board = _empty_board()
    output = _render_output(board)
    # Find lines that contain '|' — these are grid rows
    row_lines = [line for line in output.splitlines() if "|" in line]
    assert row_lines, "render() must produce lines containing '|' separators"
    for line in row_lines:
        parts = line.split("|")
        # parts[0] is before first '|', parts[-1] is after last '|'
        # inner cells are parts[1:-1]
        inner_cells = parts[1:-1]
        assert inner_cells, f"Row line has no inner cells: {line!r}"
        for cell in inner_cells:
            assert len(cell) == 6, (
                f"Cell {cell!r} has width {len(cell)}, expected 6"
            )


# ---------------------------------------------------------------------------
# DISP-04 — score and best score appear in the rendered output
# ---------------------------------------------------------------------------

def test_score_display():
    """render(board, 42, 100) must include '42' and '100' in its output."""
    board = _empty_board()
    output = _render_output(board, score=42, best=100)
    assert "42" in output, "Current score '42' must appear in rendered output"
    assert "100" in output, "Best score '100' must appear in rendered output"


# ---------------------------------------------------------------------------
# DISP-05 — controls hint includes 'W' and 'Q'
# ---------------------------------------------------------------------------

def test_controls_hint():
    """render() must include movement key 'W' and quit key 'Q' in its output."""
    board = _empty_board()
    output = _render_output(board)
    output_upper = output.upper()
    assert "W" in output_upper, "Controls hint must mention 'W' (move up)"
    assert "Q" in output_upper, "Controls hint must mention 'Q' (quit)"


# ---------------------------------------------------------------------------
# DISP-05 — empty cells are rendered as '.'
# ---------------------------------------------------------------------------

def test_empty_cells():
    """An all-zero board must render each empty cell as '.'."""
    board = _empty_board()
    output = _render_output(board)
    assert "." in output, (
        "Empty cells (value 0) must be displayed as '.' in the rendered output"
    )
