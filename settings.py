from utils import str_to_image

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

# can get by a formula related to accel and scroll speed?
# can make non static and can derive it in update() or smth?
minimum_cross_pipe_distance = 14
pipe_width = 6
gap_height = 6
