import ai_global, global_vars, piece, game_logic

def initialize():
    ai_global.max_point = -9999999999
    ai_global.max_point_col = 0
    ai_global.max_point_dirc = "90"

    ai_global.next_piece = piece.Shape()
    ai_global.next_piece.shape = global_vars.next_shape

    global_vars.first_hold = False


def calculate_piece_above_none():
    for col in range(10):
        for row in range(20):
            if global_vars.piece_index[col][row] != None and global_vars.piece_index[col][row + 1] == None:
                ai_global.current_point +=  row + ai_global.PIECE_ABOVE_NONE_VALUE
                # calculate_near_end(row)


def calculate_near_end(row):
    if row < 2:
        ai_global.current_point = -9999999
    elif row < 10:
        ai_global.current_point += ai_global.NEAR_END_VALUE * 1/row

def calculate_I_on_hold():
    if global_vars.hold_shape == "I":
        ai_global.current_point += ai_global.I_ON_HOLD_VALUE
        

def calculate_max_height():
    for row in range(20):
        row_list = []
        for col in range(10):
            if global_vars.piece_index[col][row] != None:
                ai_global.current_point += row + ai_global.MAX_HEIGHT_VALUE
            row_list.append(global_vars.piece_index[col][row])
        if None not in row_list:
            ai_global.ai_num_completed_lines += 1
    
def calculate_only_one_none_col():
    for row in range(20):
        none_count = 0
        for col in range(10):
            if global_vars.piece_index[col][row] == None: none_count += 1
        if none_count == 1 : ai_global.current_point += ai_global.ONE_NONE_VALUE

def calculate_completed_lines():
    try: 
        ai_global.current_point += ai_global.COMPLETED_LINE_VALUE[ai_global.ai_num_completed_lines]
    except IndexError:
        print(ai_global.ai_num_completed_lines)

def calculate_points():
    ai_global.ai_num_completed_lines = 0

    calculate_piece_above_none()
    calculate_max_height()
    # calculate_I_on_hold()
    # calculate_completed_lines()
    



def switch_piece(dropping_piece):
    game_logic.switch_holding_shape(dropping_piece)
    dropping_piece.update_shape()
    if dropping_piece.piece_in_same_place():
        game_logic.switch_holding_shape(dropping_piece)

def ai_piece_drop(dropping_piece): 
    while not dropping_piece.piece_in_same_place():
        dropping_piece.row += 1
        dropping_piece.update_shape()
    
    dropping_piece.row -= 1
    dropping_piece.update_shape()
    dropping_piece.adjust_illegal_piece()

    dropping_piece.save_pieces_index()

def try_all_plays(dropping_piece):
    for holding_piece_num in range (2):
        game_logic.switch_holding_shape(dropping_piece) 
        for dirc in  ["0", "90", "180", "270"]:
            for col in range (10):
                dropping_piece.row, dropping_piece.col, dropping_piece.direction = 0, col, dirc
                
                dropping_piece.update_shape()
                dropping_piece.adjust_illegal_piece()
                ai_piece_drop(dropping_piece)

                for dirc2 in  ["0", "90", "180", "270"]:
                    for col2 in range (10):
                        ai_global.next_piece.row,  ai_global.next_piece.col,  ai_global.next_piece.direction = 0, col2, dirc2
                        ai_global.current_point = 0
                        
                        ai_global.next_piece.update_shape()
                        ai_global.next_piece.adjust_illegal_piece()
                        ai_piece_drop(ai_global.next_piece)
                        global_vars.next_shape = global_vars.current_shape
                        global_vars.next_color = global_vars.current_color
                        
                        calculate_points()

                        ai_global.next_piece.delete_pieces_index()

                        if ai_global.current_point > ai_global.max_point:
                            ai_global.max_point = ai_global.current_point
                            ai_global.max_point_col = col
                            ai_global.max_point_dirc = dirc
                            ai_global.switch_piece = holding_piece_num

                ai_global.next_piece.row = 0
                dropping_piece.delete_pieces_index()

    dropping_piece.row = 0
    


def get_best_play(dropping_piece):
    try_all_plays(dropping_piece)

def drop_peice_slowly(dropping_piece):
    global_vars.pressed_time += 1

    if global_vars.pressed_time % 2 == 0:
        game_logic.update_dropping_piece_state(dropping_piece)

def play(dropping_piece):
    dropping_piece.col = ai_global.max_point_col
    dropping_piece.direction = ai_global.max_point_dirc
    if ai_global.switch_piece == 0: switch_piece(dropping_piece)

    dropping_piece.update_shape()
    dropping_piece.adjust_illegal_piece()
    # game_logic.piece_drop(dropping_piece)

def run(dropping_piece):
    initialize()
    get_best_play(dropping_piece)
        
    play(dropping_piece)
    





