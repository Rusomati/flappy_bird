import random
import os

import settings
import runtime_globals
import draw

def update():
    did_collide = check_collision({'y': runtime_globals.bird_y})
    
    increase_score()

    runtime_globals.high_score = update_high_score(runtime_globals.score, runtime_globals.high_score)

    if not settings.debug:
        move_pipes()

        runtime_globals.bird_y += runtime_globals.bird_velocity
 
        runtime_globals.bird_velocity -= settings.bird_acceleration

    return not did_collide

def move_pipes():
    for pipe in runtime_globals.pipes:
        pipe['x'] -= settings.scroll_speed

def increase_score():
    for pipe in runtime_globals.pipes:
        if settings.bird_x >= (pipe['width'] + pipe['x']) and not pipe['passed']: 
            runtime_globals.score += 1
            #TODO rem? runtime_globals.high_score = max(runtime_globals.score, runtime_globals.high_score)
            pipe['passed'] = True

# why not in main, it runs once
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

def update_high_score(current_score , current_high_score):
    if current_score > current_high_score :
        with open("highscore.txt" , "w") as file :
            file.write(str(current_score))
        return current_score
    return current_high_score    
                
def check_collision(bird  ):
    bird_y = round(bird['y']) # we use round() in draw_bird
    if bird_y < 0 or bird_y >= settings.height:
        return True
    for pipe in runtime_globals.pipes :
        pipe_x = pipe['x']
        gap_y = pipe['y']
        if settings.bird_x + 1 >= pipe_x and settings.bird_x < pipe_x + settings.pipe_width:
            if bird_y <= gap_y or bird_y >= (gap_y + settings.gap_height - 1) :
                return True
    return False        

# uhhhh + CURRENTLY (?) MUST IMPORT DRAW BEFORE UPDATE
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
        p_x = settings.width + random.randrange(settings.minimum_cross_pipe_distance, settings.width)

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
