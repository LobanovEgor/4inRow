from board import get_valid_position

def minimax(grid, depth, alpha, beta, max_player):
    valid_position = get_valid_position(grid)
    terminal = is_terminal_node(grid)