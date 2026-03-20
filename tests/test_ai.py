from game.board import Board
from game.ai import get_empty_count, get_max_tile, get_heuristic_score, best_move


# AI-01: get_empty_count returns correct count
# A fully filled board has no empty cells, so the count must be 0.
def test_empty_count_full():
    b = Board(grid=[[2, 4, 2, 4], [4, 2, 4, 2], [2, 4, 2, 4], [4, 2, 4, 2]])
    assert get_empty_count(b) == 0

# One tile placed in the top-left corner leaves the remaining 15 cells empty.
def test_empty_count_partial():
    b = Board(grid=[[2, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
    assert get_empty_count(b) == 15

# An all-zero board has all 16 cells empty.
def test_empty_count_empty_board():
    b = Board(grid=[[0] * 4 for _ in range(4)])
    assert get_empty_count(b) == 16


# AI-02: get_max_tile returns the largest tile
# With tiles 2, 4, 8, 16 in row 0, the max should be 16.
def test_max_tile_basic():
    b = Board(grid=[[2, 4, 8, 16], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
    assert get_max_tile(b) == 16

# A lone 1024 tile anywhere on the board should be identified as the max.
def test_max_tile_single():
    b = Board(grid=[[0, 0, 0, 0], [0, 1024, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
    assert get_max_tile(b) == 1024


# AI-03: get_heuristic_score rewards more empty cells
# A nearly-empty board should outscore a nearly-full one because
# empty cells carry a weight of 100 vs. log2(max_tile) * 10 for the tile term.
def test_heuristic_more_empty_is_better():
    few_empty = Board(grid=[[2, 4, 8, 16], [32, 64, 128, 256], [2, 4, 8, 16], [32, 64, 128, 0]])
    many_empty = Board(grid=[[2, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
    assert get_heuristic_score(many_empty) > get_heuristic_score(few_empty)

# With the same number of empty cells, a board with a larger max tile should
# score higher because of the log2(max_tile) * 10 term.
def test_heuristic_higher_max_tile_is_better():
    low = Board(grid=[[2, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
    high = Board(grid=[[1024, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
    assert get_heuristic_score(high) > get_heuristic_score(low)


# AI-04: best_move returns a valid direction
# On a normal board with room to move, best_move must return one of the four
# valid direction strings, never None or an unexpected value.
def test_best_move_returns_direction():
    b = Board(grid=[[2, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
    move = best_move(b, depth=2)
    assert move in ("left", "right", "up", "down"), f"unexpected move: {move}"

# On a fully locked checkerboard (no empty cells, no adjacent equal tiles),
# no direction produces a valid move, so best_move should return None.
def test_best_move_no_moves_returns_none():
    b = Board(grid=[
        [2, 4, 2, 4],
        [4, 2, 4, 2],
        [2, 4, 2, 4],
        [4, 2, 4, 2],
    ])
    move = best_move(b, depth=2)
    assert move is None, f"expected None for locked board, got {move}"

# Two 2-tiles sitting at the right end of the top row can only be usefully
# merged by sliding left. Verifies the AI picks the clearly correct move.
def test_best_move_obvious_merge():
    b = Board(grid=[
        [0, 0, 2, 2],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ])
    move = best_move(b, depth=2)
    assert move == "left", f"expected 'left' to merge tiles, got '{move}'"
