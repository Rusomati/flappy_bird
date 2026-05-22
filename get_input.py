from time import sleep

is_unix = False

try:
    import msvcrt # a windows-only built-in module
except Exception: # we are probably not in windows if an exception was raised
    is_unix = True
    stdin_fd = 0 # 0 stands for the standard input file descriptor
    
    from os import set_blocking
    set_blocking(stdin_fd, False) # blocking mode forces the program to wait until there is an input

    from tty import setcbreak
    setcbreak(stdin_fd) # cbreak mode allows the program to terminate with ctrl-c for example
                            # while also allowing us to read input before enter is pressed

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
#    sleep(1)
