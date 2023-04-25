import pygame
import random
pygame.font.init()

WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Pathfinding')

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255, 0, 0)
BLUE = (0, 128, 255)
GREEN = (0, 128, 0)
PURPLE = (128, 0, 128)
ORANGE = (255,128,0)

MY_FONT = pygame.font.SysFont("monospace", 12)

FPS = 60

SPEED = 2 #higher the number, program is slower

ALL_COLORS = [] 

PIXEL_SIZE = 10

HIEIGHT_OF_PALLET = 200

ROWS = (HEIGHT - HIEIGHT_OF_PALLET)//PIXEL_SIZE
COLS = (WIDTH)//PIXEL_SIZE
BG_COLOR = (WHITE)

pallet_size = 50

BLACK_PROPABILITY = 35   #%


COLORS = [BLACK, WHITE, PURPLE]


class ColorBlock:
    def __init__(self,x,y,color):
        self.color = color
        self.pos_x = x
        self.pos_y = y
        self.color_block = pygame.Rect(self.pos_x, self.pos_y, pallet_size, pallet_size)

class Node:
    def __init__(self, position, current_cost, parent, estimate_distance):
        self.position = position
        self.current_cost = current_cost
        self.parent = parent
        self.estimate_distance = estimate_distance



def draw_window(all_colors, grid, erease_block, random_block, proper_way):


    screen.fill(WHITE)
    for colors in all_colors:
        pygame.draw.rect(screen, colors.color, colors.color_block)
        pygame.draw.rect(screen, BLACK, colors.color_block, 2)

    pygame.draw.rect(screen, BLACK, erease_block, 2)
    text_clear = MY_FONT.render('clear', 1, (0, 0, 0,))
    screen.blit(text_clear, (pallet_size + 7, (HEIGHT - HIEIGHT_OF_PALLET//2) + pallet_size//3))


    pygame.draw.rect(screen, BLACK, random_block, 2)
    text_random = MY_FONT.render('random', 1, (0, 0, 0,))
    screen.blit(text_random, (pallet_size*2.5 + 4, (HEIGHT - HIEIGHT_OF_PALLET//2) + pallet_size//3))
    
    for i, row in enumerate(grid):
        for j, pixel in enumerate(row):
            pygame.draw.rect(screen, pixel, (j*PIXEL_SIZE,i*PIXEL_SIZE,PIXEL_SIZE,PIXEL_SIZE))

    for i in range(ROWS+1):
         pygame.draw.line(screen, BLACK, (0,i*PIXEL_SIZE), (COLS * PIXEL_SIZE,i*PIXEL_SIZE), width=1)  ## if you want lines

    for i in range(COLS):
        pygame.draw.line(screen, BLACK, (i*PIXEL_SIZE,0), (i*PIXEL_SIZE,ROWS * PIXEL_SIZE), width=1)  ## if you want lines

    if proper_way == None:
        this_font = pygame.font.SysFont("arialblack", 25)
        text_clear = this_font.render('NO WAY TO GET TO THIS POINT', 1, (0, 0, 0,))                          
        screen.blit(text_clear, (WIDTH//3, (HEIGHT - HIEIGHT_OF_PALLET//2 - HIEIGHT_OF_PALLET//8)))


    pygame.display.update()



def init_grid(rows, cols, color):
    grid  = []
    for x in range(rows):
        grid.append([])
        for _ in range(cols):
            grid[x].append(color)
    return grid

def get_grid_pos(mouse_position):
    x,y = mouse_position
    row = x//PIXEL_SIZE
    col = y//PIXEL_SIZE
    return row, col

def change_color(mouse_position, drawing_color):
    x,y = mouse_position
    for colors in ALL_COLORS:
        if x >= colors.pos_x and x <= colors.pos_x + pallet_size and y >= colors.pos_y and y <= colors.pos_y + pallet_size:
            drawing_color = colors.color
    return drawing_color

def erase(grid, start_chosen, end_chosen):
    for j in range(ROWS):
        for i in range(COLS):
            grid[j][i] = WHITE
    start_chosen, end_chosen = False, False
    return grid, start_chosen, end_chosen

def random_labirynt(grid):
    for j in range(ROWS):
        for i in range(COLS):
            if random.randrange(100) >= BLACK_PROPABILITY:
                grid[j][i] = WHITE
            else:
                grid[j][i] = BLACK



    start_pos = random.randrange(COLS), random.randrange(ROWS)
    while True:
        end_pos = random.randrange(COLS), random.randrange(ROWS)
        if end_pos != start_pos: 
            grid[start_pos[1]][start_pos[0]] = ORANGE
            grid[end_pos[1]][end_pos[0]] = BLUE
            return grid, start_pos, end_pos


def insert(row, col, grid, start_chosen, end_chosen, drawing_color, start_pos, end_pos):
    if start_chosen == False:
        grid[col][row] = ORANGE
        start_pos = row, col
        start_chosen = True
    elif end_chosen == False:
        if grid[col][row] == ORANGE:
            pass
        else:
            grid[col][row] = BLUE
            end_pos = row, col
            end_chosen = True
    else:
        draw_pos = row, col
        if draw_pos != start_pos and draw_pos != end_pos:
            grid[col][row] = drawing_color
    return start_chosen, end_chosen, start_pos, end_pos, grid




def estimate_distance_f(point, end):
    x = abs(point[0] - end[0])
    y = abs(point[1] - end[1])
    return x + y 

def set_current_and_remove_from_open(Open):
    
    Current = Open[0]

    for pos in Open:
        if pos.current_cost + pos.estimate_distance < Current.current_cost + Current.estimate_distance:
            Current = pos

    for pos in Open:
        if pos.position == Current.position:
            Open.remove(pos)
            return Current

def check_neighbour(Current, grid):
    for_open_pos = []
    if Current.position[1]+1 < ROWS:
        if grid[Current.position[1]+1][Current.position[0]] != BLACK:    #below
            niegbour = Current.position[0], Current.position[1]+1
            for_open_pos.append(niegbour)

    if grid[Current.position[1]-1][Current.position[0]] != BLACK and Current.position[1]-1 >= 0:    #above
        niegbour = Current.position[0], Current.position[1]-1
        for_open_pos.append(niegbour)

    if Current.position[0]+1 < COLS:
        if grid[Current.position[1]][Current.position[0]+1] != BLACK:    #right
            niegbour = Current.position[0]+1, Current.position[1]
            for_open_pos.append(niegbour)

    if grid[Current.position[1]][Current.position[0]-1] != BLACK and Current.position[0]-1 >= 0:    #left
        niegbour = Current.position[0]-1, Current.position[1]
        for_open_pos.append(niegbour)

    return for_open_pos  


def check_cheaper_way(new_open, Open, Closed, grid):
    for node in Open:
        if new_open.position == node.position: 
            if new_open.current_cost < node.current_cost:
                Open.remove(node)
                Open.append(new_open)
            return Open, Closed, grid

    for node in Closed:
        if new_open.position == node.position:
            if new_open.current_cost < node.current_cost:
                node.parent == new_open.position
                Closed.remove(node)
                Open.append(new_open)
            return Open, Closed, grid

    
    Open.append(new_open)
    grid[new_open.position[1]][new_open.position[0]] = GREEN
    pygame.draw.rect(screen, grid[new_open.position[1]][new_open.position[0]], (new_open.position[0]*PIXEL_SIZE,new_open.position[1]*PIXEL_SIZE,PIXEL_SIZE,PIXEL_SIZE))

    return Open, Closed, grid




def find_a_way(start_pos, end_pos, grid):
    Open = [Node(start_pos, 0, 0, estimate_distance_f(start_pos,end_pos))]  #position, current cost, parent element, estimate cost
    Closed = []
    while True:
        if Open == []:
            return None, grid
        Current = set_current_and_remove_from_open(Open)
        Closed.append(Current)

        pygame.time.delay(SPEED) 
        
        if Current.position == end_pos:
            return Closed, grid

        else:
            new_open_pos = check_neighbour(Current, grid)
            
            for element in new_open_pos:
                new_open = Node(element, Current.current_cost+1, Current.position, estimate_distance_f(element, end_pos))

                Open, Closed, grid = check_cheaper_way(new_open, Open, Closed, grid)


        grid[Current.position[1]][Current.position[0]] = RED
        grid[start_pos[1]][start_pos[0]] = ORANGE
        pygame.draw.rect(screen, grid[Current.position[1]][Current.position[0]], (Current.position[0]*PIXEL_SIZE,Current.position[1]*PIXEL_SIZE,PIXEL_SIZE,PIXEL_SIZE))
        for i in range(ROWS):
         pygame.draw.line(screen, BLACK, (0,i*PIXEL_SIZE), (COLS * PIXEL_SIZE,i*PIXEL_SIZE), width=1)  ## if you want lines
        for i in range(COLS):
            pygame.draw.line(screen, BLACK, (i*PIXEL_SIZE,0), (i*PIXEL_SIZE,ROWS * PIXEL_SIZE), width=1)  ## if you want lines

        #for element in Closed:
            #text_cost = MY_FONT.render(str(element.current_cost + element.estimate_distance), 1, (0, 0, 0,))
            #screen.blit(text_cost, (element.position[0]*PIXEL_SIZE, element.position[1]*PIXEL_SIZE )) ## if you want cost
        #for element in Open:
            #text_cost = MY_FONT.render(str(element.current_cost + element.estimate_distance), 1, (0, 0, 0,))
            #screen.blit(text_cost, (element.position[0]*PIXEL_SIZE, element.position[1]*PIXEL_SIZE )) ## if you want cost  

        pygame.display.update()

def show_proper_way(proper_way, grid):
    end_element = proper_way[len(proper_way)-1]
    while True:
        for element in proper_way:
            if end_element.parent == element.position:
                grid[element.position[1]][element.position[0]] = PURPLE
                end_element = element
        if end_element.parent == 0:
            return grid

        

def start_movement(event, start_pos, grid):
    if event.key == pygame.K_d:
        if start_pos[0] + 1 < WIDTH//PIXEL_SIZE:
            if grid[start_pos[1]][start_pos[0] + 1] != BLACK:
                grid[start_pos[1]][start_pos[0]] = WHITE
                grid[start_pos[1]][start_pos[0] + 1] = ORANGE
                start_pos = start_pos[0] + 1,start_pos[1]
    elif event.key == pygame.K_a:
        if grid[start_pos[1]][start_pos[0]-1] != BLACK and start_pos[0] - 1 > 0:
            grid[start_pos[1]][start_pos[0]] = WHITE
            grid[start_pos[1]][start_pos[0]-1] = ORANGE
            start_pos = start_pos[0] - 1,start_pos[1]
    elif event.key == pygame.K_s:
        if start_pos[1] + 1 < HEIGHT//PIXEL_SIZE - HIEIGHT_OF_PALLET//PIXEL_SIZE:
            if grid[start_pos[1] + 1][start_pos[0]] != BLACK:
                grid[start_pos[1]][start_pos[0]] = WHITE
                grid[start_pos[1] + 1][start_pos[0]] = ORANGE
                start_pos = start_pos[0] ,start_pos[1] + 1
    elif event.key == pygame.K_w:
        if grid[start_pos[1] - 1][start_pos[0]] != BLACK and start_pos[1] > 0:
            grid[start_pos[1]][start_pos[0]] = WHITE
            grid[start_pos[1] - 1][start_pos[0]] = ORANGE
            start_pos = start_pos[0] ,start_pos[1] - 1

    return start_pos, grid
        


    
def main():

    x = pallet_size 
    y = HEIGHT - HIEIGHT_OF_PALLET//1.2
    for color in COLORS:
        ALL_COLORS.append(ColorBlock(x,y,color))
        x += pallet_size*1.5


    

    erease_block = pygame.Rect(pallet_size, HEIGHT - HIEIGHT_OF_PALLET//2, pallet_size, pallet_size)
    random_block = pygame.Rect(pallet_size * 2.5, HEIGHT - HIEIGHT_OF_PALLET//2, pallet_size, pallet_size)
    drawing_color = BLACK

    grid = init_grid(ROWS,COLS,BG_COLOR)

    start_chosen = False
    end_chosen = False

    start_pos = None
    end_pos = None

    proper_way = 'nothing for now'



    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            draw_window(ALL_COLORS, grid, erease_block, random_block, proper_way)

            if event.type == pygame.QUIT:
                run = False
            elif pygame.mouse.get_pressed()[0]:
                m_pos = pygame.mouse.get_pos()
                try:
                    row, col = get_grid_pos(m_pos)
                    drawing_color = change_color(m_pos, drawing_color)
                    x,y = m_pos
                    if x >= erease_block.x and x <= erease_block.x + pallet_size and y >= erease_block.y and y <= erease_block.y + pallet_size:
                        grid, start_chosen, end_chosen = erase(grid, start_chosen, end_chosen)
                        proper_way = 'nothing for now'
                    elif x >= random_block.x and x <= random_block.x + pallet_size and y >= random_block.y and y <= random_block.y + pallet_size:
                        grid, start_pos, end_pos = random_labirynt(grid)
                        start_chosen, end_chosen = True, True
                        proper_way = 'nothing for now'
                    start_chosen, end_chosen, start_pos, end_pos, grid = insert(row, col, grid, start_chosen, end_chosen, drawing_color, start_pos, end_pos)

                except IndexError:
                        pass
            elif event.type == pygame.KEYDOWN:
                if start_chosen == True and end_chosen == True:
                    if event.key == pygame.K_SPACE:
                        proper_way, grid = find_a_way(start_pos, end_pos, grid) 

                        if proper_way != None:
                            show_proper_way(proper_way, grid)
                            grid[end_pos[1]][end_pos[0]] = BLUE
                            grid[start_pos[1]][start_pos[0]] = ORANGE
                    else:
                        start_pos, grid = start_movement(event, start_pos, grid)

                    
    pygame.quit()

if __name__ == '__main__':
    main()