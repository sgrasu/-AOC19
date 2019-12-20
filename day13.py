import intcode
import collections
import time
import curses

def print_screen(pixels, stdscr):
    xs = sorted(pixels.keys(), key= lambda k: k[0])
    ys = sorted(pixels.keys(), key = lambda k: k[1])
    xmin, xmax = xs[0][0], xs[-1][0]
    ymin, ymax = ys[0][1], ys[-1][1]

    screen = [[' '] * (xmax - xmin + 1) for _ in range(ymax - ymin + 1)]
    for y in range(ymax - ymin + 1):
        for x in range(xmax - xmin + 1):
            if pixels[(x, y)] == 0:
                char = ' '
            elif pixels[(x, y)] == 1:
                char = '|'
            elif pixels[(x, y)] == 2:
                char= '='
            elif pixels[(x, y)] == 3:
                char = '_'
            else:
                char = 'o' 
            stdscr.addstr(y, x, char)
    stdscr.refresh()
    time.sleep(0.015)
        
def play(game, pixels, stdscr):
    cursor = 0
    ball = 0
    i = 0
    x = 0
    y = 0
    while True:
        out = game.start()
        if i == 0:
            x = out
        elif i == 1:
            y = out
        else:
            if x == -1:
                stdscr.addstr(20, 38,"score: " + str(out))
                drawing = False
            else:
                pixels[(x, y)] = out
                if out == 4:
                    print_screen(pixels, stdscr)
                    ball = x 
                elif out == 3:
                    cursor = x
                if cursor < ball:
                    game.set_input(1)
                elif cursor > ball:
                    game.set_input(-1)
                else:
                    game.set_input(0)
        i = (i + 1) % 3

def main(stdscr):
    game = intcode.IntCode('day13_in',2)
    pixels = collections.defaultdict(lambda: ' ')
    try:
        play(game, pixels,stdscr)
    except StopIteration:
        time.sleep(3)

curses.wrapper(main)