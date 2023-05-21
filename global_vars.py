import pygame

pygame.init()
pygame.font.init()

current_score = "0"
num_completed_line = 0

TEXT_FORMAT = pygame.font.SysFont("Comic Sans MS", 30)
NEXT_SURFACE = TEXT_FORMAT.render("NEXT", False, (65, 65, 65))
HOLD_SURFACE = TEXT_FORMAT.render("HOLD", False, (65, 65, 65))



SCREEN_WIDTH = 760
SCREEN_HEIGHT = 900
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
USE_AI = True
running = True

clock = pygame.time.Clock()

#Colors
GREY = (70, 70, 70)
BLACK = (0, 0 ,0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255,140,0)
GREEN = (50, 70, 50)
YELLOW = (255, 100, 0)
CYAN = (0,255,255)

game_board = pygame.Surface((SCREEN_WIDTH * 0.5, SCREEN_WIDTH))

PIECE_SIZE = SCREEN_WIDTH * 0.05
NEXT_SHAPE_SURFACE_SIZE = PIECE_SIZE * 6
HOLD_SHAPE_SURFACE_SIZE = PIECE_SIZE * 6


hold_shape_surface = pygame.Surface((HOLD_SHAPE_SURFACE_SIZE, HOLD_SHAPE_SURFACE_SIZE))
next_shape_surface = pygame.Surface((NEXT_SHAPE_SURFACE_SIZE, NEXT_SHAPE_SURFACE_SIZE))

piece_index = [[None for x in range(22)] for x in range(13)]

for i in range(13):
    piece_index[i][20] = RED




SHAPES_FORMS = { "I": {"x0" : (0, 0, 0, 0), "y0": (-1, 0, 1 ,2), "x90": (-1, 0, 1 ,2), "y90": (0, 0, 0, 0), "x180" : (1, 1, 1, 1), "y180": (-1, 0, 1 ,2), "x270": (-1, 0, 1 ,2), "y270": (1, 1, 1, 1)},
                "O": {"x0" : (0, 0, 1, 1), "y0": (0, 1, 0, 1), "x90": (0, 0, 1, 1), "y90": (0, 1, 0, 1), "x180" : (0, 0, 1, 1), "y180": (0, 1, 0, 1), "x270": (0, 0, 1, 1), "y270": (0, 1, 0, 1)},
                "T": {"x0" : (0, 0, 1, -1), "y0": (0, -1, 0, 0), "x90": (0, 1, 0, 0), "y90": (0, 0, 1, -1), "x180" : (0, 0, 1, -1), "y180": (0, 1, 0, 0), "x270": (0, -1, 0, 0), "y270": (0, 0, 1, -1)},
                "S": {"x0" : (0, 1, 0, -1), "y0": (0, 0, 1, 1), "x90": (0, 0, 1, 1), "y90": (0, -1, 0, 1), "x180" : (0, 1, 0, -1), "y180": (0, 0, 1, 1), "x270": (0, 0, 1, 1), "y270": (0, -1, 0, 1)}, 
                "Z": {"x0" : (0, -1, 0, 1), "y0": (0, 0, 1 ,1), "x90": (0, 0, -1, -1), "y90": (0, -1, 0 ,1), "x180" : (0, -1, 0, 1), "y180": (0, 0, 1 ,1), "x270": (0, 0, -1, -1), "y270": (0, -1, 0, 1)},
                "L": {"x0" : (0, 0, 0, 1), "y0": (-1, 0, 1, 1), "x90": (1, 0, -1, -1), "y90": (0, 0, 0, 1), "x180" : (0, 0, 0, -1), "y180": (1, 0, -1, -1), "x270": (-1, 0, 1, 1), "y270": (0, 0, 0, -1)},
                "J": {"x0" : (0, 0, 0, -1), "y0": (-1, 0, 1, 1), "x90": (1, 0, -1, -1), "y90": (0, 0, 0, -1), "x180" : (0, 0, 0, 1), "y180": (1, 0, -1, -1), "x270": (-1, 0, 1, 1), "y270": (0, 0, 0, 1)}
}
current_shape = ""
current_color = ""

next_shape =  ""
next_color =  ""

hold_shape = "O"
hold_color = RED
first_hold = True

pressed_time = 1

    

