import operator
f = open("day3_in","r")

l1 = list(f.readline().strip().split(','))
l2 = list(f.readline().strip().split(','))
trip = dict()

def getCoord(input):
    direction = (0,0)
    if input[0] == "R":
        direction =  (1,0)
    elif input[0] == "L":
        direction = (-1,0)
    elif input[0] == "D":
        direction = (0,-1)
    else:
        direction = (0,1)
    count = int(input[1:])
    for i in range(count):
        yield direction

x, y = 0, 0
step = 0
for move in l1:
    for h, w in getCoord(move):
        x += h
        y += w
        step += 1
        trip[(x,y)] = step
x, y = 0, 0
step = 0
minSteps = float('inf')
for move in l2:
    for h, w in getCoord(move):
        x += h
        y += w
        step += 1
        if (x,y) in trip and step + trip[(x, y)] < minSteps and x != y != 0:
            minSteps = step + trip[(x, y)]
print(minSteps)


