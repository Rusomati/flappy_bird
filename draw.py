import runtime_globals
import update
import utils
import settings

canvas_fill = ' '

canvas = []

def clear_terminal():
    print('\x1b[2J')

def draw_frame():
    clear_canvas()
    draw_pipes()
    draw_bird(settings.bird_x, runtime_globals.bird_y)
    show()

def clear_canvas():
    global canvas
    canvas.clear()
    canvas += [list(canvas_fill * settings.width) for i in range(settings.height)]

def draw_px(ch, x, y):
    global canvas

    is_inside = 0 <= x < settings.width and 0 <= y < settings.height

    if is_inside:
        canvas[y][x] = ch

    return is_inside

def draw_pipes():
    _, first_out = draw_pipe(canvas, runtime_globals.pipes[0], settings.width, settings.height)

    for pipe in utils.sublist_iterator(runtime_globals.pipes, 1, len(runtime_globals.pipes) - 1):
        draw_pipe(canvas, pipe, settings.width, settings.height)

    last_in, _ = draw_pipe(canvas, runtime_globals.pipes[-1], settings.width, settings.height)

    if first_out:
        update.delete_first_pipe()

    if last_in:
        update.generate_pipe()

# idea: make a detailed docstring that takes basically every ambiguous variable?
# draws a pipe and returns whether the pipe is fully inside the canvas and whether it is fully outside it
# those returns are used to track relevant head pipes, and generate tail pipes
def draw_pipe(canvas , pipe , canvas_width , canvas_height):
    p_x = pipe ['x']
    gap_y =pipe['y']
    gap_h = settings.gap_height
    p_w = settings.pipe_width
    total_pixels = 0
    drawn_pixels = 0

    # draws the top pipe's vertical edges row by row, top to bottom, in this implementation p_w is inclusive of the edges
    for y in range (0 , gap_y):
        for i in [0 , p_w - 1]:
            current_x = p_x + i
            total_pixels += 1
            if draw_px('|' , current_x , y):
                drawn_pixels += 1

    # draws the top horizontal edge, then the bottom one, both column by column and left to right
    for y in [gap_y , gap_y + gap_h - 1]:
        for i in range(p_w):
            current_x = p_x + i
            total_pixels += 1
            if draw_px('-' , current_x , y):
                drawn_pixels += 1

    # draws the bottom pipe's vertical edges row by row, top to bottom, in this implementation p_w is inclusive of the edges
    for y in range(gap_y + gap_h , canvas_height ):
        for i in [0 , p_w - 1]:
            current_x = p_x + i
            total_pixels += 1
            if draw_px('|' , current_x , y):
                drawn_pixels += 1

    fully_inside = (drawn_pixels == total_pixels)        
    fully_outside = (drawn_pixels == 0)
    return (fully_inside , fully_outside)

def test_draw_pipe(x, y):
    clear_terminal()
    clear_canvas()
    res = draw_pipe(canvas, {'x': x, 'y': y}, settings.width, settings.height)
    show()
    return res

def draw_bird(x, y):
    y = round(y)
    for v_off, line in enumerate(settings.bird_image):
        for h_off, px in enumerate(line):
            draw_px(px, x+h_off, y+v_off)

# ugly at best..
def test_draw_bird(x, y):
    clear_terminal()
    clear_canvas()
    draw_bird(x, y)
    show()

def show():
    scores_str = f'\x1b[Hscore: {runtime_globals.score}\thigh score: {runtime_globals.high_score}'
    canvas_str = '\n'.join(''.join(line) for line in canvas)
    border_str = '*' * settings.width
    print('\n'.join([scores_str, border_str, canvas_str, border_str]), flush=True) # flush=True?
