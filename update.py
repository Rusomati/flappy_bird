from random import randrange
from settings import *
from runtime_globals import *
#TODO: fix the testing mess
import draw

def update():
    #update bird and pipes, and..
    for pipe in pipes:
        pipe['x'] -= scroll_speed

    bird_velocity += bird_acceleration
    
def increase_score():
    runtime_globals.score += 1

#in theory can use a biased distribution for far-ness
def generate_pipe():
    pipes.append({'x':width + randrange(1, width),
                  'y':randrange(1, height - gap_height),
                  'gap_height': gap_height,
                  'width': pipe_width , 'passed' : False })

def very_basic_height_testing():
    while True:
        pipes.clear()
        generate_pipe()
        draw.test_pipe(12, pipes[0]['y'])
        print(f'\t\t\theight: {pipes[0]['y']}')
        input()

def delete_first_pipe():
    for i in range(len(pipes)-1):
        pipes[i] = pipes[i+1]

    pipes.pop()
