import pygame, copy
from chess_pawn import Pawn, Knight, Bishop, Rook, Queen, King

# Define some colors
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)
DARK_GREEN = (0, 153, 0)
RED = (204, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 100
HEIGHT = 100

# Initialize Pygame
pygame.init()

# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [800, 800]
screen = pygame.display.set_mode(WINDOW_SIZE)

# Set the title of the window
pygame.display.set_caption("Chessboard")


# Used to manage how fast the screen updates
clock = pygame.time.Clock()

## position - [y,x]
## lowercase letters are black, uppercase are white


## Create list of figures in figures
def create_figures(board):
    figures = []
    for y, line in enumerate(board):
        for x, figure  in enumerate(line):
            if figure == 'p':
                figures.append(Pawn(x, y, 'black', 'p'))
            elif figure == 'h':
                figures.append(Knight(x, y, 'black', 'h'))
            elif figure == 'm':
                figures.append(Bishop(x, y, 'black', 'm'))
            elif figure == 't':
                figures.append(Rook(x, y, 'black', 't'))
            elif figure == 'q':
                figures.append(Queen(x, y, 'black', 'q'))
            elif figure == 'k':
                figures.append(King(x, y, 'black', 'k'))
            elif figure == 'P':
                figures.append(Pawn(x, y, 'white', 'P'))
            elif figure == 'H':
                figures.append(Knight(x, y, 'white', 'H'))
            elif figure == 'M':
                figures.append(Bishop(x, y, 'white', 'M'))
            elif figure == 'T':
                figures.append(Rook(x, y, 'white', 'T'))
            elif figure == 'Q':
                figures.append(Queen(x, y, 'white', 'Q'))
            elif figure == 'K':
                figures.append(King(x, y, 'white', 'K'))

    return figures

## Clears the board
def erase_grid(check):
    grid = []
    for row in range(8):
        grid.append([])
        for column in range(8):
            if row % 2 == 0:
                if column % 2 == 0:
                    color = WHITE
                else:
                    color = GRAY
            else:
                if column % 2 == 0:
                    color = GRAY
                else:
                    color = WHITE
            grid[row].append(color)
    if check != None:
        grid[check[0]][check[1]] = RED
    return grid

      

def draw_board(figures, grid):
    # Create the chessboard pattern
    for row in range(8):
        for column in range(8):

            color = grid[row][column]

            pygame.draw.rect(screen,
                            color,
                            [(WIDTH) * column,
                            (HEIGHT) * row,
                            WIDTH,
                            HEIGHT])
    
    for figure in figures:
        screen.blit(figure.object_image, (figure.object.x + 10, figure.object.y + 10))


## Higlights where selected figure can move and if it's occupied by an enemy
def highlight_moves(movable_positions, grid, board):
    for pos in movable_positions:
        if board[pos[0]][pos[1]] in 'hmtqkpHMTQKP':
            grid[pos[0]][pos[1]] = RED
        else:
            grid[pos[0]][pos[1]] = DARK_GREEN
    pass

## Higlights the sellected figure 
def highlight_selected_figure(figure_picked, grid):
    grid[figure_picked.pos_y][figure_picked.pos_x] = YELLOW

## Selects a particular figure on a board
def get_figure(figures, mouse_pos, player):
    for figure in figures:
        if figure.object.x <= mouse_pos[0] and figure.object.x + WIDTH >= mouse_pos[0] and figure.object.y <= mouse_pos[1] and figure.object.y + HEIGHT >= mouse_pos[1]:
            if player == figure.color:
                return figure
            else:
                return None
    return None
## Checks if position where we want figure to go is valid (figure can go there)
def is_valid_move(movable_positions, new_x_pos, new_y_pos):
    our_pos = [new_y_pos, new_x_pos]
    if our_pos in movable_positions:
        return True
    return False


## Responsible for killing an enemy 
def remove_captured_figure(figures, x_pos, y_pos, player_turn):
    for index, figure in enumerate(figures):
        if figure.pos_x == x_pos and figure.pos_y == y_pos:
            if player_turn != figure.color:
                del figures[index]
                return figures
    return figures

## Checks if player's king will be under attack if player moves his figure (figure_picked)
def is_king_in_check(position, figure_picked, board, player_turn, figures):

    local_board = copy.deepcopy(board)
    local_board[figure_picked.pos_y][figure_picked.pos_x] = '0'   ## updating board position
    local_board[position[0]][position[1]] = figure_picked.symbol

    for figure in figures:
        if figure.color != player_turn:

            if figure.pos_x == position[1] and figure.pos_y == position[0]: ##allows picked_figure to kill figure that is threatning a king
                if figure_picked.symbol != 'k' or figure_picked.symbol != 'K': ## king canot kill a figure if he would be check again
                    return False
            
            figure_positions = figure.check_if_can_move(local_board)
            for figure_position in figure_positions:
                if player_turn == 'white':
                    if local_board[figure_position[0]][figure_position[1]] == 'K':
                        return True
                elif player_turn == 'black':
                    if local_board[figure_position[0]][figure_position[1]] == 'k':
                        return True
    return False

## Check if moving somewhere will cause own king to be under check
def movable_positions_without_check(movable_positions, figure_picked, board, player, figures):
    new_movable_positions = []
    for position in movable_positions:
        if not is_king_in_check(position, figure_picked, board, player, figures):
            new_movable_positions.append(position)

    return new_movable_positions
def get_movable_positions(board, figure_picked, player_turn, figures):   
    movable_positions = figure_picked.check_if_can_move(board)
    movable_positions = movable_positions_without_check(movable_positions, figure_picked, board, player_turn, figures)

    return movable_positions

## Check if enemy king is under check
def check_if_check(board, player_turn, figures, grid, check):
    for figure in figures:
        if figure.color == player_turn:
            positions = figure.check_if_can_move(board)
            for position in positions:
                if player_turn == 'white' and board[position[0]][position[1]] == 'k':
                    grid[position[0]][position[1]] = RED
                    check = position[0],position[1]
                    return grid, check
                if player_turn == 'black' and board[position[0]][position[1]] == 'K':

                    grid[position[0]][position[1]] = RED
                    check = position[0],position[1]
                    return grid, check
    check = None
    return grid, check

## Check if anny figure of a current player has an option to move
def check_if_no_more_moves(figures, player, board):
    for figure in figures:
        if figure.color == player:
            movable_positions = get_movable_positions(board, figure, player, figures)
            if movable_positions != []:
                return False
    return True


def main():

    ## define how board looks
    board = [   
            ['t','h','m','q','k','m','h','t'],
            ['p','p','p','p','p','p','p','p'],
            ['0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0'],
            ['P','P','P','P','P','P','P','P'],
            ['T','H','M','Q','K','M','H','T']
        ]
    done = False
    figures = create_figures(board)
    player_turn = 'white'
    enemy_turn = 'black'
    figure_picked = None
    movable_positions = None
    check = None
    grid  = erase_grid(check)

    while not done:
        # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif pygame.mouse.get_pressed()[0]:
                m_pos = pygame.mouse.get_pos()

                if figure_picked == None:
                    figure_picked = get_figure(figures, m_pos, player_turn)

                    if figure_picked != None:

                        movable_positions = get_movable_positions(board, figure_picked, player_turn, figures)
                        highlight_moves(movable_positions, grid, board)
                        highlight_selected_figure(figure_picked, grid)

                elif figure_picked != None:

                    new_x_pos = (m_pos[0]//WIDTH)
                    new_y_pos = (m_pos[1]//HEIGHT)

                    if is_valid_move(movable_positions, new_x_pos, new_y_pos):

                        board[figure_picked.pos_y][figure_picked.pos_x] = '0'   ## updating board position
                        board[new_y_pos][new_x_pos] = figure_picked.symbol
                        
                        figure_picked.object.x = 100*new_x_pos  ## updating sprite position
                        figure_picked.object.y = 100*new_y_pos
                        figure_picked.pos_x = new_x_pos     ## updating object position
                        figure_picked.pos_y = new_y_pos

                        figures = remove_captured_figure(figures, new_x_pos, new_y_pos, player_turn)

                        grid, check = check_if_check(board, player_turn, figures, grid, check)

                        if check != None:
                            if check_if_no_more_moves(figures, enemy_turn, board):
                                print(f'%s won' % player_turn)
                                main()

                        elif check == None:
                            if check_if_no_more_moves(figures, enemy_turn, board):
                                print('draw')
                                main()

                        for element in board:  ## control loop
                            print(element)

                        ## Change which player's turn
                        temp = player_turn
                        player_turn = enemy_turn
                        enemy_turn = temp
                    
                    figure_picked = None

                    grid = erase_grid(check)


        draw_board(figures, grid)

        pygame.display.flip()

        # --- Limit to 60 frames per second
        clock.tick(60)

    # Close the window and quit.
    pygame.quit()

if __name__ == '__main__':
    main()