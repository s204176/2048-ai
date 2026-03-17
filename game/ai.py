from game.board import Board
import math

DIRECTIONS = ['left', 'right', 'up', 'down']

def get_empty_count(board):
    empty_count = 0
    for row in board.grid:
        for cell in row:
            if cell == 0:
                empty_count += 1
    return empty_count

def get_max_tile(board):
    max_tile = 0
    for row in board.grid:
        for cell in row:
            if cell > max_tile:
                max_tile = cell
    return max_tile



def get_heuristic_score(board):
    empty_count = get_empty_count(board)
    max_tile = get_max_tile(board)

    # Here we weigh how much each part of the heuristic contributes... fiddle with this to see how it changes the AI's behavior
    return empty_count * 100 + math.log2(max_tile) * 10


def expectimax(board, depth, is_maximizing):
    if depth == 0 or board.is_game_over():
        return get_heuristic_score(board)
    
    if is_maximizing:
        max_score = float('-inf')
        for direction in DIRECTIONS:
            new_board, score_gained, moved = board.move(direction)
            if not moved:
                continue

            score = score_gained + expectimax(new_board, depth - 1, False)
            max_score = max(max_score, score)

        if max_score == float('-inf'):
            return get_heuristic_score(board)

        return max_score
    
    else:
        total_score = 0

        empty_cells = []

        for r in range(board.SIZE):
            for c in range(board.SIZE):
                if board.grid[r][c] == 0:
                    empty_cells.append((r, c))

        if not empty_cells:
            return get_heuristic_score(board)
        
        probability_per_cell = 1 / len(empty_cells)

        for r, c in empty_cells:
            for value, prob in [(2, 0.9), (4, 0.1)]:
                new_grid = [row[:] for row in board.grid]

                new_board = Board(grid=new_grid)

                new_board.grid[r][c] = value
                score = expectimax(new_board, depth - 1, True)

                total_score += probability_per_cell * prob * score
        return total_score
    
def best_move(board, depth):
    best_direction = None
    best_score = float('-inf')
    for direction in DIRECTIONS:
        new_board, score_gained, moved = board.move(direction)
        if not moved:
            continue
        score = score_gained + expectimax(new_board, depth - 1, False)
        if score > best_score:
            best_score = score
            best_direction = direction
    return best_direction