import random
import copy

# Initialize board
CANDIES = ['R', 'G', 'B']  # Red, Green, Blue
BOARD_SIZE = 5

def generate_board():
    return [[random.choice(CANDIES) for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

def print_board(board):
    for row in board:
        print(' '.join(row))
    print()

# Check and clear matches
def clear_matches(board):
    score = 0
    cleared = [[False]*BOARD_SIZE for _ in range(BOARD_SIZE)]
    
    # Horizontal matches
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE-2):
            if board[i][j] == board[i][j+1] == board[i][j+2]:
                cleared[i][j] = cleared[i][j+1] = cleared[i][j+2] = True
                score += 10
    
    # Vertical matches
    for j in range(BOARD_SIZE):
        for i in range(BOARD_SIZE-2):
            if board[i][j] == board[i+1][j] == board[i+2][j]:
                cleared[i][j] = cleared[i+1][j] = cleared[i+2][j] = True
                score += 10
    
    # Clear matched candies
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if cleared[i][j]:
                board[i][j] = random.choice(CANDIES)
    return score

# Generate all possible moves
def get_possible_moves(board):
    moves = []
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if j+1 < BOARD_SIZE:
                moves.append(((i,j),(i,j+1)))  # swap right
            if i+1 < BOARD_SIZE:
                moves.append(((i,j),(i+1,j)))  # swap down
    return moves

def make_move(board, move):
    new_board = copy.deepcopy(board)
    (x1, y1), (x2, y2) = move
    new_board[x1][y1], new_board[x2][y2] = new_board[x2][y2], new_board[x1][y1]
    score = clear_matches(new_board)
    return new_board, score

# Minimax algorithm
def minimax(board, depth, is_maximizing):
    if depth == 0:
        return 0
    
    moves = get_possible_moves(board)
    if is_maximizing:
        best_score = float('-inf')
        for move in moves:
            new_board, score = make_move(board, move)
            total_score = score + minimax(new_board, depth-1, False)
            best_score = max(best_score, total_score)
        return best_score
    else:
        worst_score = float('inf')
        for move in moves:
            new_board, score = make_move(board, move)
            total_score = score - minimax(new_board, depth-1, True)
            worst_score = min(worst_score, total_score)
        return worst_score

def recommend_move(board, depth=2):
    best_move = None
    best_score = float('-inf')
    for move in get_possible_moves(board):
        new_board, score = make_move(board, move)
        total_score = score + minimax(new_board, depth-1, False)
        if total_score > best_score:
            best_score = total_score
            best_move = move
    return best_move, best_score

# Main program
board = generate_board()
print("Initial Board:")
print_board(board)

move, score = recommend_move(board)
print(f"Recommended Move: Swap {move} with expected score gain {score}")
