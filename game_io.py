# this module currently breaks init and deinit semantics in main
# but imports are top-level so, init kinda has to be coupled, what about de-init?

import time
import atexit

is_unix = False

def clean_unix(old_term_state):
    termios.tcsetattr(stdin_fd, termios.TCSAFLUSH, old_term_state)

try:
    import msvcrt # a windows-only built-in module

    import ctypes
    # Get handles to stdout and the kernel32 DLL
    kernel32 = ctypes.windll.kernel32
    handle = kernel32.GetStdHandle(-11)  # -11 is standard output (stdout)

    # Get the current console mode flags
    mode = ctypes.c_ulong()
    kernel32.GetConsoleMode(handle, ctypes.byref(mode))

    # Flip the bit for ENABLE_VIRTUAL_TERMINAL_PROCESSING (0x0004)
    kernel32.SetConsoleMode(handle, mode.value | 0x0004)

except Exception: # we are probably not in windows if an exception was raised
    is_unix = True
    stdin_fd = 0 # 0 stands for the standard input file descriptor
    
    from os import set_blocking
    set_blocking(stdin_fd, False) # blocking mode forces the program to wait until there is an input

    from tty import setcbreak
    old_term_state = setcbreak(stdin_fd) # cbreak mode allows the program to terminate with ctrl-c for example
                                         # while also allowing us to read input before enter is pressed

    import termios
    atexit.register(clean_unix, old_term_state) # reset terminal when the program ends

    from sys import stdin # for stdin.read

def get_last_ch():
    if is_unix:
        try:
            return stdin.read()[-1]
        except Exception: # the read raises an exception when there is nothing to read
            return ''
    else:
        res = ''
        while msvcrt.kbhit(): # runs until there are no characters to get
            res = msvcrt.getwch()
        return res

#while True:
#    last_ch = get_last_ch() or 'nothing'
#    print(f'got: {last_ch}')
#    time.sleep(1)
