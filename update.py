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

# NOT WRITTEN WITH THE HELP OF AI, ALSO WE FOUND THIS IDEA INDEPEDANTLY
# point-wise approximation
def approx_min_pipe_x_off(delta_y):
    estimated_time = None

    if delta_y < 0:
        # yv = dy/dt
        # dt = dy/yv
        # acceleration doesnt count as jumping resets acceleration, if you spam jump acceleration basically ceases
        # and spamming jump is expected if you want to go up as soon as possible, which is expected given
        # how we want the minimum time to reach the pipe
        estimated_time = -delta_y / settings.bird_jump_velocity
    else:
        # y = sum(velocity(i), from i=0 to i=t) | integral(v(i)*di, from i=0 to i=t)
        # velocity(i) = acceleration * i
        # y = sum(acceleration * i, from i=0 to i=t) | integral(acceleration * i * di, from i=0 to i=t)
        # y = acceleration * sum(i, from i=0 to i=t) | acceleration * t**2 / 2 - 0
        # (triangle number formula)
        # y = `acceleration * t * (t+1) / 2` close to `acceleration * t * t / 2` | ...
        # y = acceleration * t**2 / 2 | acceleration * t**2 / 2
        # y = acceleration * t**2 / 2
        # 2 * y / acceleration = t**2
        # t = sqrt(2 * y / acceleration)
        estimated_time = math.sqrt(2 * delta_y / -settings.bird_acceleration)

    # vx = dx/dt
    # dx = vx*dt
    return round(estimated_time * settings.scroll_speed)

def generate_pipe():
    p_y = random.randrange(1, settings.height - settings.gap_height - 1)

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
