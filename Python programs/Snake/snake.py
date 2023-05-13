import pygame
import random
pygame.font.init()

WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Snake game')

GREEN = (0, 128, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

cell_size = 40

FPS = 8




class Fruit:
    def __init__(self):
        self.pos_x = random.randrange(1,HEIGHT/cell_size)
        self.pos_y = random.randrange(1,HEIGHT/cell_size)
        self.fruit_rect = pygame.Rect(self.pos_x * cell_size, self.pos_y * cell_size, cell_size, cell_size)


class Snake:
    def __init__(self):
        self.pos_x = HEIGHT/cell_size/2
        self.pos_y = WIDTH/cell_size/2
        self.length = [pygame.Rect(self.pos_x * cell_size, self.pos_y * cell_size, cell_size, cell_size)]
        self.direction = 'right'



def checks_if_collision(snake):
    for object in snake.length [1::1]:
        if object.x == snake.length[0].x and object.y == snake.length[0].y:
            pygame.time.delay(1000)
            main()
    if snake.pos_x == -1 or snake.pos_x == HEIGHT/cell_size or snake.pos_y == -1 or snake.pos_y == HEIGHT/cell_size:
        pygame.time.delay(1000)
        main()
        

def change_position(snake, fruit):
    finding = True
    while finding:
        fruit.pos_x = random.randrange(1,HEIGHT/cell_size)
        fruit.pos_y = random.randrange(1,HEIGHT/cell_size)
        finding = True in (object.x == fruit.pos_x * cell_size and object.y == fruit.pos_y * cell_size for object in snake.length) 

    fruit.fruit_rect.x = fruit.pos_x * cell_size
    fruit.fruit_rect.y = fruit.pos_y * cell_size

def check_if_increases(snake, fruit):
    if snake.pos_x == fruit.pos_x and snake.pos_y == fruit.pos_y:
        whitch = len(snake.length) - 1
        

        snake.length.append(pygame.Rect(snake.length[whitch].x * cell_size, snake.length[whitch].y * cell_size, cell_size, cell_size)) 
        change_position(snake, fruit)
 
def draw_window(fruit, snake, myfont):

    
    screen.fill(GREEN)
    pygame.draw.rect(screen, WHITE, fruit.fruit_rect)

    for objects in (range(len(snake.length) - 1)[::-1]):

        snake.length[objects + 1].x = snake.length[objects].x
        snake.length[objects + 1].y = snake.length[objects].y

    snake.length[0].x = snake.pos_x  * cell_size
    snake.length[0].y = snake.pos_y  * cell_size
    
    [pygame.draw.rect(screen, BLUE, object) for object in snake.length]
    pygame.draw.rect(screen, RED, snake.length[0])


    text = myfont.render("Score {0}".format(len(snake.length) - 1), 1, (0, 0, 0,))
    screen.blit(text, (5, 10))
    pygame.display.update()



def snake_direction(snake, Pause, myBiggerFont):

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_p:
                Pause = not Pause
                if Pause:
                    text = myBiggerFont.render("Game is Paused", 1, (0, 0, 0,))
                    screen.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
                    pygame.display.update()
            if not Pause:
                if event.key == pygame.K_a and snake.direction != 'right':
                    snake.direction = 'left'
                    snake_movement(snake)      
                    return Pause
                if event.key == pygame.K_d and snake.direction != 'left':
                    snake.direction = 'right'
                    snake_movement(snake)      
                    return Pause
                if event.key == pygame.K_s and snake.direction != 'up':
                    snake.direction = 'down'
                    snake_movement(snake)      
                    return Pause
                if event.key == pygame.K_w and snake.direction != 'down':
                    snake.direction = 'up'
                    snake_movement(snake)      
                    return Pause

    if not Pause:
        snake_movement(snake)
        
    return Pause

def snake_movement(snake):

    if snake.direction == 'right':
        snake.pos_x += 1
    if snake.direction == 'left':
        snake.pos_x -= 1
    if snake.direction == 'down':
        snake.pos_y += 1
    if snake.direction == 'up':
        snake.pos_y -= 1

def main():

    snake = Snake()

    fruit = Fruit()
    
    myfont = pygame.font.SysFont("monospace", 20)

    myBiggerFont = pygame.font.SysFont("monospace", 50)

    Pause = False
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        Pause = snake_direction(snake, Pause, myBiggerFont)
        if not Pause:
            check_if_increases(snake, fruit)
            checks_if_collision(snake)
            draw_window(fruit, snake, myfont)  
            

    pygame.quit()


if __name__ == '__main__':
    main()