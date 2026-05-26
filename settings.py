from utils import str_to_image

debug = False

width = 64
height = round((width*9/16)/2)

frame_rate = 20

scroll_speed = 1

bird_x = width // 4
bird_acceleration = -0.02
bird_jump_gain = 0.3
bird_image=str_to_image("""
@>
""")

min_pipe_distance_slack_factor = 1.1
max_to_min_pipe_distance_factor = 2.0
pipe_width = 6
gap_height = 6
