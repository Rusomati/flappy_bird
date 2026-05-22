from random import randrange
from settings import *
from runtime_globals import *

def update():
    ...

#in theory can use a biased distribution for far-ness
def generate_pipe():
    pipes.append({'x':width+randrange(1,width),
                  'y':randrange(1,width-gap_height),
                  'gap_height': gap_height,
                  'width': pipe_width})

def delete_first_pipe():
    for i in range(len(pipes)-1):
        pipes[i] = pipes[i+1]
        pipes.pip()
