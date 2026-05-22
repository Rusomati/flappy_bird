from utils import str_to_image

width = 64
height = round((width*9/16)/2)

frame_rate = 20

scroll_speed = 1

bird_x = width//4
bird_acceleration = -1.0
bird_jump_gain = 3.0
bird_image=str_to_image("""
@>
""")

pipe_width = 6
gap_height = 6
