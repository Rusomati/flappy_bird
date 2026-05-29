import time
import os

import settings
import runtime_globals
import draw
import update
import io_init_and_kb

def load_high_score():
    file_name = "highscore.txt"
    if not os.path.exists(file_name):
        with open(file_name , "w") as file :
            file.write("0")
            return 0
    with open(file_name , "r") as file : 
        try :
            return int (file.read().strip())
        except ValueError:
            return 0

# TODO: args, get high score?
def initialize():
    print('\x1b[2J') # clears the screen
    update.generate_pipe()
    runtime_globals.high_score = load_high_score()

def main_loop():
    should_run = True
    while should_run:
        draw.draw_frame()
        should_run = update.update()
        io_init_and_kb.process_last_keypress()
 
        # can improve..
        time.sleep(1/settings.frame_rate)

def show_game_over_screen():
    #draw.draw_frame()
    io_init_and_kb.get_last_ch()
    print('game over, press any key to exit')
    while not io_init_and_kb.get_last_ch(): time.sleep(1/settings.frame_rate)

if __name__ == '__main__':
    initialize()
    main_loop()
    show_game_over_screen()
