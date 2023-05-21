from piece import *
from pygame import USEREVENT
import global_vars, ai

def get_completed_line():
    for y in range (20):
        row = []
        for x in range(10):
            row.append(piece_index[x][y])
        if None in row:
            continue
        return y
    return -1
def drop_above_pieces(completed_line):
    for y in range (completed_line, 0, -1):
        for x in range(10):
            piece_index[x][y] = piece_index[x][y - 1] 
def delete_completed_line(): 
    completed_line = get_completed_line()
    if completed_line != -1:
        for i in range (10):
            piece_index[i][completed_line] = None
        drop_above_pieces(completed_line)
        
def draw_next_shape():
    next_shape = Shape()
    next_shape_surface.fill((65, 65, 65))
    next_shape.draw_next_shape()

def update_round(dropping_piece):
    dropping_piece.update_shape()
    update_game_state()
    dropping_piece.create_new()
    draw_next_shape()
    if USE_AI:
        ai.run(dropping_piece)
        

# move the dropping piece 1 row down or stop it if it hits other pieces
def update_dropping_piece_state(dropping_piece):
    if not dropping_piece.gonna_hit_down():
        dropping_piece.row += 1 
    else:
        dropping_piece.save_pieces_index()
        update_round(dropping_piece)

def update_score():
    lines = global_vars.num_completed_line
    sum = 0 if lines == 0 else 40 if lines == 1 else 100 if lines == 2 else 300 if lines == 3 else 1200
    global_vars.current_score = str(int(global_vars.current_score) + sum)
 


# check if there is a completed line and delete it 
def get_completed_line():
    for y in range (20):
        row = []
        for x in range(10):
            row.append(piece_index[x][y])
        if None in row:
            continue
        return y
    return -1
def drop_above_pieces(completed_line):
    for y in range (completed_line, 0, -1):
        for x in range(10):
            piece_index[x][y] = piece_index[x][y - 1] 
def delete_completed_line():
    completed_line = get_completed_line()
    while completed_line != -1:
        global_vars.num_completed_line += 1
        for i in range (10):
            piece_index[i][completed_line] = None
        drop_above_pieces(completed_line)
        completed_line = get_completed_line()

# check if the game has ended
def is_game_over():
    for i in range (10):
        if piece_index[i][0] != None:  
            print("game ended")
            return True
    return False
def update_game_state():
    if is_game_over():
        global_vars.running = False

def draw_dropped_pieces():
    for col, _ in enumerate(piece_index):
        for row, color in enumerate(piece_index[col]):
            if color != None:
                piece = Piece(col, row, color, game_board)
                piece.draw()

# when click space drop the piece veryyy down
def piece_drop(dropping_piece): 
    while not dropping_piece.piece_in_same_place():
        dropping_piece.row += 1
        dropping_piece.update_shape()
    
    dropping_piece.row -= 1
    dropping_piece.update_shape()
    dropping_piece.save_pieces_index()
    update_round(dropping_piece)


def update_background():
    global_vars.SCORE_SURFACE = TEXT_FORMAT.render("SCORE = " + global_vars.current_score, False, (65, 65, 65))
    global_vars.num_completed_line = 0

    screen.fill((25, 25, 25))
    screen.blit(game_board, (SCREEN_WIDTH // 5 - game_board.get_width() // 5, SCREEN_HEIGHT // 2 - game_board.get_height() // 2))
    screen.blit(next_shape_surface, (SCREEN_WIDTH - NEXT_SHAPE_SURFACE_SIZE * 1.25, SCREEN_HEIGHT * 0.15))
    screen.blit(hold_shape_surface, (SCREEN_WIDTH - NEXT_SHAPE_SURFACE_SIZE * 1.25, SCREEN_HEIGHT * 0.5))
    screen.blit(NEXT_SURFACE, (SCREEN_WIDTH - NEXT_SHAPE_SURFACE_SIZE * 1.25, SCREEN_HEIGHT * 0.1))
    screen.blit(global_vars.HOLD_SURFACE, (SCREEN_WIDTH - NEXT_SHAPE_SURFACE_SIZE * 1.25, SCREEN_HEIGHT * 0.45))
    screen.blit(global_vars.SCORE_SURFACE, (SCREEN_WIDTH // 5 - game_board.get_width() // 5, SCREEN_HEIGHT // 2 - game_board.get_height() // 2 * 1.1))

    hold_shape_surface.fill((65, 65, 65))
    game_board.fill((65, 65, 65))
    
def move_down_while_pressing(dropping_piece):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
        global_vars.pressed_time += 1
    else:
        global_vars.pressed_time = 1
    if global_vars.pressed_time % 5 == 0:
        update_dropping_piece_state(dropping_piece)

def save_first_hold(dropping_piece) -> Piece:
    global_vars.hold_color = dropping_piece.color
    global_vars.hold_shape = dropping_piece.shape
    global_vars.first_hold = False

    update_round(dropping_piece)

def draw_holding_shape():
    if not global_vars.first_hold:
        hold_shape = Shape()
        hold_shape.draw_hold_shape()

def switch_holding_shape(dropping_piece):
    dropping_piece.color, global_vars.hold_color = global_vars.hold_color, dropping_piece.color
    dropping_piece.shape, global_vars.hold_shape = global_vars.hold_shape, dropping_piece.shape


