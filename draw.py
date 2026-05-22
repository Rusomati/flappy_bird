from runtime_globals import *
from utils import str_to_image, copy_image
from settings import *

debug_fill = '*'

def draw_frame():
    clear_canvas()
    draw_pipes()
    draw_bird(bird_x, bird_y)
    print(f'score: {score}\thigh score: {high_score}')
    print('*' * width)
    show()
    print('*' * width)

def clear_canvas():
    global canvas
    global debug_fill
    global width
    global height
    canvas.clear()
    canvas += [list(debug_fill * width) for i in range(height)]

def draw_px(ch, x, y):
    is_inside = 0 <= x < width and 0 <= y < height

    if is_inside:
        canvas[y][x] = ch

    return is_inside

def draw_pipes():
    global canvas
    global width
    global height
    global pipes
    
    _, first_out = draw_pipe(canvas, pipes[0], width, height)

    for pipe in pipes[1:-1]: # can optimise by removing this copy..
        draw_pipe(canvas, pipe, width, height)

    last_in, _ = draw_pipe(canvas, pipes[-1], width, height)

    if first_out:
        delete_first_pipe()

    if last_in:
        generate_pipe()

def draw_pipe(canvas , pipe , canvas_width , canvas_height):
    p_x = pipe ['x']
    gap_y =pipe['y']
    gap_h = pipe['gap_height'] # TODO: make a constant?
    p_w = pipe['width']
    for y in range (1 , gap_y):
        for i in [0 , p_w - 1]:
            current_x = p_x + i
            draw_px('|' , current_x , y)
    for y in [gap_y , gap_y + gap_h - 1]:
        for i in range(p_w):
            current_x = p_x + i
            draw_px('-' , current_x , y)
    for y in range(gap_y + gap_h , canvas_height):
        for i in [0 , p_w - 1]:
            current_x = p_x + i
            draw_px('|' , current_x , y)

def test_pipe(x, y):
    global canvas
    global width
    global height
    clear_canvas()
    draw_pipe(canvas, {'x': x, 'y': y, 'gap_height': gap_height, 'width': pipe_width}, width, height)
    show()

def draw_bird(x, y):
    global canvas
    for v_off, line in enumerate(bird_image):
        for h_off, px in enumerate(line):
            draw_px(px, x+h_off, y+v_off)

def test_draw_bird(x, y):
    clear_canvas()
    draw_bird(x, y)
    show()

def show():
    for line in canvas:
        print(''.join(line))
