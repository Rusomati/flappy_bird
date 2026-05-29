import math
import random

import settings
import runtime_globals
import draw

def update():
    did_collide = check_collision({'y': runtime_globals.bird_y})

    if not settings.debug:
        move_pipes()

        runtime_globals.bird_y += runtime_globals.bird_velocity
 
        runtime_globals.bird_velocity -= settings.bird_acceleration
 
    increase_score()
    runtime_globals.high_score = update_high_score(runtime_globals.score, runtime_globals.high_score)

    return not did_collide

def move_pipes():
    for pipe in runtime_globals.pipes:
        pipe['x'] -= settings.scroll_speed

def increase_score():
    for pipe in runtime_globals.pipes:
        if settings.bird_x >= (settings.pipe_width + pipe['x']) and not pipe['passed']: 
            runtime_globals.score += 1
            pipe['passed'] = True

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

# superceeded by debug mode
"""
def test_score():
    runtime_globals.pipes.clear()
    generate_pipe()

    while True:
        increase_score()

        draw.clear_terminal()
        draw.draw_frame()
        print(f'{settings.bird_x=}, {runtime_globals.pipes[0]['x']=}')

        shift = -int(input('insert the amount of shifting you want to perform: '))
        for pipe in runtime_globals.pipes:
            pipe['x'] += shift

        # first pipe should be in scope else it will be deleted next frame for being outside the canvas...
        runtime_globals.pipes[0]['x'] = min(runtime_globals.pipes[0]['x'], settings.width - 1)
"""

# NOT WRITTEN WITH THE HELP OF AI, ALSO WE FOUND THIS IDEA INDEPEDANTLY
# point-wise approximation
def approx_min_pipe_x_off(delta_y):
    """
    delta_y = y(t)
    scroll_x = delta_x / t => t = delta_x / scroll_x
    this function aims to calculate a fitting delta_x

    (first branch)
    when delta_y is negative y(t) = jumpgain * t
    this is because the next pipe is higher, so you are capped by jump speed
    jumping in this game resets velocity and acceleration can be ignored if you spam jump

    delta_y = jumpgain * delta_x / scroll_x
    delta_y * scroll_x / jumpgain = delta_x
    delta_x = delta_y * scroll_x / jumpgain
    (we flip relevant signs in code)

    (second branch)
    when delta_y is positive y(t) = sum(v(i)) from i=0 to i=t)
    v(i) = a * i
    y(t) = integral(a*t) with respect to t
    y(t) = a * t**2 / 2

    another formulation:
    y(t) = sum(a*i from i=0 to i=t) = a * sum(i from i=0 to i=t)
    substituting the triangle number formula:
    y(t) = a * t * (t + 1) / 2
    when t is big enough, it would become fairly close to t+1
    y(t) = a * t * t / 2
    y(t) = a * t**2 / 2

    delta_y = a * (delta_x / scroll_x)**2 / 2
    2 * delta_y / a = delta_x ** 2 / scroll_x ** 2
    2 * scroll_x ** 2 * delta_y / a = delta_x ** 2
    sqrt(2 * scroll_x**2 * delta_y / a) = delta_x
    delta_x = sqrt(2 * delta_y / a) * scroll_x

    (we flip relevant signs in code)
    """
    if delta_y < 0:
        return -delta_y * (settings.scroll_speed / settings.bird_jump_velocity)
    else:
        return math.sqrt(2 * delta_y / -settings.bird_acceleration) * settings.scroll_speed

def generate_pipe():
    p_y = random.randrange(1, settings.height - settings.gap_height)

    # first pipe should be in scope else it will be deleted next frame for being outside the canvas...
    if len(runtime_globals.pipes) == 0:
        p_x = settings.width - 1
    else:
        delta_x = round((approx_min_pipe_x_off(p_y - runtime_globals.pipes[-1]['y']) + 1) \
                * settings.min_pipe_distance_slack_factor)

        # min is used to clamp the distance, if distance is too big pipe will be freed before its used
        p_x = settings.width + random.randint(delta_x,\
            min(settings.width - 1,round(delta_x * settings.max_to_min_pipe_distance_factor)))

    runtime_globals.pipes.append({'x': p_x,
                                  'y': p_y,
                                  'passed' : False })

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
