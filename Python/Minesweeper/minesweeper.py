from tkinter import *
import random



WIDTH = 1240
HEIGHT = 700

SMALL = 20 # grid
MEDIUM = 30 # grid
LARGE = 40 # grid

GRID_SIZE = None

DIFFICULTY = None

NUMBER_OF_MINES = None

EASY = 10
MEDIUM_LEVEL = 9
HARD = 8

root = Tk()
root.configure(bg="black")
root.geometry(f'{WIDTH}x{HEIGHT}')
root.title('MinseSweeping')
root.resizable(False,False)

option_frame = Frame(root, bg="white", width=WIDTH//3, height=HEIGHT//3)
option_frame.place(x=WIDTH/2-WIDTH//6,y=HEIGHT/2-HEIGHT//6)

option_text = Label(option_frame, text="Game size", height=2, width=WIDTH//3, font = ("Arial", 24), bg="white", anchor=W)
option_text.place(relx=0.3, rely=0)

def height_prct(percentage):
    return HEIGHT//100 * percentage
def width_prct(percentage):
    return WIDTH//100 * percentage



def init_small():
    global GRID_SIZE
    GRID_SIZE = SMALL
    Cell.cell_left = GRID_SIZE*(GRID_SIZE//2)
    configure_difficulty_level()

def init_medium():
    global GRID_SIZE
    GRID_SIZE = MEDIUM
    Cell.cell_left = GRID_SIZE*(GRID_SIZE//2)
    configure_difficulty_level()


def init_large():
    global GRID_SIZE
    GRID_SIZE = LARGE
    Cell.cell_left = GRID_SIZE*(GRID_SIZE//2)
    configure_difficulty_level()

def init_easy():
    global DIFFICULTY
    DIFFICULTY = EASY
    Cell.mines_left = DIFFICULTY
    Cell.initialize()

def init_medium_level():
    global DIFFICULTY
    DIFFICULTY = MEDIUM_LEVEL
    Cell.mines_left = DIFFICULTY
    Cell.initialize()


def init_hard():
    global DIFFICULTY
    DIFFICULTY = HARD
    Cell.mines_left = DIFFICULTY
    Cell.initialize()



small_button = Button(option_frame, text='Small', height=2, width=WIDTH//100, command = init_small)
small_button.place(relx=0.4, rely=0.3)

medium_button = Button(option_frame, text='Medium', height=2, width=WIDTH//100, command = init_medium)
medium_button.place(relx=0.4, rely=0.5)

large_button = Button(option_frame, text='Large', height=2, width=WIDTH//100, command = init_large)
large_button.place(relx=0.4, rely=0.7)


top_frame = Frame(root, bg="black", width=WIDTH, height=height_prct(15))

left_frame = Frame(root, bg="black", width=width_prct(25), height=height_prct(75))

center_frame = Frame(root, bg="white", width=width_prct(80), height=height_prct(70))





def configure_difficulty_level():

    option_text.configure(text = "Game difficulty")

    small_button.configure(text = "Easy", command=init_easy)

    medium_button.configure(text = "Medium", command=init_medium_level)

    large_button.configure(text = "Hard", command=init_hard)











class Cell():
    mines_left = None
    cell_left = None
    all = []
    def __init__(self, x, y, is_mine = False):
        self.is_mine = is_mine
        self.cell_btn_object = None
        self.x = x
        self.y = y
        self.neighbour = []

        Cell.all.append(self)

    def create_button(self, location):
        btn = Button(location, text='', height=(HEIGHT//24)//GRID_SIZE, width=(WIDTH//24)//GRID_SIZE)

        btn.bind('<Button-1>', self.left_click_action)
        btn.bind('<Button-3>', self.right_click_action)

        self.cell_btn_object = btn

    def number_of_bombs_arround(self):
        mines = 0
        for neighbour in self.neighbour:
            if neighbour.is_mine == True:
                mines += 1
        return str(mines)

    def left_click_action(self, event):
        if self.is_mine == False:

            if self.cell_btn_object['text'] == '':
                Cell.cell_left -= 1

            self.cell_btn_object['text'] = self.number_of_bombs_arround()
            
            Cell.edit_cells_left()
            if self.number_of_bombs_arround() == str(0):
                for cell in self.neighbour:
                    cell.check_if_neighbour_is_0()

            for cell in Cell.all:
                if cell.cell_btn_object['text'] == "":
                    return
            print("you won")
            Cell.reset()




        elif self.is_mine == True:
            print("you lost")
            Cell.reset()

            
    def check_if_neighbour_is_0(self):
        if self.is_mine == False:
            if self.cell_btn_object['text'] == "" or self.cell_btn_object['text'] == "X":
                self.cell_btn_object['text'] = self.number_of_bombs_arround()
                Cell.cell_left -= 1
                Cell.edit_cells_left()
                if self.number_of_bombs_arround() == str(0):
                    for cell in self.neighbour:
                        if cell.cell_btn_object['text'] != "0":
                            cell.check_if_neighbour_is_0()

    def right_click_action(self, event):
        if self.cell_btn_object['text'] == "":
            self.cell_btn_object['text'] = "X"
            Cell.mines_left -= 1
            if Cell.mines_left >= 0:
                Cell.edit_count_mines()
        elif self.cell_btn_object['text'] == "X":
            self.cell_btn_object['text'] = ""
            Cell.mines_left += 1
            if Cell.mines_left >= 0:
                Cell.edit_count_mines()


    @staticmethod

    def initialize():

        option_frame.destroy()
        small_button.destroy()
        medium_button.destroy()
        large_button.destroy()

        global NUMBER_OF_MINES
        NUMBER_OF_MINES = (GRID_SIZE*GRID_SIZE)//DIFFICULTY
        

        top_frame.place(x=0,y=0)

        left_frame.place(x=0,y=height_prct(25))

        center_frame.place(x=width_prct(25),y=height_prct(15))




        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE//2):
                c = Cell(x, y)
                c.create_button(center_frame)
                c.cell_btn_object.grid(column=x, row=y)

        Cell.find_neighbour()

        Cell.randomize_mines()

        Cell.create_count_mines()

        Cell.creat_cells_left()



    def randomize_mines():
        picked_cells = random.sample(Cell.all, NUMBER_OF_MINES)
        for cell in picked_cells:
            cell.is_mine = True

    def find_neighbour():
        for this_cell in Cell.all:
            for cell in Cell.all:
                if this_cell.x + 1 == cell.x and this_cell.y == cell.y: 
                    this_cell.neighbour.append(cell)
                elif this_cell.x - 1 == cell.x and this_cell.y == cell.y: 
                    this_cell.neighbour.append(cell)

                elif this_cell.y + 1 == cell.y and this_cell.x == cell.x: 
                    this_cell.neighbour.append(cell)

                elif this_cell.y - 1 == cell.y and this_cell.x == cell.x: 
                    this_cell.neighbour.append(cell)

                elif this_cell.x + 1 == cell.x and this_cell.y + 1 == cell.y : 
                    this_cell.neighbour.append(cell)

                elif this_cell.x + 1 == cell.x and this_cell.y - 1 == cell.y : 
                    this_cell.neighbour.append(cell)

                elif this_cell.x - 1 == cell.x and this_cell.y + 1 == cell.y : 
                    this_cell.neighbour.append(cell)

                elif this_cell.x - 1 == cell.x and this_cell.y - 1 == cell.y : 
                    this_cell.neighbour.append(cell)

    def reset():
        for cell in Cell.all:
            cell.cell_btn_object['text'] = ""
            cell.is_mine = False
        Cell.mines_left = NUMBER_OF_MINES
        Cell.cell_left = GRID_SIZE*(GRID_SIZE//2)
        Cell.randomize_mines()
        Cell.edit_cells_left()
        Cell.edit_count_mines()

    def create_count_mines():
        Cell.mines_left_text = Label(left_frame, text=f"Mines count:{NUMBER_OF_MINES}", height=4, width=44, font = ("Arial", 16), bg="black", anchor=W, fg="white")
        Cell.mines_left_text.place(relx=0.25, rely=0.3)

    def edit_count_mines():
        Cell.mines_left_text['text'] = f"Mines count:{Cell.mines_left}"

    def creat_cells_left():
        Cell.cell_left_text = Label(left_frame, text=f"Cells left:{Cell.cell_left}", height=1, width=44, font = ("Arial", 24), bg="black", anchor=W, fg="white")
        Cell.cell_left_text.place(relx=0.2, rely=0)

    def edit_cells_left():
        Cell.cell_left_text['text'] = f"Cells left:{Cell.cell_left}"









root.mainloop()