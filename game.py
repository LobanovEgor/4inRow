import pygame as pg
import sys
import math
import random
from minimax import *
from Config import *
from board import *


pg.init()
pg.display.set_caption("Connect 4")

width = COLUMNS * DISC_SIZE
height = (ROWS + 1) * DISC_SIZE
size = (width, height)
screen = pg.display.set_mode(size)

my_font = pg.font.SysFont("Roboto", 60)

def draw_grid(grid):
    for c in range(COLUMNS):
        for r in range(ROWS):
            pg.draw.rect(screen, BLUE, (c * DISC_SIZE, r * DISC_SIZE + DISC_SIZE, DISC_SIZE, DISC_SIZE))
            pg.draw.circle(screen, WHITE, (int(c * DISC_SIZE + DISC_SIZE / 2),
                           int(r * DISC_SIZE + DISC_SIZE + DISC_SIZE /2)), DISC_RADIUS)
    for c in range(COLUMNS):
        for r in range(ROWS):
            if grid[r][c] == PLAYER_PIECE:
                pg.draw.circle(screen, RED, (int(c * DISC_SIZE + DISC_SIZE / 2),
                               height - int(r * DISC_SIZE + DISC_SIZE / 2)), DISC_RADIUS)
            elif grid[r][c] == AI_PLAYER_PIECE:
                pg.draw.circle(screen, YELLOW, (int(c * DISC_SIZE + DISC_SIZE / 2), height - int(r * DISC_SIZE + DISC_SIZE / 2)), DISC_RADIUS)
    pg.display.update()


def search_win_move(grid, piece):
    for c in range(COLUMNS - 3):
        for r in range(ROWS):
            if grid[r][c] == piece and grid[r][c+1] == piece and grid[r][c+2] == piece and grid[r][c+3] == piece:
                return True

    for c in range(COLUMNS):
        for r in range(ROWS-3):
            if grid[r][c] == piece and grid[r+1][c] == piece and grid[r+2][c] == piece and grid[r+3][c] == piece:
                return True
    for c in range(COLUMNS-3):
        for r in range(ROWS-3):
            if grid[r][c] == piece and grid[r+1][c+1] == piece and grid[r + 2][c + 2] == piece and grid[r+3][c+3] == piece:
                return True
    for c in range(COLUMNS-3):
        for r in range(3, ROWS):
            if grid[r][c] == piece and grid[r-1][c+1] == piece and grid[r - 2][c + 2] == piece and grid[r-3][c+3] == piece:
                return True

def evaluate_window(window, piece):
    # by default the oponent is the player
    opponent_piece = PLAYER_PIECE

    # if we are checking from the player's perspective, then the oponent is AI
    if piece == PLAYER_PIECE:
        opponent_piece = AI_PLAYER_PIECE

    # initial score of a window is 0
    score = 0

    # based on how many friendly pieces there are in the window, we increase the score
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2

    # or decrese it if the oponent has 3 in a row
    if window.count(opponent_piece) == 3 and window.count(0) == 1:
        score -= 4

    return score


# scoring the overall attractiveness of a board after a piece has been droppped
def score_position(board, piece):

    score = 0

    # score center column --> we are prioritizing the central column because it provides more potential winning windows
    center_array = [int(i) for i in list(board[:,COLUMNS//2])]
    center_count = center_array.count(piece)
    score += center_count * 6

    # below we go over every single window in different directions and adding up their values to the score
    # score horizontal
    for r in range(ROWS):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLUMNS - 3):
            window = row_array[c:c + 4]
            score += evaluate_window(window, piece)

    # score vertical
    for c in range(COLUMNS):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROWS-3):
            window = col_array[r:r+4]
            score += evaluate_window(window, piece)

    # score positively sloped diagonals
    for r in range(3,ROWS):
        for c in range(COLUMNS - 3):
            window = [board[r-i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)

    # score negatively sloped diagonals
    for r in range(3,ROWS):
        for c in range(3,COLUMNS):
            window = [board[r-i][c-i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score

def minimax(grid, depth, alpha, beta, max_player):
    def is_terminal_node(board):
        return search_win_move(board, PLAYER_PIECE) or search_win_move(board, AI_PLAYER_PIECE) or len(
            get_valid_position(board)) == 0
    valid_position = get_valid_position(grid)
    terminal = is_terminal_node(grid)
    if depth == 0 or terminal:
        if terminal:
            if search_win_move(grid, AI_PLAYER_PIECE):
                return (None, 10**14)

            elif search_win_move(grid, PLAYER_PIECE):
                return (None, -(10**13))
            else:
                return(None, 0)
        else:
            return(None, score_position(grid, AI_PLAYER_PIECE))
    if max_player:
        value = -math.inf
        column = random.choice(valid_position)
        for col in valid_position:
            row = get_next_open_row(grid, col)
            grid_copy = grid.copy()
            grid_copy[row][col] = AI_PLAYER_PIECE
            new_score = minimax(grid_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value
    else:
        value = math.inf
        column = random.choice(valid_position)
        for col in valid_position:
            row = get_next_open_row(grid, col)
            grid_copy = grid.copy()
            grid_copy[row][col] = PLAYER_PIECE
            new_score = minimax(grid_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

def main():
    grid = new_grid()

    draw_grid(grid)
    pg.display.update()

    pick_random = random.randint(PLAYER, AI_PLAYER)

    game_over = False
    while not game_over:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    sys.exit()
            elif event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.MOUSEMOTION:
                pg.draw.rect(screen, WHITE, (0, 0, width, DISC_SIZE))
                position_x = event.pos[0]
                if pick_random == PLAYER:
                    pg.draw.circle(screen, RED, (position_x, int(DISC_SIZE / 2)), DISC_RADIUS)
                    pg.display.update()
            if event.type == pg.MOUSEBUTTONDOWN:
                pg.draw.rect(screen, WHITE, (0, 0, width, DISC_SIZE))
                if pick_random == PLAYER:
                    position_x = event.pos[0]
                    col = int(math.floor(position_x / DISC_SIZE))

                if is_valid_position(grid, col):
                    row = get_next_open_row(grid, col)
                    grid[row][col] = PLAYER_PIECE

                    if search_win_move(grid, PLAYER_PIECE):
                        label = my_font.render("Player 1 wins!", 1, RED)
                        screen.blit(label, (10, 10))
                        game_over = True
                    pick_random += 1
                    pick_random = pick_random % 2
                    draw_grid(grid)

            if pick_random == AI_PLAYER and not game_over:
                col, minimax_score = minimax(grid, 5, -math.inf, math.inf, True)
                if is_valid_position(grid, col):
                    row = get_next_open_row(grid,col)
                    grid[row][col] = AI_PLAYER_PIECE

                    if search_win_move(grid, AI_PLAYER_PIECE):
                        label = my_font.render("Player 2 WINS!", 1, YELLOW)
                        screen.blit(label, (10, 10))
                        game_over = True
                    draw_grid(grid)
                    pick_random += 1
                    pick_random = pick_random % 2
    if game_over:
        pg.time.wait(2500)

if __name__ == '__main__':
    main()
    pg.quit()