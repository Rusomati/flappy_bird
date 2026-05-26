import time

import settings
import runtime_globals
import draw
import update
import game_io

# TODO: args, get high score?
def initialize():
    print('\x1b[2J') # clears the screen
    update.generate_pipe()
    runtime_globals.high_score = update.load_high_score()

def main_loop():
    should_run = True
    while should_run:
        draw.draw_frame()
        should_run = update.update()

        key = game_io.get_last_ch()
        if settings.debug:
            if key == 'w':
                runtime_globals.bird_y -= 1
            if key == 's':
                runtime_globals.bird_y += 1
            if key == 'd':
                update.move_pipes()
        else:
            if key == ' ':
                runtime_globals.bird_velocity = -settings.bird_jump_gain
 
        # can improve..
        time.sleep(1/settings.frame_rate)

def show_game_over_screen():
    #draw.draw_frame()
    game_io.get_last_ch()
    print('game over, press any key to exit')
    while not game_io.get_last_ch(): time.sleep(1/settings.frame_rate)

if __name__ == '__main__':
    initialize()
    main_loop()
    show_game_over_screen()
