from time import sleep

from settings import *
from get_input import get_last_ch

# args, get high score?
def initialise():
    ...
    
    
def main_loop():
    while True:
        update()
        draw_and_collide()

        if get_last_char() == ' ':
            bird_velocity += bird_jump_gain

        sleep(1/frame_rate)

if __name__ == '__main__':
    initialise()
    main_loop()
