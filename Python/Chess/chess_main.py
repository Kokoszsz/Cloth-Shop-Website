import pygame, copy, time
from chess_pawn import Pawn, Horse, Monk, Tower, Queen, King

# Define some colors
GREY = (128, 128, 128)
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

# Create an 8x8 grid of cells


## position - [y,x]





def creating_figures(board):
    figures = []
    for y, line in enumerate(board):
        for x, figure  in enumerate(line):
            if figure == 'p':
                figures.append(Pawn(x, y, 'black', 'p'))
            elif figure == 'h':
                figures.append(Horse(x, y, 'black', 'h'))
            elif figure == 'm':
                figures.append(Monk(x, y, 'black', 'm'))
            elif figure == 't':
                figures.append(Tower(x, y, 'black', 't'))
            elif figure == 'q':
                figures.append(Queen(x, y, 'black', 'q'))
            elif figure == 'k':
                figures.append(King(x, y, 'black', 'k'))
            elif figure == 'P':
                figures.append(Pawn(x, y, 'white', 'P'))
            elif figure == 'H':
                figures.append(Horse(x, y, 'white', 'H'))
            elif figure == 'M':
                figures.append(Monk(x, y, 'white', 'M'))
            elif figure == 'T':
                figures.append(Tower(x, y, 'white', 'T'))
            elif figure == 'Q':
                figures.append(Queen(x, y, 'white', 'Q'))
            elif figure == 'K':
                figures.append(King(x, y, 'white', 'K'))

    return figures




def empty_grid(check):
    grid = []
    for row in range(8):
        grid.append([])
        for column in range(8):
            if row % 2 == 0:
                if column % 2 == 0:
                    color = WHITE
                else:
                    color = GREY
            else:
                if column % 2 == 0:
                    color = GREY
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


def draw_movable_positions(movable_positions, grid, board):
    for pos in movable_positions:
        if board[pos[0]][pos[1]] in 'hmtqkpHMTQKP':
            grid[pos[0]][pos[1]] = RED
        else:
            grid[pos[0]][pos[1]] = DARK_GREEN
    pass

def draw_picked_figure(figure_picked, grid):
    grid[figure_picked.pos_y][figure_picked.pos_x] = YELLOW

def get_figure(figures, mouse_pos, player):
    for figure in figures:
        if figure.object.x <= mouse_pos[0] and figure.object.x + WIDTH >= mouse_pos[0] and figure.object.y <= mouse_pos[1] and figure.object.y + HEIGHT >= mouse_pos[1]:
            if player == figure.color:
                return figure
            else:
                return None
    return None

def check_if_can_move_there(movable_positions, new_x_pos, new_y_pos):
    our_pos = [new_y_pos, new_x_pos]
    if our_pos in movable_positions:
        return True
    return False



def check_if_there_is_a_enemy_figure(figures, x_pos, y_pos, player_turn):
    for index, figure in enumerate(figures):
        if figure.pos_x == x_pos and figure.pos_y == y_pos:
            if player_turn != figure.color:
                del figures[index]
                return figures
    return figures


def check_if_king_will_be_under_attack(position, figure_picked, board, player_turn, figures):

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

def movable_positions_without_check(movable_positions, figure_picked, board, player, figures):
    new_movable_positions = []
    for position in movable_positions:
        if not check_if_king_will_be_under_attack(position, figure_picked, board, player, figures):
            new_movable_positions.append(position)

    return new_movable_positions

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


def check_if_no_more_moves(figures, player, board):
    for figure in figures:
        if figure.color == player:
            positions = figure.check_if_can_move(board)
            positions = movable_positions_without_check(positions, figure, board, player, figures)
            if positions != []:
                return False
    return True


def check_if_draw():
    pass

        



def main():
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
    figures = creating_figures(board)
    player_turn = 'white'
    enemy_turn = 'black'
    figure_picked = None
    movable_positions = None
    check = None
    grid  = empty_grid(check)

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
                        movable_positions = figure_picked.check_if_can_move(board)

                        movable_positions = movable_positions_without_check(movable_positions, figure_picked, board, player_turn, figures)

                        draw_movable_positions(movable_positions, grid, board)
                        draw_picked_figure(figure_picked, grid)



                elif figure_picked != None:

                    new_x_pos = (m_pos[0]//WIDTH)
                    new_y_pos = (m_pos[1]//HEIGHT)


                    if check_if_can_move_there(movable_positions, new_x_pos, new_y_pos):

                        board[figure_picked.pos_y][figure_picked.pos_x] = '0'   ## updating board position
                        board[new_y_pos][new_x_pos] = figure_picked.symbol
                        
 
                        figure_picked.object.x = 100*new_x_pos  ## updating sprite position
                        figure_picked.object.y = 100*new_y_pos
                        figure_picked.pos_x = new_x_pos     ## updating object position
                        figure_picked.pos_y = new_y_pos


                        figures = check_if_there_is_a_enemy_figure(figures, new_x_pos, new_y_pos, player_turn)

                        grid, check = check_if_check(board, player_turn, figures, grid, check)


                        if check != None:


                            if check_if_no_more_moves(figures, enemy_turn, board):
                                print(f'%s won' % player_turn)
                                main()
                        elif check == None:
                            if check_if_no_more_moves(figures, enemy_turn, board):
                                print('draw')
                                main()

                        for element in board:
                            print(element)




                        if player_turn == 'white':
                            player_turn = 'black'
                            enemy_turn = 'white'
                        elif player_turn == 'black':
                            player_turn = 'white'
                            enemy_turn = 'black'

                    
                    figure_picked = None

                    grid = empty_grid(check)




        draw_board(figures, grid)

        # --- Game logic should go here

        # --- Drawing code should go here

        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # --- Limit to 60 frames per second
        clock.tick(60)

    # Close the window and quit.
    pygame.quit()

if __name__ == '__main__':
    main()
