import sys
import time

from game.ai import best_move
from .board import Board
from .display import render

DIRECTION_MAP = {'w': 'up', 's': 'down', 'a': 'left', 'd': 'right'}


def get_key():
    if sys.platform == "win32":
        import msvcrt
        ch = msvcrt.getch()
        if ch in (b'\x00', b'\xe0'):  # Arrow keys send two bytes on Windows
            ch = msvcrt.getch()
            return {b'H': 'up', b'P': 'down', b'K': 'left', b'M': 'right'}.get(ch, '')
        return ch.decode('utf-8', errors='ignore')
    else:
        import tty, termios
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
        return ch

def process_key(board, key, score, best, won):
    """Apply one keypress to the game state. Pure function — no I/O.

    Returns (board, score, best, won).
    Invalid or non-moving keys return inputs unchanged.
    """
    if key not in DIRECTION_MAP:
        return board, score, best, won

    new_board, gained, moved = board.move(DIRECTION_MAP[key])
    if not moved:
        return board, score, best, won

    score += gained
    if score > best:
        best = score

    if new_board.has_won() and not won:
        won = True

    return new_board, score, best, won


def check_game_over(board, score):
    """Return True when the board has no valid moves."""
    return board.is_game_over()


def main():
    auto = '--auto' in sys.argv or '-a' in sys.argv
    board = Board()
    score = 0
    best = 0
    won = False

    render(board, score, best)

    while True:
        if auto:
            time.sleep(0.1)  # Small delay to make it watchable
            direction=best_move(board, depth=3)
            if direction is None:
                print(f"\nGame over! Final score: {score}")
                break
            key = {'up': 'w', 'down': 's', 'left': 'a', 'right': 'd'}[direction]
        else:
            try:
                key = get_key()
            except KeyboardInterrupt:
                break

            if key == 'q':
                break

        prev_board = board
        board, score, best, won = process_key(board, key, score, best, won)

        if board is prev_board:
            continue  # Nothing moved, skip render

        render(board, score, best)

        if won:
            # Print win message below board (stays until next keypress clears screen)
            print("\n*** You reached 2048! Keep going! ***")

        if check_game_over(board, score):
            print(f"\nGame over! Final score: {score}")
            break


if __name__ == '__main__':
    main()
