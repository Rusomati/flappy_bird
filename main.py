import time

import settings
import runtime_globals
import draw
import update
import game_io

# TODO: args, get high score?
def initialize():
    update.generate_pipe() 
    
def main_loop():
    while True:
        draw.draw_frame()
        update.update()

        if game_io.get_last_ch() == ' ':
            runtime_globals.bird_velocity = -settings.bird_jump_gain

        # can improve..
        time.sleep(1/settings.frame_rate)

if __name__ == '__main__':
    initialize()
    main_loop()
