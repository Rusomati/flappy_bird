from utils import str_to_image, copy_image, sublist
import runtime_globals
from settings import *
from update import *

debug_fill = ' '

canvas = []

def draw_frame():
    clear_canvas()
    draw_pipes()
    draw_bird(bird_x, runtime_globals.bird_y)
    show()

def clear_canvas():
    global debug_fill
    global width
    global height
    global canvas
    canvas.clear()
    canvas += [list(debug_fill * width) for i in range(height)]

def draw_px(ch, x, y):
    global canvas

    is_inside = 0 <= x < width and 0 <= y < height

    if is_inside:
        canvas[y][x] = ch

    return is_inside

def draw_pipes():
    global generate_pipe
    global delete_first_pipe

    global canvas
    global width
    global height
    
    _, first_out = draw_pipe(canvas, runtime_globals.pipes[0], width, height)

    for pipe in sublist(runtime_globals.pipes, 1, 1):
        draw_pipe(canvas, pipe, width, height)

    last_in, _ = draw_pipe(canvas, runtime_globals.pipes[-1], width, height)

    if first_out:
        delete_first_pipe()

    if last_in:
        generate_pipe()

def draw_pipe(canvas , pipe , canvas_width , canvas_height):
    p_x = pipe ['x']
    gap_y =pipe['y']
    gap_h = pipe['gap_height']
    p_w = pipe['width']
    total_pixels = 0
    drawn_pixels = 0

    # draws the top pipe's vertical edges, in this implementation p_w is inclusive of the edges
    for y in range (0 , gap_y):
        for i in [0 , p_w - 1]:
            current_x = p_x + i
            total_pixels += 1
            if draw_px('|' , current_x , y):
                drawn_pixels += 1

    # draws the horizontal edges, in this implementation gap_h is inclusive of the edges
    for y in [gap_y , gap_y + gap_h - 1]:
        for i in range(p_w):
            current_x = p_x + i
            total_pixels += 1
            if draw_px('-' , current_x , y):
                drawn_pixels += 1

    # draws the bottom pipe's vertical edges, in this implementation p_w is inclusive of the edges
    for y in range(gap_y + gap_h , canvas_height ):
        for i in [0 , p_w - 1]:
            current_x = p_x + i
            total_pixels += 1
            if draw_px('|' , current_x , y):
                drawn_pixels += 1

    fully_inside = (drawn_pixels == total_pixels)        
    fully_outside = (drawn_pixels == 0)
    return (fully_inside , fully_outside)

def test_pipe(x, y):
    global canvas
    global width
    global height

    clear_canvas()
    draw_pipe(canvas, {'x': x, 'y': y, 'gap_height': gap_height, 'width': pipe_width}, width, height)
    show()

def draw_bird(x, y):
    global canvas
    y = round(y)
    for v_off, line in enumerate(bird_image):
        for h_off, px in enumerate(line):
            draw_px(px, bird_x+h_off, y+v_off)

# ugly at best..
def test_draw_bird(x, y):
    clear_canvas()
    draw_bird(x, y)
    show()

def show():
    scores_str = f'\x1b[Hscore: {runtime_globals.score}\thigh score: {runtime_globals.high_score}'
    canvas_str = '\n'.join(''.join(line) for line in canvas)
    border_str = '*' * width
    print('\n'.join([scores_str, border_str, canvas_str, border_str]), flush=True) # flush=True?
