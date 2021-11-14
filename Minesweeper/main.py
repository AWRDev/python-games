from enum import Enum
import sys
import random
import time
import pygame

import pprint as pp

WINDOW_SIZE = (600, 600)
FIELD_SIZE = (30, 30)

pygame.init()
pygame.display.set_caption('Minesweeper')
pygame.font.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()

class Grid:
    def __init__(self) -> None:
        self.bg_color = (55,55,55)
        self.cells : list[list[Cell]]= []
        self.opened_cells = set()
        self.extended_cells = set()
        self.flagged_cells = set()
        self.__init_cells()
    def __init_cells(self):
        '''
        Prepares all cells
        '''
        self.__place_cells()
        self.__place_bombs()
        self.__create_marks()
    def __check_neighbours(self, x, y):
        result = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                try:
                    if self.cells[x+i][y+j].role == Cell.Role.Mine:
                        result += 1
                except Exception as e:
                    print(str(e))
        return result
    def __create_marks(self):
        for i in range(0,FIELD_SIZE[0]):
            for j in range(0, FIELD_SIZE[1]):
                neighbours_number = self.__check_neighbours(i,j)
                if (i,j) not in self.points and neighbours_number > 0:
                    self.cells[i][j].role = Cell.Role.Number
                    self.cells[i][j].set_number(neighbours_number)
                    self.cells[i][j].update()
    def __place_cells(self):
        for i in range(FIELD_SIZE[0]):
            row = []
            for j in range(FIELD_SIZE[1]):
                row.append(Cell(i, j, Cell.Role.Empty))
            self.cells.append(row)
        
    def __place_bombs(self):
        self.points = gen_random_points(25)
        print(self.points)
        for point in self.points:
            self.cells[point[0]][point[1]] = Cell(point[0], point[1], Cell.Role.Mine)
    def extend_open_area(self, x, y):
        # print(f"Extending {x}, {y}")
        if (x,y) in self.extended_cells:
            # print("Already extended, skipping..")
            return
        self.extended_cells.add((x,y))
        for i in range(-1, 2):
            for j in range(-1, 2):
                try:
                    self.open_cell(x+i, y+j)
                    #self.opened_cells.add((x+i,y+i))
                except Exception as e:
                    break
    def draw(self, screen):
        pixel_side = WINDOW_SIZE[0]//FIELD_SIZE[0]
        screen.fill(self.bg_color)
        for i in range(FIELD_SIZE[0]):
            for j in range(FIELD_SIZE[1]):
                self.cells[i][j].draw(screen)
        for i in range(FIELD_SIZE[0]):
            pygame.draw.line(screen, (255, 255, 255), (i*pixel_side,0), (i*pixel_side, WINDOW_SIZE[0]))
            pygame.draw.line(screen, (255, 255, 255), (0, i*pixel_side), (WINDOW_SIZE[1], i*pixel_side))
    def open_cell(self, cell_x, cell_y):
        # print(cell_x, cell_y)
        self.cells[cell_x][cell_y].open()
        #self.draw(screen)
        #pygame.display.flip()
        if cell_x in range(1,FIELD_SIZE[0]) and cell_y in range(1,FIELD_SIZE[1])  and self.cells[cell_x][cell_y].role == Cell.Role.Empty:
            self.extend_open_area(cell_x, cell_y)
    def open(self):
        # for i in range(FIELD_SIZE[0]):
        #     for j in range(FIELD_SIZE[1]):
        #         self.cells[i][j].open()
        for point in self.points:
            self.cells[point[0]][point[1]].open()
    def update(self):
        pass
    def check_win(self):
        if self.flagged_cells == set(self.points):
            print("You won!")
            win_screen()
def win_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        msg_font = pygame.font.SysFont("Lucida Console", 24)
        text = msg_font.render("Ура!", True, (0, 0, 0))
        place = text.get_rect(center=(WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2))
        screen.blit(text, place)
        pygame.display.flip()

class Cell:
    cell_side = WINDOW_SIZE[0]//FIELD_SIZE[0]
    class Role(Enum):
        Empty = 0
        Mine = 1
        Flag = 2
        Number = 3
    def __init__(self, x, y, role) -> None:
        self.font = pygame.font.SysFont('Comic Sans MS', 18)
        self.role = role
        self.x = x
        self.y = y
        self.is_open = False
        self.is_number = False
        self.number = 0
        self.__set_color()
    
    def __set_color(self):
        if not self.is_open:
            match self.role:
                case Cell.Role.Flag:
                    self.color = (50,50,150)
                case _:
                    self.color = (220, 220, 220)
                
        elif self.is_open:
            match self.role:
                case Cell.Role.Empty:
                    self.color = (128,128,128)
                case Cell.Role.Mine:
                    self.color = (255, 0, 0)
                case Cell.Role.Flag:
                    self.color = (50,50,150)
                case Cell.Role.Number:
                    self.color = (128,128,128)
                    self.is_number = True
    def set_number(self, number):
        self.number = number
        match number:
            case 1:
                self.num_color = (0,255,0)
            case 2:
                self.num_color = (0,250,154)
            case 3:
                self.num_color = (255,215,0)
            case _:
                self.num_color = (0,0,255)
    def update(self):
        self.__set_color()
    def open(self):
        self.is_open = True
        self.update()
    def make_flag(self):
        self.role = Cell.Role.Flag
        self.update()
    def remove_flag(self):
        self.role = Cell.Role.Empty
        self.update()
    def draw(self, screen):
        if not self.is_number:
            pygame.draw.rect(screen, self.color, (self.x*Cell.cell_side, self.y*Cell.cell_side, Cell.cell_side, Cell.cell_side))
        elif self.is_number:
            pygame.draw.rect(screen, self.color, (self.x*Cell.cell_side, self.y*Cell.cell_side, Cell.cell_side, Cell.cell_side))
            one = self.font.render(str(self.number), True, self.num_color)
            place = one.get_rect(center=(self.x*Cell.cell_side+(Cell.cell_side//2), self.y*Cell.cell_side+(Cell.cell_side//2)))
            screen.blit(one, place)

def draw_point(screen, x ,y):
    pygame.draw.rect(screen, (255, 0, 0), (x*20, y*20, 20, 20))

def gen_random_points(count) -> list:
    result_list = []
    for _ in range(count):
        a = random.randint(0, FIELD_SIZE[0]-1)
        b = random.randint(0, FIELD_SIZE[1]-1)
        result_list.append((a,b))
    return result_list
    

grid = Grid()

while True:
    clock.tick(15)
    grid.check_win()
    grid.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos_x = event.pos[0]//(WINDOW_SIZE[0]//FIELD_SIZE[0])
            pos_y = event.pos[1]//(WINDOW_SIZE[1]//FIELD_SIZE[1])
            if event.button == 1:
                print(pos_x, pos_y)
                if grid.cells[pos_x][pos_y].role == Cell.Role.Flag:
                    pass
                elif grid.cells[pos_x][pos_y].role == Cell.Role.Number or grid.cells[pos_x][pos_y].role == Cell.Role.Mine:
                    grid.cells[pos_x][pos_y].open()
                    if (pos_x, pos_y) in grid.points:
                        grid.open()
                else:
                    grid.open_cell(pos_x, pos_y)
            if event.button == 3:
                print(pos_x, pos_y)
                if not grid.cells[pos_x][pos_y].role == Cell.Role.Flag:
                    grid.cells[pos_x][pos_y].make_flag()
                    grid.flagged_cells.add((pos_x, pos_y))
                    print(list(grid.flagged_cells), grid.points)
                else:
                    grid.cells[pos_x][pos_y].remove_flag()
                    grid.flagged_cells.remove((pos_x, pos_y))

                #draw_point(screen, pos_x, pos_y)
    pygame.display.flip()