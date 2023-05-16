import pygame
import os

dir_path = os.path.dirname(os.path.abspath(__file__))

class Figure():
    def __init__(self, pos_x, pos_y, color, symbol) -> None:
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.color = color
        self.symbol = symbol

class Pawn(Figure):
    def __init__(self, pos_x, pos_y, color, symbol):
        super().__init__(pos_x, pos_y, color, symbol)
        self.image = pygame.image.load(os.path.join(dir_path, f'gfx/pawn_{self.color}.png'))
        self.object_image = pygame.transform.rotate(pygame.transform.scale(self.image, (80, 80)),0)
        self.object = pygame.Rect(pos_x*100, pos_y*100, 80, 80)

    def check_if_can_move(self, board):
        where_can_move = []
        try:
            if self.color == 'white':
                if board[self.pos_y - 1][self.pos_x] == '0':
                    where_can_move.append([self.pos_y - 1, self.pos_x])
                    if self.pos_y == 6 and board[self.pos_y - 2][self.pos_x] == '0':
                        where_can_move.append([self.pos_y - 2, self.pos_x])
                if board[self.pos_y - 1][self.pos_x + 1] in 'hmtqkp':
                    where_can_move.append([self.pos_y - 1, self.pos_x + 1])
                if board[self.pos_y - 1][self.pos_x - 1] in 'hmtqkp':
                    where_can_move.append([self.pos_y - 1, self.pos_x - 1])

            elif self.color == 'black':
                if board[self.pos_y + 1][self.pos_x] == '0':
                    where_can_move.append([self.pos_y + 1, self.pos_x])
                    if self.pos_y == 1 and board[self.pos_y + 2][self.pos_x] == '0':
                        where_can_move.append([self.pos_y + 2, self.pos_x])
                if board[self.pos_y + 1][self.pos_x + 1] in 'HMTQKP':
                    where_can_move.append([self.pos_y + 1, self.pos_x + 1])
                if board[self.pos_y + 1][self.pos_x - 1] in 'HMTQKP':
                    where_can_move.append([self.pos_y + 1, self.pos_x - 1])

        except:
            pass

        return where_can_move
        

class Knight(Figure):
    def __init__(self, pos_x, pos_y, color, symbol):
        super().__init__(pos_x, pos_y, color, symbol)
        self.image = pygame.image.load(os.path.join(dir_path, f'gfx/knight_{self.color}.png'))
        self.object_image = pygame.transform.rotate(pygame.transform.scale(self.image, (80, 80)),0)
        self.object = pygame.Rect(pos_x*100, pos_y*100, 80, 80)




    def check_if_occupied(self, symbols, board):
        where_can_move = []


        try:
            if self.pos_y - 2 >= 0 and self.pos_x + 1 < 8:
                if board[self.pos_y - 2][self.pos_x + 1] in symbols:
                    where_can_move.append([self.pos_y - 2, self.pos_x + 1])
            if self.pos_y - 2 >= 0 and self.pos_x - 1 >= 0:
                if board[self.pos_y - 2][self.pos_x - 1] in symbols:
                    where_can_move.append([self.pos_y - 2, self.pos_x - 1])
            if self.pos_y - 1 >= 0 and self.pos_x + 2 < 8:
                if board[self.pos_y - 1][self.pos_x + 2] in symbols:
                    where_can_move.append([self.pos_y - 1, self.pos_x + 2])
            if self.pos_y - 1 >= 0 and self.pos_x - 2 >= 0:
                if board[self.pos_y - 1][self.pos_x - 2] in symbols:
                    where_can_move.append([self.pos_y - 1, self.pos_x - 2])
            if self.pos_y + 1 < 8 and self.pos_x + 2 < 8:
                if board[self.pos_y + 1][self.pos_x + 2] in symbols:
                    where_can_move.append([self.pos_y + 1, self.pos_x + 2])
            if self.pos_y + 1 < 8 and self.pos_x - 2 >= 0:
                if board[self.pos_y + 1][self.pos_x - 2] in symbols:
                    where_can_move.append([self.pos_y + 1, self.pos_x - 2])
            if self.pos_y + 2 < 8 and self.pos_x + 1 < 8:
                if board[self.pos_y + 2][self.pos_x + 1] in symbols:
                    where_can_move.append([self.pos_y + 2, self.pos_x + 1])
            if self.pos_y + 2 < 8 and self.pos_x - 1 >= 0:
                if board[self.pos_y + 2][self.pos_x - 1] in symbols:
                    where_can_move.append([self.pos_y + 2, self.pos_x - 1])

        except:
            pass

        return where_can_move




    def check_if_can_move(self, board):
        where_can_move = []
        try:
            if self.color == 'white':
                symbols = 'hmtqkp0'
                where_can_move = self.check_if_occupied(symbols, board)

            elif self.color == 'black':
                symbols = 'HMTQKP0'
                where_can_move = self.check_if_occupied(symbols, board)

        except:
            pass

        return where_can_move

class Bishop(Figure):
    def __init__(self, pos_x, pos_y, color, symbol):
        super().__init__(pos_x, pos_y, color, symbol)
        self.image = pygame.image.load(os.path.join(dir_path, f'gfx/bishop_{self.color}.png'))
        self.object_image = pygame.transform.rotate(pygame.transform.scale(self.image, (80, 80)),0)
        self.object = pygame.Rect(pos_x*100, pos_y*100, 80, 80)

    def check_if_occupied(self, symbols_our, symbols_enemy, board):
        where_can_move = []


        x = 1
        y = 1
        while self.pos_x + x < 8 and self.pos_y + y < 8:
            if board[self.pos_y + y][self.pos_x + x] in symbols_our:
                break
            elif board[self.pos_y + y][self.pos_x + x] in symbols_enemy:
                where_can_move.append([self.pos_y + y, self.pos_x + x])
                break
            elif board[self.pos_y + y][self.pos_x + x] == '0':
                where_can_move.append([self.pos_y + y, self.pos_x + x])
            x += 1
            y += 1
        x = 1
        y = 1
        while self.pos_x + x < 8 and self.pos_y - y >= 0:
            if board[self.pos_y - y][self.pos_x + x] in symbols_our:
                break
            elif board[self.pos_y - y][self.pos_x + x] in symbols_enemy:
                where_can_move.append([self.pos_y - y, self.pos_x + x])
                break
            elif board[self.pos_y - y][self.pos_x + x] == '0':
                where_can_move.append([self.pos_y - y, self.pos_x + x])
            x += 1
            y += 1
        x = 1
        y = 1
        while self.pos_x - x >= 0 and self.pos_y + y < 8:
            if board[self.pos_y + y][self.pos_x - x] in symbols_our:
                break
            elif board[self.pos_y + y][self.pos_x - x] in symbols_enemy:
                where_can_move.append([self.pos_y + y, self.pos_x - x])
                break
            elif board[self.pos_y + y][self.pos_x - x] == '0':
                where_can_move.append([self.pos_y + y, self.pos_x - x])
            x += 1
            y += 1
        x = 1
        y = 1
        while self.pos_x - x >= 0 and self.pos_y - y >= 0:
            if board[self.pos_y - y][self.pos_x - x] in symbols_our:
                break
            elif board[self.pos_y - y][self.pos_x - x] in symbols_enemy:
                where_can_move.append([self.pos_y - y, self.pos_x - x])
                break
            elif board[self.pos_y - y][self.pos_x - x] == '0':
                where_can_move.append([self.pos_y - y, self.pos_x - x])
            x += 1
            y += 1


        return where_can_move
    

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

        except:
            pass

        return where_can_move

class Rook(Figure):
    def __init__(self, pos_x, pos_y, color, symbol):
        super().__init__(pos_x, pos_y, color, symbol)
        self.image = pygame.image.load(os.path.join(dir_path, f'gfx/rook_{self.color}.png'))
        self.object_image = pygame.transform.rotate(pygame.transform.scale(self.image, (80, 80)),0)
        self.object = pygame.Rect(pos_x*100, pos_y*100, 80, 80)
        self.castling = False

    def check_if_occupied(self, symbols_our, symbols_enemy, board):
        where_can_move = []


        x = 1
        while self.pos_x + x < 8:
            if board[self.pos_y][self.pos_x + x] in symbols_our:
                break
            elif board[self.pos_y][self.pos_x + x] in symbols_enemy:
                where_can_move.append([self.pos_y, self.pos_x + x])
                break
            elif board[self.pos_y][self.pos_x + x] == '0':
                where_can_move.append([self.pos_y, self.pos_x + x])
            x += 1

        x = 1
        while self.pos_x - x >= 0 :
            if board[self.pos_y][self.pos_x - x] in symbols_our:
                break
            elif board[self.pos_y][self.pos_x - x] in symbols_enemy:
                where_can_move.append([self.pos_y, self.pos_x - x])
                break
            elif board[self.pos_y][self.pos_x - x] == '0':
                where_can_move.append([self.pos_y, self.pos_x - x])
            x += 1

        y = 1
        while self.pos_y + y < 8:
            if board[self.pos_y + y][self.pos_x] in symbols_our:
                break
            elif board[self.pos_y + y][self.pos_x] in symbols_enemy:
                where_can_move.append([self.pos_y + y, self.pos_x])
                break
            elif board[self.pos_y + y][self.pos_x] == '0':
                where_can_move.append([self.pos_y + y, self.pos_x])
            y += 1

        y = 1
        while self.pos_y - y >= 0:
            if board[self.pos_y - y][self.pos_x] in symbols_our:
                break
            elif board[self.pos_y - y][self.pos_x] in symbols_enemy:
                where_can_move.append([self.pos_y - y, self.pos_x])
                break
            elif board[self.pos_y - y][self.pos_x] == '0':
                where_can_move.append([self.pos_y - y, self.pos_x])
            y += 1


        return where_can_move
    

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

        except:
            pass

        return where_can_move

class Queen(Figure):
    def __init__(self, pos_x, pos_y, color, symbol):
        super().__init__(pos_x, pos_y, color, symbol)
        self.image = pygame.image.load(os.path.join(dir_path, f'gfx/queen_{self.color}.png'))
        self.object_image = pygame.transform.rotate(pygame.transform.scale(self.image, (80, 80)),0)
        self.object = pygame.Rect(pos_x*100, pos_y*100, 80, 80)

    def check_if_occupied(self, symbols_our, symbols_enemy, board):
        where_can_move = []


        x = 1
        while self.pos_x + x < 8:
            if board[self.pos_y][self.pos_x + x] in symbols_our:
                break
            elif board[self.pos_y][self.pos_x + x] in symbols_enemy:
                where_can_move.append([self.pos_y, self.pos_x + x])
                break
            elif board[self.pos_y][self.pos_x + x] == '0':
                where_can_move.append([self.pos_y, self.pos_x + x])
            x += 1

        x = 1
        while self.pos_x - x >= 0 :
            if board[self.pos_y][self.pos_x - x] in symbols_our:
                break
            elif board[self.pos_y][self.pos_x - x] in symbols_enemy:
                where_can_move.append([self.pos_y, self.pos_x - x])
                break
            elif board[self.pos_y][self.pos_x - x] == '0':
                where_can_move.append([self.pos_y, self.pos_x - x])
            x += 1

        y = 1
        while self.pos_y + y < 8:
            if board[self.pos_y + y][self.pos_x] in symbols_our:
                break
            elif board[self.pos_y + y][self.pos_x] in symbols_enemy:
                where_can_move.append([self.pos_y + y, self.pos_x])
                break
            elif board[self.pos_y + y][self.pos_x] == '0':
                where_can_move.append([self.pos_y + y, self.pos_x])
            y += 1

        y = 1
        while self.pos_y - y >= 0:
            if board[self.pos_y - y][self.pos_x] in symbols_our:
                break
            elif board[self.pos_y - y][self.pos_x] in symbols_enemy:
                where_can_move.append([self.pos_y - y, self.pos_x])
                break
            elif board[self.pos_y - y][self.pos_x] == '0':
                where_can_move.append([self.pos_y - y, self.pos_x])
            y += 1

        x = 1
        y = 1
        while self.pos_x + x < 8 and self.pos_y + y < 8:
            if board[self.pos_y + y][self.pos_x + x] in symbols_our:
                break
            elif board[self.pos_y + y][self.pos_x + x] in symbols_enemy:
                where_can_move.append([self.pos_y + y, self.pos_x + x])
                break
            elif board[self.pos_y + y][self.pos_x + x] == '0':
                where_can_move.append([self.pos_y + y, self.pos_x + x])
            x += 1
            y += 1
        x = 1
        y = 1
        while self.pos_x + x < 8 and self.pos_y - y >= 0:
            if board[self.pos_y - y][self.pos_x + x] in symbols_our:
                break
            elif board[self.pos_y - y][self.pos_x + x] in symbols_enemy:
                where_can_move.append([self.pos_y - y, self.pos_x + x])
                break
            elif board[self.pos_y - y][self.pos_x + x] == '0':
                where_can_move.append([self.pos_y - y, self.pos_x + x])
            x += 1
            y += 1
        x = 1
        y = 1
        while self.pos_x - x >= 0 and self.pos_y + y < 8:
            if board[self.pos_y + y][self.pos_x - x] in symbols_our:
                break
            elif board[self.pos_y + y][self.pos_x - x] in symbols_enemy:
                where_can_move.append([self.pos_y + y, self.pos_x - x])
                break
            elif board[self.pos_y + y][self.pos_x - x] == '0':
                where_can_move.append([self.pos_y + y, self.pos_x - x])
            x += 1
            y += 1
        x = 1
        y = 1
        while self.pos_x - x >= 0 and self.pos_y - y >= 0:
            if board[self.pos_y - y][self.pos_x - x] in symbols_our:
                break
            elif board[self.pos_y - y][self.pos_x - x] in symbols_enemy:
                where_can_move.append([self.pos_y - y, self.pos_x - x])
                break
            elif board[self.pos_y - y][self.pos_x - x] == '0':
                where_can_move.append([self.pos_y - y, self.pos_x - x])
            x += 1
            y += 1


        return where_can_move
    

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

        except:
            pass

        return where_can_move

class King(Figure):
    def __init__(self, pos_x, pos_y, color, symbol):
        super().__init__(pos_x, pos_y, color, symbol)
        self.image = pygame.image.load(os.path.join(dir_path, f'gfx/king_{self.color}.png'))
        self.object_image = pygame.transform.rotate(pygame.transform.scale(self.image, (80, 80)),0)
        self.object = pygame.Rect(pos_x*100, pos_y*100, 80, 80)
        self.castling = False


    def check_if_occupied(self, symbols, board):
        where_can_move = []


        try:
            if self.pos_y - 1 >= 0:
                if board[self.pos_y - 1][self.pos_x] not in symbols:
                        where_can_move.append([self.pos_y - 1, self.pos_x])
            if self.pos_y + 1 < 8:
                if board[self.pos_y + 1][self.pos_x] not in symbols:
                        where_can_move.append([self.pos_y + 1, self.pos_x])
            if self.pos_x + 1 < 8:
                if board[self.pos_y][self.pos_x + 1] not in symbols:
                        where_can_move.append([self.pos_y, self.pos_x + 1])
            if self.pos_x - 1 >= 0:
                if board[self.pos_y][self.pos_x - 1] not in symbols:
                        where_can_move.append([self.pos_y, self.pos_x - 1])
            if self.pos_x - 1 >= 0 and self.pos_y + 1 < 8:
                if board[self.pos_y + 1][self.pos_x - 1] not in symbols:
                        where_can_move.append([self.pos_y + 1, self.pos_x - 1])
            if self.pos_x - 1 >= 0 and self.pos_y - 1 >= 0:
                if board[self.pos_y - 1][self.pos_x - 1] not in symbols:
                        where_can_move.append([self.pos_y - 1, self.pos_x - 1])
            if self.pos_x + 1 < 8 and self.pos_y + 1 < 8:
                if board[self.pos_y + 1][self.pos_x + 1] not in symbols:
                        where_can_move.append([self.pos_y + 1, self.pos_x + 1])
            if self.pos_x + 1 < 8 and self.pos_y - 1 >= 0:
                if board[self.pos_y - 1][self.pos_x + 1] not in symbols:
                        where_can_move.append([self.pos_y - 1, self.pos_x + 1])


            if self.castling == False:
                if board[self.pos_y][1] == '0' and board[self.pos_y][2] == '0' and board[self.pos_y][3] == '0':
                    where_can_move.append([self.pos_y, 1])
                if board[self.pos_y][5] == '0' and board[self.pos_y][6] == '0':
                    where_can_move.append([self.pos_y, 6])
            

        except:
            pass

        return where_can_move

    def check_if_can_move(self, board):
        where_can_move = []
        try:
            if self.color == 'white':
                symbols_our = 'HMTQKP'
                where_can_move = self.check_if_occupied(symbols_our, board)

            elif self.color == 'black':
                symbols_our = 'hmtqkp'
                where_can_move = self.check_if_occupied(symbols_our, board)

        except:
            pass

        return where_can_move
        