from collections import defaultdict
from functools import reduce
import operator

f = open("day6_in","r")
orbits = list(map(lambda x: tuple(x.strip().split(')')), f.readlines()))
orbitalMap = defaultdict(lambda: [])
for primary, satellite in orbits:
    orbitalMap[primary].append(satellite)
def checkSum(planet, depth = 0):
    if planet is None: return 0
    orbitCount = depth
    for satellite in orbitalMap[planet]:
        orbitCount += checkSum(satellite, depth + 1)
    return orbitCount

def minDist(planet):
    if planet is None: return (0, False, False)
    elif planet == "YOU": return (0,True, False)
    elif planet == "SAN": return (0, False, True)

    paths = filter(None, map(minDist, orbitalMap[planet]))
    next = [0, False, False]
    for path in paths:
        next[0] += path[0]
        next[1] = next[1] or path[1]
        next[2] = next[2] or path[2]
    if next[1] ^ next[2]:
        next[0] += 1
    return tuple(next)

print(minDist("COM"))
