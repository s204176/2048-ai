import sys

CELL_WIDTH = 6


def _clear():
    sys.stdout.write('\033[2J\033[H')
    sys.stdout.flush()


def _format_cell(value):
    return '.' if value == 0 else str(value)


def _print_grid(grid):
    sep = '+' + ('-' * CELL_WIDTH + '+') * 4
    for row in grid:
        print(sep)
        row_str = '|' + '|'.join(_format_cell(c).center(CELL_WIDTH) for c in row) + '|'
        print(row_str)
    print(sep)


def render(board, score, best_score):
    _clear()
    print(f"Score: {score}   Best: {best_score}")
    print()
    _print_grid(board.grid)
    print()
    print("W/A/S/D to move   Q to quit")
