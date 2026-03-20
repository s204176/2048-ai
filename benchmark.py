import game.ai as ai
from game.board import Board
from game.ai import best_move

def run_game(depth=3):
    board = Board()
    score = 0

    while True:
        direction = best_move(board, depth=depth)
        if direction is None:
            break
        board, gained, moved = board.move(direction)
        score += gained

    max_tile = max(cell for row in board.grid for cell in row)
    return score, max_tile


def benchmark(n=20, depth=3, empty_weight=100, max_tile_weight=10, monotonicity_weight=25):
    ai.EMPTY_WEIGHT = empty_weight
    ai.MAX_TILE_WEIGHT = max_tile_weight
    ai.MONOTONICITY_WEIGHT = monotonicity_weight
    print(f"Running {n} games at depth {depth} | empty={empty_weight}, max_tile={max_tile_weight}, monotonicity={monotonicity_weight}...\n")

    scores = []
    max_tiles = []

    for i in range(1, n + 1):
        score, max_tile = run_game(depth)
        scores.append(score)
        max_tiles.append(max_tile)
        print(f"  Game {i:>2}: score={score:>6}  max_tile={max_tile}")

    print(f"\n--- Results ---")
    print(f"  Avg score:       {sum(scores) / n:.0f}")
    print(f"  Max score:       {max(scores)}")
    print(f"  Avg max tile:    {sum(max_tiles) / n:.0f}")
    print(f"  Best max tile:   {max(max_tiles)}")
    print(f"  % reached  512:  {sum(t >= 512  for t in max_tiles) / n * 100:.0f}%")
    print(f"  % reached 1024:  {sum(t >= 1024 for t in max_tiles) / n * 100:.0f}%")
    print(f"  % reached 2048:  {sum(t >= 2048 for t in max_tiles) / n * 100:.0f}%")
    print()


if __name__ == "__main__":
    print("=== Experiment 1: Empty cell weight sweep (max_tile=10, monotonicity=25) ===\n")
    for w in [25, 50, 100, 200, 400]:
        benchmark(empty_weight=w, max_tile_weight=10, monotonicity_weight=25)

    print("=== Experiment 2: Max tile weight sweep (empty=100, monotonicity=25) ===\n")
    for w in [1, 5, 10, 20, 50]:
        benchmark(empty_weight=100, max_tile_weight=w, monotonicity_weight=25)
