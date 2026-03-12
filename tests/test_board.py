from board import Board
import random


# STRUCT-01: Board exposes the required interface
def test_board_interface():
    b = Board()
    assert hasattr(b, "spawn_tile"), "Board must have spawn_tile method"
    assert hasattr(b, "move"), "Board must have move method"
    assert hasattr(b, "is_game_over"), "Board must have is_game_over method"
    assert hasattr(b, "has_won"), "Board must have has_won method"


# BOARD-01: Board initialises with exactly 2 tiles (2 or 4) on a 4x4 grid
def test_init_two_tiles():
    b = Board()
    assert isinstance(b.grid, list), "grid must be a list"
    assert len(b.grid) == 4, "grid must have 4 rows"
    for row in b.grid:
        assert len(row) == 4, "each row must have 4 columns"
    non_zero = sum(1 for row in b.grid for cell in row if cell != 0)
    assert non_zero == 2, f"expected exactly 2 non-zero tiles, got {non_zero}"
    for row in b.grid:
        for cell in row:
            if cell != 0:
                assert cell in (2, 4), f"initial tiles must be 2 or 4, got {cell}"


# BOARD-02: spawn_tile places a 2 with ~90% probability and a 4 with ~10%
def test_spawn_probability():
    twos = 0
    fours = 0
    trials = 1000
    for _ in range(trials):
        b = Board(grid=[[0] * 4 for _ in range(4)])
        b.spawn_tile()
        value = next(cell for row in b.grid for cell in row if cell != 0)
        if value == 2:
            twos += 1
        elif value == 4:
            fours += 1
    proportion_twos = twos / trials
    assert 0.85 <= proportion_twos <= 0.95, (
        f"expected ~90% twos, got {proportion_twos:.2%} over {trials} trials"
    )


# BOARD-03: move() accepts all four direction strings without raising
def test_move_directions():
    start_grid = [[2, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    for direction in ("left", "right", "up", "down"):
        b = Board(grid=[row[:] for row in start_grid])
        result = b.move(direction)
        assert isinstance(result, tuple) and len(result) == 3, (
            f"move('{direction}') must return a 3-tuple"
        )
        new_board, score, moved = result
        assert isinstance(new_board, Board)
        assert isinstance(score, int)
        assert isinstance(moved, bool)


# BOARD-04: tiles slide to the far end of the direction
def test_slide_to_end():
    start_grid = [[2, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    b = Board(grid=start_grid)
    new_board, score, moved = b.move("right")
    assert moved is True, "moving right when tile can slide must set moved=True"
    # After slide: original tile is at index 3 of row 0. Exactly 2 non-zero cells
    # (slid tile + one new spawn).
    non_zero = sum(1 for row in new_board.grid for cell in row if cell != 0)
    assert non_zero == 2, f"expected 2 non-zero cells after move+spawn, got {non_zero}"
    assert new_board.grid[0][3] == 2, (
        "the 2-tile must have slid to column 3 of row 0"
    )


# BOARD-05: two equal adjacent tiles merge into their sum
def test_merge_equal():
    b = Board(grid=[[2, 2, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
    new_board, score, moved = b.move("left")
    assert moved is True
    assert score == 4, f"merging two 2s must give score 4, got {score}"
    assert new_board.grid[0][0] == 4, (
        f"merged tile must be 4 at grid[0][0], got {new_board.grid[0][0]}"
    )


# BOARD-06: a row of four equal tiles merges as two pairs, not a chain
def test_no_double_merge():
    b = Board(grid=[[2, 2, 2, 2], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
    new_board, score, moved = b.move("left")
    assert score == 8, f"merging [2,2,2,2] left must give score 8, got {score}"
    assert new_board.grid[0][0] == 4, f"grid[0][0] must be 4, got {new_board.grid[0][0]}"
    assert new_board.grid[0][1] == 4, f"grid[0][1] must be 4, got {new_board.grid[0][1]}"


# BOARD-07: move spawns exactly one new tile; original board is not mutated
def test_spawn_after_move():
    start_grid = [[2, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    original_grid = [row[:] for row in start_grid]
    b = Board(grid=start_grid)
    new_board, score, moved = b.move("right")
    # Exactly 2 non-zero cells: slid tile + spawned tile
    non_zero = sum(1 for row in new_board.grid for cell in row if cell != 0)
    assert non_zero == 2, f"expected 2 non-zero cells, got {non_zero}"
    # Original board is unchanged
    for r in range(4):
        for c in range(4):
            assert b.grid[r][c] == original_grid[r][c], (
                "move() must not mutate the original board"
            )
    # Sanity: moving left on same start board also reports moved=True
    b2 = Board(grid=[row[:] for row in original_grid])
    _, _, moved_left = b2.move("left")
    assert moved_left is False, (
        "moving left when tile is already at column 0 should not move"
    )


# BOARD-08: score accumulates correctly across multiple merges in one move
def test_score_accumulation():
    b = Board(grid=[[2, 2, 4, 4], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
    new_board, score, moved = b.move("left")
    assert score == 12, (
        f"merging [2,2,4,4] left: 2+2=4 and 4+4=8 → total 12, got {score}"
    )


# STRUCT-02: move() return value has the correct types
def test_move_return_signature():
    b = Board(grid=[[2, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
    result = b.move("left")
    assert isinstance(result, tuple) and len(result) == 3, (
        "move() must return a tuple of length 3"
    )
    assert isinstance(result[0], Board), "result[0] must be a Board instance"
    assert isinstance(result[1], int), "result[1] (score) must be an int"
    assert isinstance(result[2], bool), "result[2] (moved) must be a bool"


# BOARD-09: is_game_over detects when no moves remain (and when they do)
def test_game_over():
    full_grid = [
        [2, 4, 2, 4],
        [4, 2, 4, 2],
        [2, 4, 2, 4],
        [4, 2, 4, 2],
    ]
    assert Board(grid=full_grid).is_game_over() is True, (
        "checkerboard with no merges or empty cells must be game over"
    )
    empty_cell_grid = [
        [2, 4, 2, 4],
        [4, 2, 4, 2],
        [2, 4, 2, 4],
        [4, 2, 4, 0],  # one empty cell
    ]
    assert Board(grid=empty_cell_grid).is_game_over() is False, (
        "board with an empty cell must not be game over"
    )


# BOARD-10: has_won returns True iff a 2048 tile is present
def test_has_won():
    winning_grid = [[2048, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    assert Board(grid=winning_grid).has_won() is True, (
        "board with 2048 tile must report has_won=True"
    )
    not_won_grid = [[1024, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    assert Board(grid=not_won_grid).has_won() is False, (
        "board without 2048 tile must report has_won=False"
    )
