import colorsys
from global_vars import *
import random
import global_vars

class Piece:
    def __init__(self, col, row, color, surface):
        self.row = row
        self.col = col
        self.color = color
        self.surface =surface
    
    def draw(self):
        pygame.draw.rect(self.surface, self.color, (PIECE_SIZE * self.col, PIECE_SIZE * self.row , PIECE_SIZE ,PIECE_SIZE) ,border_radius= 5)
        pygame.draw.rect(self.surface, (10, 10, 10), (PIECE_SIZE * self.col, PIECE_SIZE * self.row , PIECE_SIZE ,PIECE_SIZE), 2, 5)



class Shape:
    def update_shape(self):
        for i in range (len(self.pieces)):
            self.pieces[i].col = (self.col + SHAPES_FORMS[self.shape]["x" + self.direction][i])
            self.pieces[i].row = (self.row + SHAPES_FORMS[self.shape]["y" + self.direction][i])
            self.pieces[i].color = self.color
            


    def get_random_shape(self):
        list_of_shapes = ['I', 'L', 'J', 'O', 'S', 'Z', 'T']
        global_vars.current_shape = global_vars.next_shape
        global_vars.next_shape = random.choice(list_of_shapes)
        while  global_vars.current_shape == global_vars.next_shape :
            global_vars.next_shape = random.choice(list_of_shapes)
        return global_vars.current_shape

    def get_random_color(self):
        list_of_colors = [RED, BLUE, YELLOW, GREEN, ORANGE, CYAN]
        global_vars.current_color = global_vars.next_color

        global_vars.next_color = random.choice(list_of_colors)

        while global_vars.current_color == global_vars.next_color:
            global_vars.next_color = random.choice(list_of_colors)
        
        return global_vars.current_color

    def piece_outside_screen(self):
        for x in range(len(self.pieces)):
            if self.pieces[x].row < 0:
                return True
        return False

    def set_first_direction(self):
        while self.piece_outside_screen():
            self.direction = str(int(self.direction) + 90)
            self.update_shape()

    def create_new(self):
        self.row = 0
        self.col = 4
        self.color = self.get_random_color()
        self.direction = "0"
        self.shape = self.get_random_shape()
        self.surface = game_board
        self.pieces = []
        for i in range (4):
            self.pieces.append(Piece(self.col, self.row, self.color, self.surface))
        self.update_shape()
        self.set_first_direction()
        

    def __init__(self):
        self.create_new()

    def adjust_illegal_piece(self):
        self.update_shape()

        for i in range(len(self.pieces)):
            if self.pieces[i].col < 0:
                self.col += 1
                self.adjust_illegal_piece()
            elif self.pieces[i].col > 9:
                self.col -= 1
                self.adjust_illegal_piece()

    def rotate(self):
        self.direction = "0" if self.direction == "270" else str(int(self.direction) + 90)
        self.update_shape()

        if self.piece_in_same_place():
            if not self.gonna_hit_adjacent(1):
                self.col += 1;
            elif not self.gonna_hit_adjacent(-1):
                self.col -= 1;
            else:
                self.direction = "270" if self.direction == "0" else str(int(self.direction) - 90)
            self.update_shape()

    def draw(self):
        self.adjust_illegal_piece()

        for i in range (len(self.pieces)):
            self.pieces[i].draw()


    def gonna_hit_down(self):

        for i in range(len(self.pieces)):
            if self.pieces[i].row > 19:
                self.pieces[i].row = 0
            if piece_index[self.pieces[i].col][self.pieces[i].row + 1] != None or self.pieces[i].row > 19: return True
        return False

    def gonna_hit_adjacent(self, dirc):
        # dirc = 1 -> gonna hit right, dirc = -1 -> gonna hit left
        for i in range(len(self.pieces)):
            if piece_index[self.pieces[i].col + dirc][self.pieces[i].row] != None: return True
            if dirc == 1:
                if self.pieces[i].col + 1 > 9:
                    return True
            elif dirc == -1:
                if self.pieces[i].col - 1 < 0:
                    return True

        return False

    def save_pieces_index(self):
        for i in range(len(self.pieces)):
            piece_index[self.pieces[i].col][self.pieces[i].row] = self.color

    def delete_pieces_index(self):
        for i in range(len(self.pieces)):
            piece_index[self.pieces[i].col][self.pieces[i].row] = None
    
    def piece_in_same_place(self):
        self.update_shape()
        self.adjust_illegal_piece()
        for i in range(len(self.pieces)):
            try : 
                if self.pieces[i].row > 20 : self.pieces[i].row = 0
                if piece_index[self.pieces[i].col][self.pieces[i].row] != None :
                    return True
            except IndexError:
                return True 
        return False
    
    def draw_next_shape(self):
        global_vars.next_shape = global_vars.current_shape
        global_vars.next_color = global_vars.current_color
        self.shape = global_vars.next_shape
        self.color = global_vars.next_color
        self.col = 2
        self.row = 2

        for i in range(len(self.pieces)):
            self.pieces[i].surface = next_shape_surface
            self.pieces[i].color = global_vars.next_color
            self.pieces[i].col = (self.col + SHAPES_FORMS[self.shape]["x" + "0"][i])
            self.pieces[i].row = (self.row + SHAPES_FORMS[self.shape]["y" + "0"][i])

            self.pieces[i].draw()
    
    def draw_hold_shape(self):
        global_vars.next_shape = global_vars.current_shape
        global_vars.next_color = global_vars.current_color
        self.shape = global_vars.hold_shape
        self.col = 2
        self.row = 2
        for i in range(len(self.pieces)):
            self.pieces[i].surface = hold_shape_surface
            self.pieces[i].color = global_vars.hold_color
            self.pieces[i].col = (self.col + SHAPES_FORMS[self.shape]["x" + "0"][i])
            self.pieces[i].row = (self.row + SHAPES_FORMS[self.shape]["y" + "0"][i])
            self.pieces[i].draw()

           
        