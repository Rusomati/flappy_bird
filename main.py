from time import sleep

from get_input import get_last_ch #..
import settings
import runtime_globals
import update

# TODO: args, get high score?
def initialize():
    update.generate_pipe() 
    
def main_loop():
    while True:
        draw.draw_frame()
        update.update()

        if get_last_char() == ' ':
            runtime_globals.bird_velocity += settings.bird_jump_gain

        # can improve..
        sleep(1/settings.frame_rate)

if __name__ == '__main__':
    initialize()
    main_loop()
