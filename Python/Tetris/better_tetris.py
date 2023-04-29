import pygame
import copy
import random
from dataclasses import dataclass
import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
pygame.font.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Tetris')

BLACK = (0,0,0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
GOLD = ( 255,215,0)
SADDLE_BROWN = (139,69,19)
AQUA = (0,255,255)
SPRING_GREEN = (0,255,127)

RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)

CELL_SIZE = 19


rows, collumns = HEIGHT//(CELL_SIZE+1), WIDTH//((CELL_SIZE+1)*2)

SPEED = 200

OBJECTS = ['straight', 'square', 'reverse_zigzag', 'zigzag', 'jocker', 'reverse_jocker', 'tee' ]

ALL_OBJECTS = []



START_X = WIDTH*(3/4) + 1
START_Y = HEIGHT*(2/3) + 1




class Object:  
    """A class representing all objects in the game.
    
    Attributes:
    - type: A string representing the type of object (e.g. "straight", "square", "reverse_zigzag", etc.)
    - position_x: An integer representing the x position of the object in the game.
    - position_y: An integer representing the y position of the object in the game.
    - color: A tuple representing the RGB color of the object.
    - shape: An instance of the Shape class representing the shape of the object.
    - body: A list of four pygame.Rect objects representing the cells occupied by the object.
    
    Methods:
    - __init__(self, type): Initializes a new instance of the Object class with the specified type.
    - check_if_can_rotate(self, new_pos_x, new_pos_y): Checks if the object can be rotated to a new position.
    - rotate(self): Rotates the object.
    """
    def __init__(self, type) -> None:
        self.type = type
        self.position_x, self.position_y = START_X, START_Y

        # Define dictionary to store object properties
        properties = {
            'straight': {'color': AQUA, 'shape': Shape(one=[1,0], two=[2,0], three=[-1,0]), 'pos_x': -CELL_SIZE - 1},
            'square': {'color': ORANGE, 'shape': Shape(one=[1,0], two=[1,-1], three=[0,-1]), 'pos_x': -CELL_SIZE - 1},
            'reverse_zigzag': {'color': PURPLE, 'shape': Shape(one=[0,-1], two=[-1,0], three=[-1,1]), 'pos_x': 0},
            'zigzag': {'color': GOLD, 'shape': Shape(one=[0,-1], two=[1,0], three=[1,1]), 'pos_x': -CELL_SIZE - 1},
            'jocker': {'color': SADDLE_BROWN, 'shape': Shape(one=[0,1], two=[-1,1], three=[0,-1]), 'pos_x': 0},
            'reverse_jocker': {'color': SPRING_GREEN, 'shape': Shape(one=[0,1], two=[1,1], three=[0,-1]), 'pos_x': -CELL_SIZE - 1},
            'tee': {'color': BLUE, 'shape': Shape(one=[1,0], two=[0,-1], three=[-1,0]), 'pos_x': 0}
        }

        # Look up object properties from dictionary
        object_properties = properties[type]
        self.color = object_properties['color']
        self.shape = object_properties['shape']
        self.position_x += object_properties['pos_x']

        # Create object body
        self.body = [
            pygame.Rect(self.position_x, self.position_y, CELL_SIZE, CELL_SIZE),
            pygame.Rect(self.position_x + self.shape.one[0]*CELL_SIZE + self.shape.one[0],
                        self.position_y + self.shape.one[1]*CELL_SIZE + self.shape.one[1], CELL_SIZE, CELL_SIZE),
            pygame.Rect(self.position_x + self.shape.two[0]*CELL_SIZE + self.shape.two[0],
                        self.position_y + self.shape.two[1]*CELL_SIZE + self.shape.two[1], CELL_SIZE, CELL_SIZE),
            pygame.Rect(self.position_x + self.shape.three[0]*CELL_SIZE + self.shape.three[0],
                        self.position_y + self.shape.three[1]*CELL_SIZE + self.shape.three[1], CELL_SIZE, CELL_SIZE)
        ]




    def check_if_can_rotate(self, new_pos_x, new_pos_y):

        if pygame.Rect(new_pos_x, new_pos_y, 19, 19) in ALL_OBJECTS:  ## checks if cell is already occupied by red one, if yes then do not rotate
            return False
        if new_pos_x > WIDTH//2 or new_pos_x < 0:               ## checks if is near edge (left, right)
            return False
        if new_pos_y > HEIGHT:                                 ## checks if is near edge (upper)
            return False
        return True                                              




    def rotate(self):  ## function that rotates an object
        if self.type != 'square':
            save_pos = copy.deepcopy(self.body)
            for cell in self.body[1:4]:


                if cell.x > self.body[0].x:
                    if cell.y == self.body[0].y:

                        if not self.check_if_can_rotate(self.body[0].x, self.body[0].y + (cell.x - self.body[0].x)):
                            self.body = save_pos
                            return
                        
                        cell.y = self.body[0].y + (cell.x - self.body[0].x)
                        cell.x = self.body[0].x

                    elif cell.y < self.body[0].y:
                        current_x = cell.x
                        if not self.check_if_can_rotate(self.body[0].x - (cell.y - self.body[0].y), self.body[0].y + (current_x - self.body[0].x)):
                            self.body = save_pos
                            return

                        cell.x = self.body[0].x - (cell.y - self.body[0].y)
                        cell.y = self.body[0].y + (current_x - self.body[0].x)

                    elif cell.y > self.body[0].y:
                        current_x = cell.x
                        if not self.check_if_can_rotate(self.body[0].x - (cell.y - self.body[0].y), self.body[0].y + (current_x - self.body[0].x)):
                            self.body = save_pos
                            return

                        cell.x = self.body[0].x - (cell.y - self.body[0].y)
                        cell.y = self.body[0].y + (current_x - self.body[0].x)


                elif cell.x < self.body[0].x:
                    if cell.y == self.body[0].y:
                        if not self.check_if_can_rotate(self.body[0].x, self.body[0].y + (cell.x - self.body[0].x)):
                            self.body = save_pos
                            return

                        cell.y = self.body[0].y + (cell.x - self.body[0].x)
                        cell.x = self.body[0].x


                    elif cell.y < self.body[0].y:
                        current_x = cell.x
                        if not self.check_if_can_rotate(self.body[0].x - (cell.y - self.body[0].y), self.body[0].y + (current_x - self.body[0].x)):
                            self.body = save_pos
                            return

                        cell.x = self.body[0].x - (cell.y - self.body[0].y)
                        cell.y = self.body[0].y + (current_x - self.body[0].x)


                    elif cell.y > self.body[0].y:
                        current_x = cell.x
                        if not self.check_if_can_rotate(self.body[0].x - (cell.y - self.body[0].y), self.body[0].y + (current_x - self.body[0].x)):
                            self.body = save_pos
                            return

                        cell.x = self.body[0].x - (cell.y - self.body[0].y)
                        cell.y = self.body[0].y + (current_x - self.body[0].x)

                elif cell.x == self.body[0].x:

                    if cell.y < self.body[0].y:

                        if not self.check_if_can_rotate(self.body[0].x - (cell.y - self.body[0].y), self.body[0].y):

                            self.body = save_pos
                            return

                        cell.x = self.body[0].x - (cell.y - self.body[0].y)
                        cell.y = self.body[0].y


                    elif cell.y > self.body[0].y:
                        if not self.check_if_can_rotate(self.body[0].x - (cell.y - self.body[0].y),self.body[0].y):
                            self.body = save_pos
                            return

                        cell.x = self.body[0].x - (cell.y - self.body[0].y)
                        cell.y = self.body[0].y



@dataclass
class Shape:
    zero = 0, 0
    one: list[int]
    two: list[int]
    three: list[int]


def grid():
    
    x = 0
    y = 0
    for l in range(collumns):
        x += (CELL_SIZE+1)
        pygame.draw.line(screen, (WHITE), (x,0), (x,HEIGHT))
    for l in range(rows):
        y += (CELL_SIZE+1)
        pygame.draw.line(screen, (WHITE), (0,y), (WIDTH/2,y))

def draw_board(object, second_object, third_object, myfont, POINTS):
    screen.fill(BLACK)
    grid()

    [pygame.draw.rect(screen, object.color, cell) for cell in object.body]
    [pygame.draw.rect(screen, second_object.color, cell) for cell in second_object.body]
    [pygame.draw.rect(screen, third_object.color, cell) for cell in third_object.body]
    [pygame.draw.rect(screen, RED, cell) for cell in ALL_OBJECTS]

    text = myfont.render("Score {0}".format(POINTS), 1, (WHITE))
    screen.blit(text, (WIDTH - text.get_width() - 10, 10))
        

    pygame.display.update()

def draw_object():
    which_object = random.choice(OBJECTS)
    return Object(which_object)



def check_if_score(object, second_object, third_object, myfont, POINTS, VELOCITY):
    for yy in range(HEIGHT//(CELL_SIZE+1) - 1,1,-1):
            if all(screen.get_at((x*(CELL_SIZE+1)+1,(yy)*(CELL_SIZE+1)+1)) == RED  for x in range((WIDTH//2)//(CELL_SIZE+1))):
                for cell in ALL_OBJECTS[0::1]:

                    if cell.y == yy*(CELL_SIZE+1) + 1:
                        ALL_OBJECTS.remove(cell)
                for cell in ALL_OBJECTS[0::1]:
                    if cell.y < yy*(CELL_SIZE+1):
                        cell.y += (CELL_SIZE+1)
                draw_board(object, second_object, third_object, myfont, POINTS)

                if VELOCITY < SPEED:
                    VELOCITY += 1
                POINTS += 1
    return pygame.time.get_ticks() - VELOCITY, VELOCITY, POINTS
                

def check_if_lose(myBiggerFont):
    for cell in ALL_OBJECTS:
        if cell.y <= CELL_SIZE:
            text = myBiggerFont.render("YOU LOST", 1, (GREEN))
            screen.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(5000)
            main()
    



def move_down(object, second_object, third_object):
    if all(cell.y < HEIGHT - (CELL_SIZE + 1) for cell in object.body) and all(RED != screen.get_at((cell.x, cell.y + (CELL_SIZE + 1))) for cell in object.body): 
        for cell in object.body:
            cell.y += (CELL_SIZE + 1)
            
            
        return object, second_object, third_object
    else:
        [ALL_OBJECTS.append(cell) for cell in object.body]
        object = second_object
        for cell in object.body:
            cell.x -= WIDTH//2
            cell.y -= HEIGHT//6
            cell.y += (CELL_SIZE + 1)
        second_object = third_object
        for cell in second_object.body:
            cell.y -= HEIGHT//2
        third_object = draw_object()
        return object, second_object, third_object

def move_left(object):
    if all(cell.x > 1 for cell in object.body) and all(RED != screen.get_at((cell.x - CELL_SIZE, cell.y)) for cell in object.body):    ## if there is red not move
        for cell in object.body:
            cell.x -= (CELL_SIZE + 1)
def move_right(object):
    if all(cell.x < WIDTH//2 - CELL_SIZE for cell in object.body) and all(RED != screen.get_at((cell.x + 2*CELL_SIZE, cell.y)) for cell in object.body):  ## if there is red not move
        for cell in object.body:
            cell.x += (CELL_SIZE + 1)


def move_whole_down(object):
    while all(cell.y < HEIGHT - 2 * CELL_SIZE for cell in object.body) and all(RED != screen.get_at((cell.x, cell.y + 2 * CELL_SIZE)) for cell in object.body):
        for cell in object.body:
            cell.y += CELL_SIZE + 1
            

def tetris_events(object, Pause, myBiggerFont):

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                Pause = not Pause
                if Pause:
                    text = myBiggerFont.render("Game is Paused", 1, (GREEN))
                    screen.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
                    pygame.display.update()
            if event.key == pygame.K_d:
                move_right(object) 
            if event.key == pygame.K_a:
                move_left(object)    
            if event.key == pygame.K_s:
                object.rotate()   
            if event.key == pygame.K_SPACE:
                move_whole_down(object)
            if event.key == pygame.K_r:
                main()

    return Pause    



        

def main():
    global ALL_OBJECTS
    ALL_OBJECTS = []

    FPS = 60
    object = draw_object()
    second_object = draw_object()
    third_object = draw_object()
    for cell in object.body:
        cell.x -= WIDTH//2
        cell.y -= HEIGHT//1.5
    for cell in second_object.body:
        cell.y -= HEIGHT//2
    second_object.position_y -= HEIGHT//2


    VELOCITY = 0

    myBiggerFont = pygame.font.SysFont("freesanbold.ttf", 60)

    myfont = pygame.font.SysFont("monospace", 20)

    POINTS = 0

    Pause = False


    start_time = pygame.time.get_ticks() - VELOCITY
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        Pause = tetris_events(object, Pause, myBiggerFont)
        if Pause == False:
            draw_board(object, second_object, third_object, myfont, POINTS)
            if pygame.time.get_ticks() - start_time > SPEED:
                start_time, VELOCITY, POINTS = check_if_score(object, second_object, third_object, myfont, POINTS, VELOCITY)
                check_if_lose(myBiggerFont)
                object, second_object, third_object = move_down(object, second_object, third_object)

            

    pygame.quit()


if __name__ == '__main__':
    main()