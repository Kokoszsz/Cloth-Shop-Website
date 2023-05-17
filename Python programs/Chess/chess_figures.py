import pygame
import os

dir_path = os.path.dirname(os.path.abspath(__file__))

class Figure():
    def __init__(self, pos_x, pos_y, color, symbol) -> None:
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.color = color
        self.symbol = symbol

    def check_if_can_move(self, board):
        where_can_move = []
        try:
            if self.color == 'white':
                symbols_our = 'HMTQKP'
                symbols_enemy = 'hmtqkp'
                where_can_move = self.check_if_occupied(symbols_our, symbols_enemy, board)

            elif self.color == 'black':
                symbols_our = 'hmtqkp'
                symbols_enemy = 'HMTQKP'
                where_can_move = self.check_if_occupied(symbols_our, symbols_enemy, board)

        except IndexError:
            pass

        return where_can_move
    
    def check_with_directions(self, board, where_can_move, symbols_our, symbols_enemy, directions):
        try:
            for direction in directions:
                dx, dy = direction
                x, y = self.pos_x, self.pos_y

                while 0 <= x + dx < 8 and 0 <= y + dy < 8:
                    x += dx
                    y += dy

                    if board[y][x] in symbols_our:
                        break
                    elif board[y][x] in symbols_enemy:
                        where_can_move.append([y, x])
                        break
                    elif board[y][x] == '0':
                        where_can_move.append([y, x])

            return where_can_move
        except IndexError:
            pass
        return where_can_move

class Pawn(Figure):
    def __init__(self, pos_x, pos_y, color, symbol):
        super().__init__(pos_x, pos_y, color, symbol)
        self.image = pygame.image.load(os.path.join(dir_path, f'gfx/pawn_{self.color}.png'))
        self.object_image = pygame.transform.rotate(pygame.transform.scale(self.image, (80, 80)),0)
        self.figure_rect = pygame.Rect(pos_x*100, pos_y*100, 80, 80)

    def check_if_occupied(self, symbols_our, symbols_enemy, board):
        where_can_move = []
        try:
            if symbols_our == 'HMTQKP':
                if board[self.pos_y - 1][self.pos_x] == '0':
                    where_can_move.append([self.pos_y - 1, self.pos_x])
                    if self.pos_y == 6 and board[self.pos_y - 2][self.pos_x] == '0':
                        where_can_move.append([self.pos_y - 2, self.pos_x])
                if board[self.pos_y - 1][self.pos_x + 1] in symbols_enemy:
                    where_can_move.append([self.pos_y - 1, self.pos_x + 1])
                if board[self.pos_y - 1][self.pos_x - 1] in symbols_enemy:
                    where_can_move.append([self.pos_y - 1, self.pos_x - 1])

            elif symbols_our == 'hmtqkp':
                if board[self.pos_y + 1][self.pos_x] == '0':
                    where_can_move.append([self.pos_y + 1, self.pos_x])
                    if self.pos_y == 1 and board[self.pos_y + 2][self.pos_x] == '0':
                        where_can_move.append([self.pos_y + 2, self.pos_x])
                if board[self.pos_y + 1][self.pos_x + 1] in symbols_enemy:
                    where_can_move.append([self.pos_y + 1, self.pos_x + 1])
                if board[self.pos_y + 1][self.pos_x - 1] in symbols_enemy:
                    where_can_move.append([self.pos_y + 1, self.pos_x - 1])

        except IndexError:
            pass

        return where_can_move

        

class Knight(Figure):
    def __init__(self, pos_x, pos_y, color, symbol):
        super().__init__(pos_x, pos_y, color, symbol)
        self.image = pygame.image.load(os.path.join(dir_path, f'gfx/knight_{self.color}.png'))
        self.object_image = pygame.transform.rotate(pygame.transform.scale(self.image, (80, 80)),0)
        self.figure_rect = pygame.Rect(pos_x*100, pos_y*100, 80, 80)


    def check_if_occupied(self, symbols_our, symbols_enemy, board):
        where_can_move = []

        def add_move_if_valid(y, x):
            if 0 <= y < 8 and 0 <= x < 8 and board[y][x] not in symbols_our:
                where_can_move.append([y, x])

        try:
            add_move_if_valid(self.pos_y - 2, self.pos_x + 1)
            add_move_if_valid(self.pos_y - 2, self.pos_x - 1)
            add_move_if_valid(self.pos_y - 1, self.pos_x + 2)
            add_move_if_valid(self.pos_y - 1, self.pos_x - 2)
            add_move_if_valid(self.pos_y + 1, self.pos_x + 2)
            add_move_if_valid(self.pos_y + 1, self.pos_x - 2)
            add_move_if_valid(self.pos_y + 2, self.pos_x + 1)
            add_move_if_valid(self.pos_y + 2, self.pos_x - 1)

        except IndexError:
            pass

        return where_can_move


class Bishop(Figure):
    def __init__(self, pos_x, pos_y, color, symbol):
        super().__init__(pos_x, pos_y, color, symbol)
        self.image = pygame.image.load(os.path.join(dir_path, f'gfx/bishop_{self.color}.png'))
        self.object_image = pygame.transform.rotate(pygame.transform.scale(self.image, (80, 80)),0)
        self.figure_rect = pygame.Rect(pos_x*100, pos_y*100, 80, 80)

    def check_if_occupied(self, symbols_our, symbols_enemy, board):
        where_can_move = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        where_can_move =  self.check_with_directions(board, where_can_move, symbols_our, symbols_enemy, directions)
        return where_can_move


class Rook(Figure):
    def __init__(self, pos_x, pos_y, color, symbol):
        super().__init__(pos_x, pos_y, color, symbol)
        self.image = pygame.image.load(os.path.join(dir_path, f'gfx/rook_{self.color}.png'))
        self.object_image = pygame.transform.rotate(pygame.transform.scale(self.image, (80, 80)),0)
        self.figure_rect = pygame.Rect(pos_x*100, pos_y*100, 80, 80)
        self.castling = False

    def check_if_occupied(self, symbols_our, symbols_enemy, board):
        where_can_move = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        where_can_move =  self.check_with_directions(board, where_can_move, symbols_our, symbols_enemy, directions)
        return where_can_move


class Queen(Figure):
    def __init__(self, pos_x, pos_y, color, symbol):
        super().__init__(pos_x, pos_y, color, symbol)
        self.image = pygame.image.load(os.path.join(dir_path, f'gfx/queen_{self.color}.png'))
        self.object_image = pygame.transform.rotate(pygame.transform.scale(self.image, (80, 80)),0)
        self.figure_rect = pygame.Rect(pos_x*100, pos_y*100, 80, 80)

    def check_if_occupied(self, symbols_our, symbols_enemy, board):
        where_can_move = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        where_can_move =  self.check_with_directions(board, where_can_move, symbols_our, symbols_enemy, directions)
        return where_can_move
    

class King(Figure):
    def __init__(self, pos_x, pos_y, color, symbol):
        super().__init__(pos_x, pos_y, color, symbol)
        self.image = pygame.image.load(os.path.join(dir_path, f'gfx/king_{self.color}.png'))
        self.object_image = pygame.transform.rotate(pygame.transform.scale(self.image, (80, 80)),0)
        self.figure_rect = pygame.Rect(pos_x*100, pos_y*100, 80, 80)
        self.castling = False


    def check_if_occupied(self, symbols_our, symbols_enemy, board):
        where_can_move = []


        def add_move_if_valid(y, x):
            if 0 <= y < 8 and 0 <= x < 8 and board[y][x] not in symbols_our:
                where_can_move.append([y, x])

        try:
            add_move_if_valid(self.pos_y - 1, self.pos_x)
            add_move_if_valid(self.pos_y + 1, self.pos_x)
            add_move_if_valid(self.pos_y, self.pos_x + 1)
            add_move_if_valid(self.pos_y, self.pos_x - 1)
            add_move_if_valid(self.pos_y + 1, self.pos_x - 1)
            add_move_if_valid(self.pos_y - 1, self.pos_x - 1)
            add_move_if_valid(self.pos_y + 1, self.pos_x + 1)
            add_move_if_valid(self.pos_y - 1, self.pos_x + 1)



            if self.castling == False:
                if board[self.pos_y][1] == '0' and board[self.pos_y][2] == '0' and board[self.pos_y][3] == '0':
                    where_can_move.append([self.pos_y, 1])
                if board[self.pos_y][5] == '0' and board[self.pos_y][6] == '0':
                    where_can_move.append([self.pos_y, 6])
            

        except IndexError:
            pass

        return where_can_move
        