from utils import str_to_image

debug = False

width = 64
height = round((width*9/16)/2)

frame_rate = 20

scroll_speed = 1

bird_x = width // 4
bird_acceleration = -0.02
bird_jump_gain = 0.3
bird_image = str_to_image("""
@>
""")

min_pipe_distance_slack_factor = 1.1
max_to_min_pipe_distance_factor = 2.0
pipe_width = 6
gap_height = 6

def shift_bird_y(sh): runtime_globals.bird_y += sh

debug_key_actions = {
        'w' : lambda: shift_bird_y(-1) # apparently, i can not assign in a lambda
        's' : lambda: shift_bird_y(1)
        'd' : lambda: update.move_pipes()
        }

normal_key_actions = {' ': lambda: runtime_globals.bird_velocity = -bird_jump_gain}

key_actions = debug_key_actions if debug else normal_key_actions
