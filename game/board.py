import random

# --- Module-level helpers ---

def _transpose(grid):
    return [list(row) for row in zip(*grid)]


def _reverse_rows(grid):
    return [row[::-1] for row in grid]


def _slide_row_left(row):
    """Compress, merge equal adjacent pairs (no double-merge), and pad with zeros.

    Returns (new_row, score_gained).
    """
    # Step 1: compress — remove zeros
    tiles = [t for t in row if t != 0]
    # Step 2: merge equal adjacent tiles (each tile merges at most once)
    score = 0
    merged = [False] * len(tiles)
    i = 0
    while i < len(tiles) - 1:
        if tiles[i] == tiles[i + 1] and not merged[i]:
            tiles[i] *= 2
            score += tiles[i]
            merged[i] = True
            tiles.pop(i + 1)
            merged.pop(i + 1)
        i += 1
    # Step 3: pad with zeros to restore original length
    tiles += [0] * (len(row) - len(tiles))
    return tiles, score


def _apply_left(grid):
    """Apply _slide_row_left to every row; return (new_grid, total_score)."""
    new_grid = []
    total_score = 0
    for row in grid:
        new_row, score = _slide_row_left(row)
        new_grid.append(new_row)
        total_score += score
    return new_grid, total_score


# Direction transform table.
# Each entry is (pre_transform, post_transform).
# pre is applied to orient the grid so that "left" logic applies;
# post reverses the orientation after sliding.
_TRANSFORMS = {
    "left":  (lambda g: g,                                   lambda g: g),
    "right": (_reverse_rows,                                 _reverse_rows),
    "up":    (_transpose,                                    _transpose),
    "down":  (lambda g: _reverse_rows(_transpose(g)),        lambda g: _transpose(_reverse_rows(g))),
}


# --- Board class ---

class Board:
    SIZE = 4

    def __init__(self, grid=None):
        """Create a Board.

        grid=None  — fresh 4x4 grid of zeros with two tiles spawned.
        grid=list  — initialise from the provided grid (defensive copy, no spawning).
        """
        if grid is None:
            self.grid = [[0] * self.SIZE for _ in range(self.SIZE)]
            self.spawn_tile()
            self.spawn_tile()
        else:
            # Defensive copy — never store a reference to the caller's list.
            self.grid = [row[:] for row in grid]

    def spawn_tile(self):
        """Spawn one tile in a random empty cell.

        Picks a random empty cell and places a 2 (90%) or 4 (10%) there.
        No-op when the board is full.
        """
        empty = [
            (r, c)
            for r in range(self.SIZE)
            for c in range(self.SIZE)
            if self.grid[r][c] == 0
        ]
        if not empty:
            return
        r, c = random.choice(empty)
        self.grid[r][c] = random.choices([2, 4], weights=[9, 1])[0]

    def move(self, direction):
        """Apply a move in the given direction.

        direction: "left" | "right" | "up" | "down" (case-insensitive).

        Returns:
            (new_board, score_gained, moved: bool)

        If nothing moved, returns (self, 0, False) — same instance, no copy.
        If moved, returns (Board(grid=new_grid), score, True) with one tile spawned.
        """
        direction = direction.lower()
        if direction not in _TRANSFORMS:
            raise ValueError(
                f"Invalid direction: {direction!r}. Must be left/right/up/down."
            )

        pre, post = _TRANSFORMS[direction]
        # Work on a copy so self.grid is never mutated.
        working = pre([row[:] for row in self.grid])
        new_grid_inner, score = _apply_left(working)
        new_grid = post(new_grid_inner)

        if new_grid == self.grid:
            return self, 0, False

        new_board = Board(grid=new_grid)
        new_board.spawn_tile()
        return new_board, score, True

    def is_game_over(self):
        """Return True when no valid move exists.

        Uses a direct adjacent-pair scan instead of calling move() four times,
        avoiding temporary Board allocations (important for Expectimax performance).
        """
        # Fast path: any empty cell means at least one slide is possible.
        for row in self.grid:
            if 0 in row:
                return False
        # Check for equal adjacent pairs horizontally.
        for row in self.grid:
            for c in range(self.SIZE - 1):
                if row[c] == row[c + 1]:
                    return False
        # Check for equal adjacent pairs vertically.
        for r in range(self.SIZE - 1):
            for c in range(self.SIZE):
                if self.grid[r][c] == self.grid[r + 1][c]:
                    return False
        return True

    def has_won(self):
        """Return True when any tile equals 2048."""
        return any(cell == 2048 for row in self.grid for cell in row)
