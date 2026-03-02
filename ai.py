import random
import numpy as np

def get_available_moves(game_board):
    moves = []
    seen_cols = set()
    for r in range(len(game_board)-1,-1,-1):
        for c,col in enumerate(game_board[r]):
            if c in seen_cols:
                continue
            if col == 0:
                moves.append((r,c))
                seen_cols.add(c)
    return moves


def get_children(game_board, player):
    children = []
    for move in get_available_moves(game_board):
        new_board = game_board.copy()
        new_board[move] = player
        children.append(new_board)
    return children


def minimax(game_board, player,depth=0,max_depth=3):

    result = check_winner(game_board)
    if result is not None:
        if result == -1:
            return 1
        if result == 1:
            return -1
        return 0
    
    if depth>=max_depth:
        return 0
        


    if player == 1: #minimize
        best_score = np.inf
        for child in get_children(game_board,player):
            score = minimax(child,-player,depth=depth+1)
            best_score = min(score,best_score)
        return best_score
    else:#maximize
        best_score = -np.inf
        for child in get_children(game_board,player):
            score = minimax(child,-player,depth=depth+1)
            best_score=max(score,best_score)
        return best_score
    

def check_winner(game_board):
    rows, cols = game_board.shape
    W = 4

    # Horizontal
    for r in range(rows):
        for c in range(cols - W + 1):
            window = game_board[r, c:c+W]
            if np.all(window == 1):
                return 1
            if np.all(window == -1):
                return -1

    # Vertical
    for c in range(cols):
        for r in range(rows - W + 1):
            window = game_board[r:r+W, c]
            if np.all(window == 1):
                return 1
            if np.all(window == -1):
                return -1

    # Diagonal down-right
    for r in range(rows - W + 1):
        for c in range(cols - W + 1):
            window = np.array([game_board[r+i, c+i] for i in range(W)])
            if np.all(window == 1):
                return 1
            if np.all(window == -1):
                return -1

    # Diagonal down-left
    for r in range(rows - W + 1):
        for c in range(W - 1, cols):
            window = np.array([game_board[r+i, c-i] for i in range(W)])
            if np.all(window == 1):
                return 1
            if np.all(window == -1):
                return -1

    # Draw / ongoing
    if np.all(game_board != 0):
        return 0
    return None

def get_best_move(game_board):

    best_moves = []

    best_score = -np.inf
    for move in get_available_moves(game_board):
        new_board = game_board.copy()
        new_board[move] = -1
        score = minimax(new_board,player=1,depth=1)
        if score > best_score:
            best_score = score
            best_moves = [move]
        elif score == best_score:
            best_moves.append(move)

    return random.choice(best_moves) if best_moves else None
    