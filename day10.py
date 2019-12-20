import collections
import math

def get_lines(space, x, y):
    arcs = collections.defaultdict(list)
    for x2, y2 in space:
        if (x2, y2) == (x, y):
            continue
        else:
            dy = y - y2
            dx = x2 - x
            arc = math.atan2(-float(dx), -float(dy)) #atypical input to satisfy transformed coordinate system
            arcs[arc].append((x2, y2))
    return arcs, len(arcs)

def dist(x1, y1, x2, y2):
    return (x1- x2) ** 2 + (y1 - y2) ** 2

f = open('day10_in','r')
lines = list(f.readlines())
space = [(x, y) for y, line in enumerate(lines)
            for x, char in enumerate(line) if char == '#']
point_map = collections.defaultdict(lambda: 0)
for point in space:
    _, count = get_lines(space, *point)
    point_map[point] = count

counter = collections.Counter(point_map)
station, count = counter.most_common(1)[0]
points, _ = get_lines(space, *station)

ordered = collections.OrderedDict(sorted(points.items(), key = lambda item: item[0]))

print(station, count)
print(sorted(list(ordered.values())[199], key = lambda point: dist(*point, *station))[0])