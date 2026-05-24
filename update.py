import random

import settings
import runtime_globals
import draw

def update():
    for pipe in runtime_globals.pipes:
        pipe['x'] -= settings.scroll_speed

    runtime_globals.bird_y += runtime_globals.bird_velocity
    runtime_globals.bird_velocity += settings.bird_acceleration

    increase_score()

def increase_score():
    for pipe in runtime_globals.pipes:
        if settings.bird_x >= (pipe['width'] + pipe['x']) and not pipe['passed']: 
            runtime_globals.score += 1
            pipe['passed'] = True

# uhhhh + CURRENTLY MUST IMPORT DRAW BEFORE UPDATE
def score_test():
    runtime_globals.pipes.clear()
    generate_pipe()

    while True:
        increase_score()
        draw.draw_frame()
        print(f'{settings.bird_x=}, {runtime_globals.pipes[0]['x']=}')

        shift = -int(input('insert the amount of shifting you want to perform: '))
        for pipe in runtime_globals.pipes:
            pipe['x'] += shift

        # first pipe should be in scope else it will be deleted next frame for being outside the canvas...
        runtime_globals.pipes[0]['x'] = min(runtime_globals.pipes[0]['x'], settings.width - 1)

#in theory can use a biased distribution for far-ness
def generate_pipe():
    # first pipe should be in scope else it will be deleted next frame for being outside the canvas...
    if len(runtime_globals.pipes) == 0:
        p_x = settings.width - 1
    else:
        p_x = settings.width + random.randrange(1, settings.width)

    runtime_globals.pipes.append({'x': p_x,
                  'y': random.randrange(1, settings.height - settings.gap_height),
                  'gap_height': settings.gap_height,
                  'width': settings.pipe_width , 'passed' : False })

def very_basic_height_testing():
    while True:
        runtime_globals.pipes.clear()
        generate_pipe()
        draw.test_pipe(12, runtime_globals.pipes[0]['y'])
        print(f'\t\t\theight: {runtime_globals.pipes[0]['y']}')
        input()

def delete_first_pipe():
    for i in range(len(runtime_globals.pipes)-1):
        runtime_globals.pipes[i] = runtime_globals.pipes[i+1]

    runtime_globals.pipes.pop()
