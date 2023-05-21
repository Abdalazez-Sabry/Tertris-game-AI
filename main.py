from pygame import K_DOWN, KEYDOWN, USEREVENT
from game_logic import *
import ai

def move_piece(event, dropping_piece):
    if event.key == pygame.K_z or event.key == pygame.K_UP:
        dropping_piece.rotate()
    if event.key == pygame.K_RIGHT:
        if not dropping_piece.gonna_hit_adjacent(1):
            dropping_piece.col +=1
    if event.key == pygame.K_LEFT:
        if not dropping_piece.gonna_hit_adjacent(-1):
            dropping_piece.col -=1
    if event.key == pygame.K_SPACE:
       piece_drop(dropping_piece)
    if event.key == pygame.K_c:
        if global_vars.first_hold:
            save_first_hold(dropping_piece)
        else:
            switch_holding_shape(dropping_piece)
            dropping_piece.update_shape()
            if dropping_piece.piece_in_same_place():
                switch_holding_shape(dropping_piece)


def take_input(dropping_piece):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            global_vars.running = False

        elif event.type == pygame.KEYDOWN:
            if not global_vars.USE_AI: move_piece(event, dropping_piece)
        
        elif event.type == pygame.USEREVENT and  global_vars.pressed_time == 1:
            # if USE_AI:
            #     ai.run(dropping_piece)
            # else:
            update_dropping_piece_state(dropping_piece)
            
    if not global_vars.USE_AI: move_down_while_pressing(dropping_piece)


def run():
    global_vars.next_color = random.choice([RED, BLUE, YELLOW, GREEN, ORANGE, CYAN])
    global_vars.next_shape = random.choice(['I', 'L', 'J', 'O', 'S', 'Z', 'T'])
    dropping_piece = Shape()
    pygame.time.set_timer(USEREVENT, 500)
    draw_next_shape()
    update_round(dropping_piece)        

    while global_vars.running:
        clock.tick(60)
        update_background()
        take_input(dropping_piece)
        delete_completed_line()
        dropping_piece.draw()
        pygame.display.flip()
        draw_dropped_pieces()
        draw_holding_shape()
        if global_vars.USE_AI:
            ai.drop_peice_slowly(dropping_piece)
            # piece_drop(dropping_piece)
        
        update_score()
        

def main():
    run()
    print(global_vars.current_score)
    pygame.quit()

 
main() 