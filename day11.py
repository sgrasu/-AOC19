import intcode
import collections
import numpy

intc = intcode.IntCode('day11_in')

hull = collections.defaultdict(lambda: 0)
hull[(0,0)] = 1
pos = (0,0)
dir = 0

def next_pos(x, y, direction ,turn):
    direction += 1 if turn else -1
    direction = direction % 4
    if direction == 3:
        new_pos = (x - 1, y)
    elif direction == 2:
        new_pos = (x, y + 1)
    elif direction == 1:
        new_pos = (x + 1, y)
    else:
        new_pos = (x, y - 1)
    return  new_pos, direction

def paint(intc, hull, pos, dir):
    curr_color = hull[pos]
    new_color = intc.start(curr_color)
    turn = intc.start()
    new_pos, new_dir = next_pos(*pos, dir, turn)
    hull[pos] = new_color
    return new_pos, new_dir
try:    
    while True:
        pos, dir = paint(intc, hull, pos, dir)
except :
    print(len(hull))

def draw_panel(panel):
    xs = sorted(panel.keys(), key= lambda k: k[0])
    ys = sorted(panel.keys(), key = lambda k: k[1])
    xmin, xmax = xs[0][0], xs[-1][0]
    ymin, ymax = ys[0][1], ys[-1][1]

    graph = [['⬜'] * (xmax - xmin + 1) for _ in range(ymax - ymin + 1)]
    for y in range(ymax - ymin + 1):
        for x in range(xmax - xmin + 1):
            if panel[(x + xmin, y + ymin)] == 0:
                graph[y][x] = '⬛'
            else:
                graph[y][x] = '⬜' 
    for line in graph:
        print(*line, sep='')
draw_panel(hull)



