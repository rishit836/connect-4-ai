import numpy as np
from ai import get_best_move
import pygame
import math
import sys

game_board = np.zeros((7,6))
pygame.init()
coin_radius = 50
offset = coin_radius/2

screen = pygame.display.set_mode(((len(game_board[0]))*(coin_radius*2)+(offset*2),(len(game_board))*(coin_radius*2)+(offset*2)))

def take_input(game_board,input_player = 1, column = None):
    
    if column is None:
        column = int(input("enter column number from 1-"+str(len(game_board[0]))+" :"))
    if column > len(game_board):
        print("enter a valid column")
    else:
        for r in range(len(game_board)-1,-1,-1):
            if game_board[r][column-1] ==0:
                game_board[r][column-1] = input_player
                break
            else:
                continue
    return game_board

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

    if not np.any(game_board == 0):
        return 0
    return None

def draw_board(game_board,screen):
    for row in range(len(game_board)):
        for col in range(len(game_board[0])):
            if game_board[row][col] == 0:
                pygame.draw.circle(screen,"black",(col*(coin_radius*2)+(offset*2),row*(coin_radius*2)+(offset*2)),coin_radius)
            elif game_board[row][col] == 1:
                pygame.draw.circle(screen,"yellow",(col*(coin_radius*2)+(offset*2),row*(coin_radius*2)+(offset*2)),coin_radius)
            else:
                pygame.draw.circle(screen,"red",(col*(coin_radius*2)+(offset*2),row*(coin_radius*2)+(offset*2)),coin_radius)



turn = 1

clock = pygame.time.Clock()
while True:
    # print(game_board)
    # result = check_winner(game_board)
    # if result is not None:
    #     winner = "human"  if result ==1 else "ai"
    #     print("the winner is",winner)
    #     break
    # game_board = take_input(game_board)
    # result = check_winner(game_board)
    # move = get_best_move(game_board)
    # print("Ai has made the move:")
    # game_board[move]=-1
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            break
        if event.type == pygame.MOUSEBUTTONDOWN and turn ==1:
            mouse_pos = pygame.mouse.get_pos()
            col_num = mouse_pos[0]//(coin_radius*2)
            game_board = take_input(game_board,1,column=col_num+1)
            turn =-1
    screen.fill("blue")
    draw_board(game_board, screen)
    pygame.display.update()
    if turn ==-1:
        move = get_best_move(game_board)
        game_board[move]=-1
        turn = 1
    result = check_winner(game_board)
    if result is not None:
        winner = "human"  if result ==1 else "ai"
        print("the winner is",winner)
        turn = 0
    clock.tick(60)


    
    

